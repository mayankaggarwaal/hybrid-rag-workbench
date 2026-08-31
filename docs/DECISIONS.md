# Architecture decision log

## ADR-001 — Hosted Supabase is the primary database

**Status:** accepted. Hybrid retrieval uses PostgreSQL full-text search and pgvector in hosted Supabase, combined with reciprocal-rank fusion. The local demo uses an in-memory equivalent so tests need no database. OpenSearch remains an unimplemented adapter boundary and no AWS resource is provisioned.

## ADR-002 — Provider-isolated generation

**Status:** accepted. `LLMProvider` separates orchestration from generation. `MockProvider` is the safe offline default; `GroqProvider` and `GeminiProvider` read environment API keys. The Codex desktop session is not treated as an endpoint. OpenAI is documented only as a future adapter.

## ADR-003 — Synthetic-only knowledge data and read-only surfaces

**Status:** accepted. The bundled representative source JSON data is hand-authored and synthetic, with explicit provenance limitations. API and MCP surfaces expose no workspace-document mutations. Answers abstain on empty evidence and provide structured citations.

## ADR-004 — Deterministic local embeddings

**Status:** accepted for the portfolio demo, not knowledge production. Feature hashing provides zero-network, reproducible tests and keeps ingestion/retrieval interfaces realistic. Production adoption requires a validated, versioned knowledge embedding model and a vector-dimension migration.

## ADR-005 — Runtime and validation

**Status:** accepted. The machine's default Python is 3.7.3 and cannot run the project. A workspace-local `.venv` was created with bundled Python 3.12 and declared dependencies installed from PyPI after explicit network permission. Verification uses that isolated interpreter. Hosted Supabase and Groq paths remain unexecuted because no credentials or external resources were requested.

