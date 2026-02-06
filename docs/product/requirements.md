# Tracelify — Product Requirements

## MVP — Must-Have

These features define the minimum viable product: a local RAG pipeline that ingests documents and answers questions with citations.

### F1: Document Ingestion

Upload `.txt` and `.md` files through the REST API. Files are stored in the local `data/` directory.

**Acceptance criteria:**
- [ ] `POST /ingest` accepts a file upload and returns a document ID
- [ ] Rejects files that are not `.txt` or `.md`
- [ ] Rejects files exceeding 10 MB
- [ ] Returns 409 if a document with the same filename already exists (or overwrites with a query param)

### F2: Text Chunking

Split ingested documents into overlapping chunks for embedding.

**Acceptance criteria:**
- [ ] Chunks default to 500 characters with 50-character overlap (configurable via `config.py`)
- [ ] Each chunk has a unique ID in the format `{doc_id}::{chunk_index}`
- [ ] Empty documents produce zero chunks
- [ ] Chunking preserves all original text (no content is silently dropped)

### F3: Embedding and Storage

Embed chunks using OpenAI and store vectors in ChromaDB.

**Acceptance criteria:**
- [ ] Chunks are embedded using `text-embedding-3-small`
- [ ] Vectors are stored in ChromaDB with metadata: `doc_id`, `chunk_index`, `filename`
- [ ] ChromaDB data persists to `chroma_data/` across server restarts
- [ ] Re-ingesting a document replaces its previous chunks in the store

### F4: Retrieval

Given a user query, retrieve the most relevant chunks from the vector store.

**Acceptance criteria:**
- [ ] Query is embedded with the same model used for document chunks
- [ ] Returns top-k chunks (default k=3, configurable)
- [ ] Each result includes the chunk text, metadata, and a relevance score

### F5: Chat with Citations

Send retrieved context to Claude and return an answer with source references.

**Acceptance criteria:**
- [ ] `POST /chat` accepts a `question` string and returns an answer with a `citations` list
- [ ] Each citation includes `doc_id`, `chunk_index`, `filename`, and relevance score
- [ ] Retrieved chunks are wrapped in delimiters in the prompt (prompt injection defense)
- [ ] The system prompt instructs the model to only answer from provided context and to say "I don't know" when context is insufficient
- [ ] Response time under 10 seconds for a vault with fewer than 100 documents

### F6: Document Management

List and delete documents from the vault.

**Acceptance criteria:**
- [ ] `GET /documents` returns a list of ingested documents with metadata (filename, chunk count, ingestion time)
- [ ] `DELETE /documents/{doc_id}` removes the document file and all associated chunks from ChromaDB

## Phase 2 — Should-Have

Features for team adoption and usability.

### F7: Web UI

A browser-based interface for uploading documents and chatting.

- [ ] File upload with drag-and-drop
- [ ] Chat interface with inline citation highlights
- [ ] Document list with delete capability
- [ ] Citation click-through to view the source chunk in context

### F8: Conversation History

Persist chat sessions so users can resume conversations.

- [ ] Sessions stored locally (SQLite or JSON)
- [ ] `GET /sessions` lists previous conversations
- [ ] Chat endpoint accepts an optional `session_id` to continue a conversation
- [ ] Context window management: include recent conversation turns in the prompt

### F9: PDF and DOCX Ingestion

Expand supported file types beyond plain text.

- [ ] Parse PDF files (extract text, ignore images for now)
- [ ] Parse DOCX files
- [ ] Maintain the same chunking and embedding pipeline

### F10: Configurable LLM Backend

Allow users to swap LLM and embedding providers.

- [ ] Support OpenAI, Anthropic, and local models (e.g., Ollama) for chat
- [ ] Support OpenAI and local models for embeddings
- [ ] Configuration via `.env` variables: `CHAT_PROVIDER`, `EMBEDDING_PROVIDER`
- [ ] Provider-specific settings (model name, API base URL)

## Phase 3 — Nice-to-Have

Features for organizational scale and advanced use cases.

### F11: Multi-Vault Workspaces

Separate knowledge into isolated vaults.

- [ ] Create, list, and delete vaults via API
- [ ] Each vault has its own ChromaDB collection and document storage
- [ ] Chat queries are scoped to a specific vault

### F12: Access Control

Multi-user support with permissions.

- [ ] API key authentication
- [ ] Role-based access: admin (manage users, vaults) and member (ingest, chat)
- [ ] SSO integration (OAuth2 / OIDC)

### F13: Audit Log

Track who queried what and which documents were retrieved.

- [ ] Log each chat query with timestamp, user, question, and cited chunks
- [ ] Queryable via API: filter by user, date range, document
- [ ] Export as CSV or JSON

### F14: Hybrid Search

Combine semantic and keyword search for better retrieval.

- [ ] BM25 keyword search alongside vector similarity
- [ ] Reciprocal rank fusion to merge results
- [ ] User-configurable weighting between keyword and semantic scores

### F15: Integrations

Connect Tracelify to external tools.

- [ ] Slack bot: query the vault from a Slack channel
- [ ] Webhook on ingestion: notify external systems when documents are added
- [ ] CLI tool for scripted ingestion and queries
