# API Standards

## Router Organization

- Each feature gets its own router file in `apps/api/src/tracelify/routers/`.
- Routers are registered in `create_app()` in `app.py` via `app.include_router(...)`.
- Use `APIRouter(tags=["feature_name"])` for OpenAPI grouping.
- One router per file. File name matches the feature: `health.py`, `documents.py`, `chat.py`.

```python
# routers/documents.py
router = APIRouter(tags=["documents"], prefix="/documents")

# app.py
app.include_router(documents.router)
```

## Endpoint Conventions

- All endpoint handlers are `async def`.
- Annotate return types explicitly.
- Every endpoint has a docstring — it becomes the description in OpenAPI docs.
- Use plural nouns for resource collections: `/documents`, `/chunks`, `/sessions`.

```python
@router.get("/documents")
async def list_documents() -> list[DocumentResponse]:
    """List all ingested documents with metadata."""

@router.post("/documents", status_code=201)
async def upload_document(file: UploadFile) -> DocumentResponse:
    """Upload and ingest a document."""

@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(doc_id: str) -> None:
    """Delete a document and its chunks."""
```

## Request & Response Schemas

- Define Pydantic models for all request bodies and response shapes. Don't return raw `dict`.
- Schema classes live in the router file unless shared across routers — then move to a `schemas.py`.
- Use descriptive field names. Include `Field(description=...)` for non-obvious fields.

```python
class ChatRequest(BaseModel):
    question: str = Field(description="The user's question to answer from the knowledge vault")

class Citation(BaseModel):
    doc_id: str
    chunk_index: int
    filename: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
```

## Error Format

- Use FastAPI's `HTTPException` for all error responses.
- Return consistent error JSON: `{"detail": "Human-readable message"}`.
- Use standard HTTP status codes:
  - `400` — bad request (invalid input, wrong file type)
  - `404` — resource not found
  - `409` — conflict (duplicate document)
  - `413` — payload too large (file size exceeded)
  - `422` — validation error (handled automatically by FastAPI/Pydantic)
  - `500` — internal server error (generic, no internal details)

```python
from fastapi import HTTPException

if not file.filename.endswith((".txt", ".md")):
    raise HTTPException(status_code=400, detail="Only .txt and .md files are supported")

if file.size > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File exceeds 10 MB limit")
```

## Path Parameters & Query Parameters

- Path parameters for resource identifiers: `/documents/{doc_id}`.
- Query parameters for optional modifiers: `?limit=10&offset=0`, `?overwrite=true`.
- Use `Annotated[type, Query(description=...)]` for documented query parameters.

## Versioning

- All endpoints are prefixed with `/v1`. Applied at the router level in `app.py`.
- See `docs/architecture/api-conventions.md` for full API conventions (error schema, request IDs, pagination, auth).
