from app.ingest import load_bundle, normalize_bundle
from app.llm import MockProvider
from app.retrieval.memory import InMemoryRetrievalProvider
from app.service import RAGService


def make_service() -> RAGService:
    provider = InMemoryRetrievalProvider()
    provider.index(normalize_bundle(load_bundle("data/synthetic_bundle.json")))
    return RAGService(provider, MockProvider())


def test_retrieval_is_workspace_scoped_and_cited() -> None:
    response = make_service().ask("workspace-demo", "What is the deployment window?")
    assert response.evidence_sufficient
    assert response.citations[0].document_id == "guide-deploy-001"
    assert "[E1]" in response.answer
    assert "not unsupported decision" in response.safety_notice


def test_unknown_workspace_returns_safe_insufficient_evidence() -> None:
    response = make_service().ask("does-not-exist", "What procedures are present?")
    assert not response.evidence_sufficient
    assert response.citations == []
    assert "Insufficient evidence" in response.answer


def test_no_record_write_capability_on_service() -> None:
    assert not hasattr(make_service(), "write_workspace")


