# Tracelify — Product Vision

## One-liner

An open-source RAG knowledge vault that lets you chat with your documents, with citations you can trust.

## Problem

Teams and individuals accumulate knowledge across docs, notes, and files but have no fast, private way to query it conversationally. Existing solutions are either closed-source (lock-in, data leaves your machine), lack source attribution (hallucination risk), or require complex infrastructure to self-host.

## Vision

Tracelify is a local-first, open-source knowledge vault. You drop in documents, and Tracelify chunks, embeds, and indexes them. When you ask a question, it retrieves relevant context and generates an answer with inline citations pointing back to the original source and chunk. Every answer is traceable — hence the name.

## Principles

1. **Local-first.** Everything runs on your machine by default. Your documents never leave your environment unless you choose to deploy to a team server.
2. **Traceable answers.** Every response includes citations with document name, chunk location, and relevance score. No black-box answers.
3. **Open-source, no lock-in.** MIT-licensed. Standard formats (plain text, markdown) in, standard vector DB (ChromaDB) underneath. Swap LLM providers freely.
4. **Safe by default.** Document content is treated as untrusted data. Retrieved chunks are clearly delimited in prompts to defend against indirect prompt injection.

## Target Users

| Phase | User | Need |
|-------|------|------|
| MVP | Individual developer or researcher | Chat with personal notes, papers, docs locally |
| V1 | Small team (2–10) | Shared knowledge vault with access control |
| V2 | Organization | Multi-vault, audit trail, SSO |

## MVP Scope

The MVP delivers a working local pipeline: ingest, retrieve, chat with citations.

### In scope

- **Document ingestion**: Upload `.txt` and `.md` files via API
- **Chunking**: Configurable overlapping text chunking
- **Embedding**: OpenAI `text-embedding-3-small` (swappable)
- **Vector storage**: ChromaDB, persisted to disk
- **Chat**: DeepSeek generates answers from retrieved context (free tier available)
- **Citations**: Each response includes which chunks were used, with document name and chunk ID
- **FastAPI backend**: REST API for ingest and chat

### Out of scope (MVP)

- Web UI (API-only for MVP)
- Multi-user auth and access control
- PDF, DOCX, or other binary format parsing
- Hosted/cloud deployment
- Conversation memory across sessions

## Post-MVP Roadmap

### V1 — Team use

- Web UI for upload, chat, and citation browsing
- Conversation history with session persistence
- Multi-user support with simple API key auth
- PDF and DOCX ingestion
- Configurable LLM backend (swap between DeepSeek, OpenAI, Anthropic, local models)

### V2 — Organization scale

- Multi-vault workspaces (e.g., per-project or per-team)
- Role-based access control and SSO
- Audit log of queries and retrieved documents
- Webhook integrations (Slack, etc.)
- Hybrid search (keyword + semantic)

## Architecture Direction

```
User → FastAPI → Ingest Pipeline → ChromaDB
                                      ↓
User → FastAPI → Retrieval → LLM (with context + citation metadata) → Response
```

- **Ingest path**: File upload → load document → chunk text → embed chunks → store in ChromaDB with metadata
- **Query path**: User question → embed query → retrieve top-k chunks → construct prompt with chunk citations → LLM generates answer → return answer + citation list
- **Citation format**: Each cited chunk includes `doc_id`, `chunk_index`, `filename`, and relevance score so the user can verify the source

## Safety: Prompt Injection Defense

Retrieved document chunks are **untrusted data**. Tracelify treats them accordingly:

1. **Delimiter isolation**: Retrieved chunks are wrapped in clearly marked delimiters in the prompt so the LLM can distinguish instructions from document content.
2. **No instruction forwarding**: The system prompt explicitly instructs the model to treat chunk content as reference data, not as instructions to follow.
3. **Citation as verification**: By always showing which chunks informed an answer, users can spot when a response has been influenced by adversarial content in a document.
4. **Input sanitization**: Uploaded documents are validated for format and size before entering the pipeline.

## Success Metrics (MVP)

- A user can ingest a set of markdown files and get accurate, cited answers in under 5 seconds locally
- Every answer includes at least one citation pointing to a real chunk
- Zero data sent to external services beyond the configured LLM/embedding API calls
