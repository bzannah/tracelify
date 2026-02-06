# Tracelify

Open-source RAG knowledge vault with chat. Upload documents, chunk and embed them, then ask questions answered by your own knowledge base.

## MVP Features

- Document ingestion with configurable text chunking
- Vector storage and retrieval via ChromaDB
- Chat interface powered by Claude with retrieved context
- FastAPI backend with file upload support

## Getting Started

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Configure API keys
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and ANTHROPIC_API_KEY

# Run the server
uvicorn tracelify.app:app --reload
```
