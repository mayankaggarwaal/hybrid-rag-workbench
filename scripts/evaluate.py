import json

from app.ingest import load_bundle, normalize_bundle
from app.llm import MockProvider
from app.retrieval.memory import InMemoryRetrievalProvider
from app.service import RAGService


def main() -> None:
    retrieval = InMemoryRetrievalProvider()
    retrieval.index(normalize_bundle(load_bundle("data/synthetic_bundle.json")))
    service = RAGService(retrieval, MockProvider())
    with open("evals/cases.json", encoding="utf-8") as case_file:
        cases = json.load(case_file)
    passed = 0
    for case in cases:
        response = service.ask(case["workspace_id"], case["question"])
        ids = {citation.document_id for citation in response.citations}
        ok = (not response.evidence_sufficient) if case.get("expect_insufficient") else case["expected_document"] in ids
        passed += ok
        print(("PASS" if ok else "FAIL"), case["question"])
    print(f"{passed}/{len(cases)} cases passed")
    raise SystemExit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()

