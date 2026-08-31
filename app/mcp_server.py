from mcp.server.fastmcp import FastMCP

from app.container import build_service

mcp = FastMCP("hybrid-rag-workbench")
service = build_service()


@mcp.tool()
def workspace_summary(workspace_id: str) -> dict:
    """Read-only summary of a synthetic workspace document."""
    return service.ask(workspace_id, "Summarize the available synthetic knowledge record.").model_dump()


@mcp.tool()
def workspace_timeline(workspace_id: str) -> list[dict]:
    """Read-only timeline for a synthetic workspace."""
    return [vars(doc) for doc in service.retrieval.timeline(workspace_id)]


@mcp.tool()
def evidence_lookup(workspace_id: str, query: str) -> dict:
    """Retrieve cited evidence from a synthetic workspace document."""
    return service.ask(workspace_id, query).model_dump()


if __name__ == "__main__":
    mcp.run()

