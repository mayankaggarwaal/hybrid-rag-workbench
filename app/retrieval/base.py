from abc import ABC, abstractmethod

from app.models import Document, SearchHit


class RetrievalProvider(ABC):
    @abstractmethod
    def index(self, documents: list[Document]) -> None: ...

    @abstractmethod
    def search(self, workspace_id: str, query: str, limit: int = 5) -> list[SearchHit]: ...

    @abstractmethod
    def timeline(self, workspace_id: str, limit: int = 50) -> list[Document]: ...


