# Tracelify

Open-source RAG knowledge vault with chat. Upload documents, chunk and embed them, then ask questions answered by your own knowledge base.

## MVP Features

- Document ingestion with configurable text chunking
- Vector storage and retrieval
- Chat interface powered by DeepSeek with retrieved context
- FastAPI backend with file upload support

## Project Structure

```
tracelify/
├── apps/
│   └── api/          # FastAPI backend
├── docs/             # Documentation and ADRs
└── Makefile          # Development commands
```

## Getting Started

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [Docker](https://docs.docker.com/get-docker/) (for PostgreSQL)

### Setup

```bash
# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and DEEPSEEK_API_KEY

# Install Python dependencies
make install
```

### Development

```bash
make dev-db     # Start PostgreSQL (pgvector) in background
make dev-api    # Start FastAPI dev server (http://localhost:8000)
make test       # Run all tests
```

API docs available at http://localhost:8000/docs when the server is running.

### All Commands

```bash
make install    # Install all dependencies
make dev-db     # Start PostgreSQL (pgvector)
make dev-api    # Start FastAPI dev server
make test       # Run all tests
make lint       # Lint with ruff
make format     # Format with ruff
make db-down    # Stop PostgreSQL (data persists in Docker volume)
make db-logs    # Tail PostgreSQL logs
```

Default database connection: `postgresql://tracelify:tracelify@localhost:5432/tracelify` (configured in `.env`).
