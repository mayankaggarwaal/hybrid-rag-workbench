import re

from app.llm import LLMProvider
from app.models import AskResponse, Citation
from app.retrieval.base import RetrievalProvider

NOTICE = "Synthetic/de-identified demo only. Informational user support; not unsupported decision-making. No workspace-document writes."


class RAGService:
    def __init__(self, retrieval: RetrievalProvider, llm: LLMProvider, top_k: int = 5) -> None:
        self.retrieval, self.llm, self.top_k = retrieval, llm, top_k

    def ask(self, workspace_id: str, question: str) -> AskResponse:
        hits = [hit for hit in self.retrieval.search(workspace_id, question, self.top_k) if hit.score > 0.05]
        citations = [Citation(document_id=h.document.id, resource_type=h.document.resource_type,
                     event_time=h.document.event_time, title=h.document.title,
                     excerpt=h.document.text[:240]) for h in hits]
        evidence = [f"[E{i}] {h.document.event_time} {h.document.title}: {h.document.text}" for i, h in enumerate(hits, 1)]
        answer = self.llm.generate(question, evidence)
        sufficient = bool(hits)
        if sufficient and not re.search(r"\[E\d+\]", answer):
            answer += " " + " ".join(f"[E{i}]" for i in range(1, len(hits) + 1))
        if not sufficient:
            answer = "Insufficient evidence is available in this synthetic record to answer the question."
        return AskResponse(answer=answer, citations=citations, safety_notice=NOTICE, evidence_sufficient=sufficient)


