from app.models import Document, SearchHit
from app.retrieval.base import RetrievalProvider


class OpenSearchProvider(RetrievalProvider):
    """Future scale adapter contract; deliberately does not provision infrastructure."""
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def index(self, documents: list[Document]) -> None:
        raise NotImplementedError("Add an authenticated OpenSearch client when scale requires it")

    def search(self, workspace_id: str, query: str, limit: int = 5) -> list[SearchHit]:
        raise NotImplementedError("Implement BM25 + k-NN fusion against an existing cluster")

    def timeline(self, workspace_id: str, limit: int = 50) -> list[Document]:
        raise NotImplementedError


