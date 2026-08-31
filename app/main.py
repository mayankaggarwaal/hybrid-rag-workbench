from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.container import build_service
from app.models import AskRequest, AskResponse
from app.service import NOTICE

app = FastAPI(title="Hybrid RAG Workbench", version="0.1.0", description=NOTICE)
service = build_service()


@app.get("/status")
def status() -> dict[str, str]:
    return {"status": "ok", "safety": NOTICE}


@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return service.ask(request.workspace_id, request.question)


@app.get("/", response_class=HTMLResponse)
def demo() -> str:
    return """<!doctype html><html><head><meta charset='utf-8'><title>Hybrid RAG Workbench</title>
<style>body{font:16px system-ui;max-width:760px;margin:3rem auto;padding:0 1rem;color:#172033}textarea,input{width:100%;padding:.7rem;margin:.3rem 0 1rem;box-sizing:border-box}button{background:#2457d6;color:white;border:0;padding:.7rem 1rem;border-radius:6px}pre{white-space:pre-wrap;background:#f3f5f8;padding:1rem}</style></head><body>
<h1>Hybrid RAG Workbench</h1><p><strong>Synthetic data only.</strong> Informational user support—not unsupported decision-making. Read-only; citations required.</p>
<label>Workspace ID</label><input id='p' value='workspace-demo'><label>Question</label><textarea id='q'>What deployment window evidence is present?</textarea><button onclick='go()'>Retrieve evidence</button><pre id='out'>Ready.</pre>
<script>async function go(){out.textContent='Loading…';let r=await fetch('/api/ask',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({workspace_id:p.value,question:q.value})});out.textContent=JSON.stringify(await r.json(),null,2)}</script></body></html>"""


