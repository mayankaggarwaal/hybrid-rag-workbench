from pathlib import Path

from app.ingest import load_bundle, normalize_bundle


def test_bundle_normalizes_supported_resources() -> None:
    docs = normalize_bundle(load_bundle(Path("data/synthetic_bundle.json")))
    assert len(docs) == 4
    assert {doc.workspace_id for doc in docs} == {"workspace-demo"}
    assert all(len(doc.embedding) == 384 for doc in docs)


