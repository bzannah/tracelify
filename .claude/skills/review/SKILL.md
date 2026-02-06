---
name: review
description: Review code changes for correctness, security, and adherence to project standards.
---

# Review Code

Review staged or recent code changes against Tracelify's project standards.

## Steps

1. **Identify what changed.** Run `git diff --staged` (or `git diff HEAD~1` for the last commit). Read every changed file in full.

2. **Check Python standards** (`.claude/rules/python.md`):
   - All functions have type annotations (parameters and return types).
   - Docstrings present on modules, classes, and public functions (Google style).
   - Imports ordered: stdlib → third-party → local.
   - `list[T]`, `dict[K,V]`, `tuple[...]` used (not `typing.List` etc.).
   - Tests follow `test_<unit>_<behavior>` naming with `-> None`.

3. **Check security standards** (`.claude/rules/security.md`):
   - No secrets hardcoded or logged.
   - File paths not constructed from raw user input.
   - SQL uses parameterized queries or ORM (never string interpolation).
   - LLM prompts wrap retrieved chunks in delimiters.
   - Error responses don't expose internals (stack traces, file paths, DB details).

4. **Check API standards** (`.claude/rules/api.md`):
   - New endpoints are `async def` with explicit return types.
   - Request/response shapes use Pydantic models (not raw dicts).
   - Errors use `HTTPException` with correct status codes.
   - New routers registered in `create_app()` with `tags`.

5. **Check architecture alignment**:
   - Changes respect subsystem boundaries from `docs/architecture/overview.md`.
   - No subsystem reaches into another's internals (e.g., chat doesn't write to the vector store directly).
   - New config values added to `config.py` and `.env.example`.

6. **Check test coverage**:
   - New endpoints have corresponding tests in `apps/api/tests/`.
   - Tests use the `client` fixture from `conftest.py`.
   - Edge cases covered (empty input, invalid file type, missing resource).

7. **Write the review** with:
   - **Summary**: One sentence on what the change does.
   - **Issues**: Numbered list of problems, each with file path, line reference, and suggested fix.
   - **Suggestions**: Optional improvements (not blocking).
   - **Verdict**: Approve, request changes, or needs discussion.

## Checklist

- [ ] All changed files read in full
- [ ] Python standards verified (types, docstrings, imports)
- [ ] Security standards verified (no secrets, safe file handling, safe SQL, safe prompts)
- [ ] API standards verified (async, Pydantic schemas, error format)
- [ ] Architecture boundaries respected
- [ ] Tests exist for new functionality
- [ ] Review written with issues, suggestions, and verdict
