import json
from pathlib import Path
from typing import Any

from app.embeddings import hash_embedding
from app.models import Document


def _display(resource: dict[str, Any]) -> str:
    code = resource.get("code", {})
    coding = code.get("coding", [{}])
    return code.get("text") or (coding[0].get("display") if coding else None) or resource["resourceType"]


def normalize_bundle(bundle: dict[str, Any], dimensions: int = 384) -> list[Document]:
    documents = []
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        kind, rid = resource.get("resourceType"), resource.get("id")
        if kind not in {"Policy", "Guide", "ProcedureRequest", "Note"} or not rid:
            continue
        subject = resource.get("subject", {}).get("reference", "")
        workspace_id = subject.removeprefix("Workspace/")
        title = _display(resource)
        event_time = resource.get("effectiveDateTime") or resource.get("recordedDate") or resource.get("authoredOn") or resource.get("period", {}).get("start") or "1900-01-01T00:00:00Z"
        value = resource.get("valueQuantity", {})
        value_text = f" Value: {value.get('value')} {value.get('unit', '')}." if value else ""
        status = resource.get("knowledgeStatus", {}).get("coding", [{}])[0].get("code") or resource.get("status", "unknown")
        text = f"{title}. Status: {status}.{value_text}"
        documents.append(Document(rid, workspace_id, kind, event_time, title, text,
                                   {"source": "bundled representative synthetic source JSON"}, hash_embedding(text, dimensions)))
    return documents


def load_bundle(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

