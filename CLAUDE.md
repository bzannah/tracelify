# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tracelify is an open-source RAG (Retrieval-Augmented Generation) knowledge vault with chat. It ingests documents, chunks them, embeds them in ChromaDB, and uses LLMs (OpenAI for embeddings, Anthropic Claude for chat) to answer questions.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # Then fill in OPENAI_API_KEY and ANTHROPIC_API_KEY
```

## Commands

```bash
# Run tests
pytest

# Run a single test
pytest tests/test_ingest.py::test_name -v

# Run the app (FastAPI)
uvicorn tracelify.app:app --reload
```

## Architecture

- **src/tracelify/**: Main package (src layout, built with hatchling)
  - `config.py`: Central configuration — loads `.env`, defines paths (`data/`, `chroma_data/`), chunking params, model names
  - `ingest.py`: Document loading and text chunking pipeline. `Chunk` dataclass is the core data unit (text + doc_id + metadata)
- Uses OpenAI `text-embedding-3-small` for embeddings and Anthropic Claude for chat
- ChromaDB is the vector store, persisted to `chroma_data/` (gitignored)
- Uploaded documents go to `data/` (auto-created by config)

## Key Conventions

- Python 3.9+ compatibility required
- Configuration via environment variables (`.env` file, loaded by python-dotenv)
- Chunk IDs follow the format `{doc_id}::{chunk_index}`
