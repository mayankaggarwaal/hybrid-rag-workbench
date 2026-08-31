from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class Document:
    id: str
    workspace_id: str
    resource_type: str
    event_time: str
    title: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: float


class AskRequest(BaseModel):
    workspace_id: str = Field(min_length=1)
    question: str = Field(min_length=3, max_length=1000)


class Citation(BaseModel):
    document_id: str
    resource_type: str
    event_time: str
    title: str
    excerpt: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    safety_notice: str
    evidence_sufficient: bool


