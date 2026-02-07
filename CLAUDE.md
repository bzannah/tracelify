# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tracelify is an open-source RAG (Retrieval-Augmented Generation) knowledge vault with chat. Monorepo with a FastAPI backend (`apps/api`) and docs.

## Commands

```bash
make install                                           # Install all dependencies (uses uv)
make dev-db                                            # Start PostgreSQL (pgvector)
make dev-api                                           # Start FastAPI dev server
make test                                              # Run all tests
cd apps/api && uv run pytest tests/test_health.py -v   # Run a single test file
```

## Architecture

- **apps/api/src/tracelify/**: Main backend package
  - `app.py`: FastAPI app factory (`create_app()`)
  - `config.py`: Central config — loads `.env`, defines paths, chunking params, model names (OpenAI for embeddings, DeepSeek for chat)
  - `errors.py`: Structured error handling (`APIError`, `ErrorResponse`)
  - `middleware.py`: Request ID middleware (`X-Request-ID`)
  - `ingest.py`: Document loading and text chunking. `Chunk` dataclass is the core data unit
  - `routers/`: API endpoint modules (`health.py`, etc.)
- **apps/api/tests/**: pytest suite with TestClient fixture in `conftest.py`

## Key Conventions

- Python 3.9+ compatibility required
- App factory pattern: `create_app()` in `app.py` for testable FastAPI instances
- Each feature gets its own router in `routers/`
- Configuration via environment variables (`.env` file, loaded by python-dotenv)
- Chunk IDs follow the format `{doc_id}::{chunk_index}`
- Package manager: uv (workspace root at repo root, app package in `apps/api`)
