# Python Standards

## Version & Typing

- Target Python 3.9+. Use lowercase built-in generics: `list[str]`, `dict[str, int]`, `tuple[str, ...]`.
- Do not import `List`, `Dict`, `Tuple` from `typing`. Use `Optional[T]` for nullable types.
- Annotate all function signatures — parameters and return types.
- Test functions return `-> None`.

```python
# Yes
def get_chunks(doc_id: str, limit: int = 10) -> list[Chunk]:
def test_upload_rejects_pdf(client: TestClient) -> None:

# No
def get_chunks(doc_id, limit=10):
def test_upload_rejects_pdf(client):
```

## Formatting & Linting

- **ruff** is the only formatter and linter. Run `make lint` and `make format` before committing.
- No custom ruff config — use defaults. Do not add pylint, flake8, black, or isort.
- Import order: stdlib → third-party → local, separated by blank lines.

## Docstrings

- Every module starts with a one-line docstring: `"""Health check endpoint."""`
- Functions use Google-style docstrings. One-liner for simple functions, `Args:`/`Returns:` sections for functions with 2+ parameters.

```python
def chunk_text(text: str, doc_id: str, chunk_size: int = 500) -> list[Chunk]:
    """
    Split text into overlapping chunks.

    Args:
        text: The document text to chunk.
        doc_id: Unique identifier for the source document.
        chunk_size: Target number of characters per chunk.

    Returns:
        List of Chunk objects.
    """
```

## Data Modeling

- Use `@dataclass` for plain data containers. Use Pydantic `BaseModel` for API request/response schemas.
- Keep models close to where they're used. Don't create a monolithic `models.py` until there are 5+ shared models.

## Testing

- Tests live in `apps/api/tests/`. Mirror the source structure when the test suite grows (e.g., `tests/routers/test_health.py`).
- Test naming: `test_<unit>_<expected_behavior>`. Be specific.
- Fixtures go in `conftest.py`. The `client` fixture creates a fresh `TestClient` via `create_app()` — use it for all HTTP tests.
- Prefer plain `assert` statements over unittest methods.
- Each test should verify one behavior. Three focused tests beat one test with five asserts.

```python
# Yes
def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200

# No
def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "tracelify-api"
    assert "version" in response.json()
```

## Dependencies

- Add dependencies to `apps/api/pyproject.toml`, not the root.
- Dev-only dependencies (pytest, httpx, ruff) go in `[dependency-groups] dev`.
- Pin minimum versions (`>=`), not exact versions (`==`).
