# Security Standards

## Secrets & Credentials

- **Never log, print, or return API keys, database passwords, or tokens.** Not in error messages, not in debug output, not in HTTP responses.
- All secrets load from environment variables via `config.py`. Never hardcode secrets anywhere.
- The `.env` file is gitignored. Only `.env.example` is committed, and it must contain placeholder values only.

```python
# Yes
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# No
OPENAI_API_KEY = "sk-abc123..."
logger.info(f"Using key: {OPENAI_API_KEY}")
```

- If a function needs an API key, accept it as a parameter or read from `config`. Never import `os.getenv` in multiple files — centralize in `config.py`.

## File Handling

- **Never construct file paths from user input directly.** Use `Path.stem` or a sanitization function to derive safe identifiers.
- Validate file extensions against an allowlist before processing. The MVP allows `.txt` and `.md` only.
- Enforce file size limits before reading content into memory.
- Store uploaded files in `DATA_DIR` (from `config.py`). Never write outside this directory based on user-provided paths.

```python
# Yes — safe: fixed parent directory, filename derived from Path
save_path = DATA_DIR / uploaded_file.filename

# No — path traversal risk
save_path = Path(user_provided_path)
```

## Database

- Use parameterized queries or SQLAlchemy ORM. Never interpolate user input into SQL strings.
- Database credentials come from `DATABASE_URL` in `.env`. Never log connection strings.

## Prompt Injection Defense

- Retrieved document chunks are **untrusted data**. Always wrap them in explicit delimiters when constructing LLM prompts.
- The system prompt must instruct the model to treat chunk content as reference data, never as instructions.
- Never pass raw user input as the system prompt.

```python
# Yes — chunks are delimited and clearly marked as data
prompt = f"""Answer based only on the following context:

<retrieved_chunk id="{chunk.id}">
{chunk.text}
</retrieved_chunk>

Question: {user_question}"""

# No — chunks mixed directly into instructions
prompt = f"You are a helpful assistant. {chunk.text}. Answer: {user_question}"
```

## Error Responses

- Return generic error messages to clients. Log detailed errors server-side.
- Never expose stack traces, file paths, database schemas, or internal configuration in HTTP responses.

```python
# Yes
raise HTTPException(status_code=500, detail="Internal server error")

# No
raise HTTPException(status_code=500, detail=f"DB error: {e} at {connection_string}")
```
