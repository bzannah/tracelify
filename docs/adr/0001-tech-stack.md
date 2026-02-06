# ADR-0001: Technology Stack

**Status:** Accepted
**Date:** 2026-02-06

## Context and Problem

Tracelify is an open-source RAG knowledge vault. The prototype used ChromaDB for vector storage and required OpenAI API keys for embeddings — meaning contributors couldn't run the pipeline without a paid account.

We need a stack that is:

- **Approachable** for beginners learning or contributing
- **Testable** at every layer without external service dependencies
- **Open-source friendly** with no vendor lock-in
- **Production-ready** without requiring a rewrite later

## Decision

| Layer | Choice |
|-------|--------|
| Backend | Python + FastAPI |
| Database | PostgreSQL + pgvector |
| Migrations | Alembic (with SQLAlchemy models) |
| Frontend | Next.js (Phase 2) |
| Embeddings | Local CPU embeddings by default, pluggable provider interface |
| Chat model | Pluggable provider, Anthropic Claude default |

### Why these choices

**Python + FastAPI.** Python is the lingua franca of the AI/ML ecosystem. FastAPI gives us native async (needed for streaming LLM responses), automatic OpenAPI docs, and Pydantic validation — with minimal boilerplate.

**PostgreSQL + pgvector.** One database for both relational data (documents, users, sessions) and vector similarity search. Eliminates running a separate vector DB alongside a relational DB. PostgreSQL is battle-tested for production, and pgvector is a simple extension (`CREATE EXTENSION vector`).

**Alembic.** Version-controlled schema migrations generated from SQLAlchemy models. Essential for an open-source project where contributors need reproducible database state.

**Next.js.** Largest React ecosystem, extensive learning resources, SSR support. Lowers the barrier for frontend contributors.

**Local CPU embeddings.** Default to `sentence-transformers/all-MiniLM-L6-v2` so the full pipeline runs without API keys. A provider interface lets users swap in OpenAI or Cohere for higher quality.

**Pluggable chat provider.** Anthropic Claude is the default, but the chat layer is behind an interface. Users can plug in OpenAI, Ollama (local), or others.

## Alternatives Considered

### ChromaDB instead of pgvector

ChromaDB was used in the prototype. It's embedded (no server process), zero-config, and has a clean Python API.

**Why we moved away:** It requires a separate store alongside whatever relational DB we'd need for users, sessions, and audit logs. pgvector lets us join vector results with relational data in one query (e.g., chunks filtered by document ownership). PostgreSQL also has mature tooling for backups, replication, and monitoring that ChromaDB lacks.

**What we lose:** ChromaDB's simplicity. pgvector requires a running Postgres instance, which is heavier for local dev. We mitigate with `docker-compose.yml`.

### Pinecone / Weaviate / Qdrant

Dedicated vector databases with advanced features: filtering, hybrid search, automatic index tuning, sharding.

**Why not:** All add operational complexity or vendor lock-in. pgvector is sufficient at our scale. If we outgrow it, Qdrant (open-source, Rust-based) is the most likely upgrade path.

### Django instead of FastAPI

Batteries included: ORM, admin panel, auth, migrations built in.

**Why not:** Django's sync-first architecture is a poor fit for streaming LLM responses. Its ORM is powerful but heavier than SQLAlchemy for our needs. FastAPI's async support and automatic OpenAPI docs are better aligned with an API-first RAG system.

### Node.js backend (Express / Hono)

Would unify the stack with Next.js (one language everywhere).

**Why not:** The Python AI/ML ecosystem (sentence-transformers, tokenizers, LangChain, etc.) has no Node equivalents of equal quality. The cost of two languages is lower than the cost of fighting the ecosystem.

### OpenAI embeddings as default

Higher quality embeddings (`text-embedding-3-small`, 1536 dimensions) with minimal code.

**Why not:** Requires an API key and costs money for every ingestion. Contributors can't run or test the pipeline without a paid account. Local embeddings by default means anyone can clone the repo and run the full system in minutes.

### SvelteKit / Remix instead of Next.js

SvelteKit has smaller bundles and a simpler reactivity model. Remix has excellent data loading patterns.

**Why not:** Next.js has the largest community and most learning resources. For an open-source project targeting beginners, ecosystem size matters more than technical elegance.

### Raw SQL instead of Alembic

Simpler, no ORM dependency, full control.

**Why not:** Manual migration tracking is error-prone as the schema grows. Alembic auto-generates migrations from model changes and provides rollback — standard workflow most Python developers already know.

## Consequences

### Good

- **Zero API keys for dev.** Local embeddings mean contributors can run the full ingest → retrieve pipeline without any accounts or API spend.
- **One database.** PostgreSQL handles relational data and vectors. One thing to back up, monitor, query, and reason about.
- **Familiar tools.** Python, PostgreSQL, React, Alembic — widely known, extensively documented.
- **No vendor lock-in.** Pluggable provider interfaces for both embeddings and chat. Users choose what fits their budget and privacy needs.
- **Production path.** FastAPI + PostgreSQL + Next.js is a proven stack. No rewrite needed as the project scales.

### Bad

- **Heavier local setup.** PostgreSQL requires Docker or a local install, unlike ChromaDB's embedded mode. Mitigated by `docker-compose.yml`.
- **Two languages.** Python backend + TypeScript frontend. In practice, most contributions are backend-only or frontend-only, so the overlap cost is low.
- **Lower default embedding quality.** `all-MiniLM-L6-v2` (384 dimensions) produces noticeably worse retrieval than OpenAI's model (1536 dimensions). Users who need quality should switch providers. We document this clearly.
- **pgvector lacks built-in hybrid search.** No native BM25. Implementing keyword + semantic search (F14) will require additional work (e.g., PostgreSQL full-text search + reciprocal rank fusion).
- **Alembic learning curve.** Contributors unfamiliar with migration workflows need ramp-up time. Mitigated with docs and helper scripts.
