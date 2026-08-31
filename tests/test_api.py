from fastapi.testclient import TestClient

import app.main as main_module
from app.ingest import load_bundle, normalize_bundle
from app.llm import MockProvider
from app.retrieval.memory import InMemoryRetrievalProvider
from app.service import RAGService


def test_status_and_ask() -> None:
    retrieval = InMemoryRetrievalProvider()
    retrieval.index(normalize_bundle(load_bundle("data/synthetic_bundle.json")))
    main_module.service = RAGService(retrieval, MockProvider())
    client = TestClient(main_module.app)
    assert client.get("/status").status_code == 200
    response = client.post("/api/ask", json={"workspace_id": "workspace-demo", "question": "uptime evidence?"})
    assert response.status_code == 200
    assert response.json()["citations"]

