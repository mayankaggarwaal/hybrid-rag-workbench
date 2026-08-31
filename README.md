# Hybrid RAG Workbench

A portfolio-grade, safety-constrained retrieval-augmented generation demo for knowledge-support workflows. It turns **synthetic source JSON** resources into workspace-scoped evidence, fuses PostgreSQL full-text and vector search, and returns answers with structured citations.

> **Safety boundary:** demonstration data only. This software is informational user support—not a regulated device, unsupported decision-making system. Never load real workspace data. The API and MCP surface are read-only.

## Why this project

The repository demonstrates production-minded MLE/AI engineering: provider abstractions, deterministic offline tests, hybrid retrieval, source data normalization, evidence-grounded generation, tenant-style workspace filtering, evaluation cases, MCP interoperability, and a clean path from local demo to hosted Supabase.

```text
Synthetic source JSON ─→ normalization + deterministic embeddings ─→ hosted Supabase
                                                                  ├─ PostgreSQL FTS
Browser / API / MCP ─→ safety-constrained RAG service ─────────────┤─ pgvector
                                      │                           └─ RRF fusion
                                      └─ Mock (offline) / Groq (env key)
```

OpenSearch is represented by a `RetrievalProvider` adapter boundary for a future high-scale deployment. This project does not provision AWS, OpenSearch, or any paid resource.

## Quick start (fully offline)

Python 3.11+ is required.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/evaluate.py
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`, or use the API:

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "content-type: application/json" \
  -d '{"workspace_id":"workspace-demo","question":"What deployment window evidence is present?"}'
```

The default `MockProvider` is deterministic and makes no network calls. Its output is deliberately plain; it tests retrieval, evidence flow, and safety behavior rather than prose quality.

## Hosted Supabase setup

1. Create a Supabase project yourself (the repository never provisions one).
2. Run [`sql/001_supabase_schema.sql`](sql/001_supabase_schema.sql) in its SQL editor. It enables `pgvector`, creates FTS/vector indexes, and enables RLS without public policies.
3. Copy `.env.example` to `.env` and set `SUPABASE_DB_URL` to a least-privilege **server-side** Postgres connection string. Keep it out of the browser and Git.
4. Run `python scripts/ingest.py data/synthetic_bundle.json`.
5. Start the API. When `SUPABASE_DB_URL` is set, the service automatically selects `SupabasePostgresProvider`.

The sample uses a deterministic feature-hashing embedding so the whole pipeline is auditable and offline-capable. For production-quality semantic recall, add a versioned knowledge embedding provider, migrate the vector dimension, validate on a representative corpus, and track model/data lineage.

## LLM providers

- `LLM_PROVIDER=mock` (default): offline and deterministic.
- `LLM_PROVIDER=gemini`: set `GEMINI_API_KEY` and optionally `GEMINI_MODEL`. Run `python scripts/smoke_gemini.py` for one synthetic-only connectivity check.
- `GroqProvider` remains available as an adapter for future use, but the environment template now promotes Gemini rather than Groq.
- An OpenAI API adapter can be added behind `LLMProvider`; it is intentionally neither required nor configured here. A Codex desktop conversation is not used as a deployable endpoint.

The response layer drops weak evidence, forces an explicit insufficient-evidence answer when retrieval is empty, and ensures returned claims have evidence labels. Structured citation objects remain the source of truth; downstream consumers should render them beside the answer.

## MCP server

Run `python -m app.mcp_server`. It exposes only:

- `workspace_summary(workspace_id)`
- `workspace_timeline(workspace_id)`
- `evidence_lookup(workspace_id, query)`

There are no workspace-create/update/delete tools.

## Data provenance and limitations

`data/synthetic_bundle.json` is a small, hand-authored representative **synthetic** source JSON Bundle, inspired by the resource shapes emitted by [sample generator](https://github.com/example/synthea). It is not claimed to be an actual sample generator export and contains no real person or workspace information. Its tiny, curated scope cannot establish knowledge accuracy, fairness, robustness, coding completeness, interoperability conformance, or real-world retrieval quality.

For a larger demo, generate source JSON records locally with sample generator, keep its provenance metadata, validate resources, and ingest only synthetic outputs. Do not mix real exports into this repository.

## Security and deployment notes

- Workspace ID filters are applied inside both lexical and semantic SQL branches, preventing cross-workspace fusion.
- RLS is enabled, but a real deployment must add organization/user claims and matching policies; workspace ID alone is not authorization.
- Use a secrets manager, TLS, short-lived credentials, audit logging, rate limits, input/output monitoring, and private networking.
- Pin and scan dependencies and images; add migration management and database backups.
- Before any knowledge use, obtain security, privacy, knowledge-safety, legal, and regulatory review. This demo is not suitable for such use.
- `compose.yaml` wraps only the API. Supabase stays hosted, and no local Postgres or OpenSearch is required.

## Repository map

| Path | Purpose |
|---|---|
| `app/retrieval/` | Provider contract, offline memory implementation, Supabase hybrid adapter, OpenSearch future adapter |
| `app/ingest.py` | source JSON normalization and deterministic embeddings |
| `app/service.py` | retrieval orchestration, citations, insufficient-evidence guardrail |
| `app/main.py` | FastAPI, demo UI, read-only question endpoint |
| `app/mcp_server.py` | basic read-only MCP tools |
| `sql/` | hosted Supabase schema and indexes |
| `tests/`, `evals/` | unit/API safety tests and retrieval evaluation starter set |

## Evaluation roadmap

The starter evaluation checks evidence recall and the unknown-workspace abstention path. A serious next phase should add Recall@k/MRR, citation precision, answer faithfulness scored independently of the generator, temporal questions, negation, adversarial prompt injection in records, workspace-isolation tests against Postgres, latency/cost traces, and user-authored synthetic cases.

## License

Add the license appropriate to your intended publication before distributing the repository.

