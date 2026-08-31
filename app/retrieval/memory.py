import math
import re

from app.embeddings import hash_embedding
from app.models import Document, SearchHit
from app.retrieval.base import RetrievalProvider


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / ((math.sqrt(sum(x*x for x in a)) or 1) * (math.sqrt(sum(y*y for y in b)) or 1))


class InMemoryRetrievalProvider(RetrievalProvider):
    def __init__(self, dimensions: int = 384) -> None:
        self.documents: list[Document] = []
        self.dimensions = dimensions

    def index(self, documents: list[Document]) -> None:
        self.documents.extend(documents)

    def search(self, workspace_id: str, query: str, limit: int = 5) -> list[SearchHit]:
        terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        query_vector = hash_embedding(query, self.dimensions)
        hits = []
        for doc in self.documents:
            if doc.workspace_id != workspace_id:
                continue
            words = set(re.findall(r"[a-z0-9]+", doc.text.lower()))
            lexical = len(terms & words) / max(len(terms), 1)
            vector = max(0.0, _cosine(query_vector, doc.embedding or hash_embedding(doc.text, self.dimensions)))
            hits.append(SearchHit(doc, 0.55 * lexical + 0.45 * vector))
        return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]

    def timeline(self, workspace_id: str, limit: int = 50) -> list[Document]:
        docs = [doc for doc in self.documents if doc.workspace_id == workspace_id]
        return sorted(docs, key=lambda doc: doc.event_time, reverse=True)[:limit]


