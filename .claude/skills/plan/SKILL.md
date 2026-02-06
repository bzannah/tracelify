---
name: plan
description: Create an implementation plan for a feature or task, referencing existing architecture and requirements docs.
---

# Plan a Feature

Create a structured implementation plan for a Tracelify feature or task.

## Steps

1. **Read the user's request** and identify which feature area it touches (ingestion, indexing, retrieval, chat, UI, governance).

2. **Load context** by reading these files:
   - `docs/product/requirements.md` — find the relevant feature (F1–F15) and its acceptance criteria.
   - `docs/architecture/overview.md` — identify which subsystems are involved and their boundaries.
   - `docs/adr/0001-tech-stack.md` — confirm the tech choices that apply.

3. **Explore the current code** in `apps/api/src/tracelify/` to understand:
   - What already exists that can be reused.
   - Which files will need changes.
   - What patterns are established (app factory, router structure, config centralization).

4. **Write the plan** with these sections:
   - **Context**: What problem this solves and why it's needed now.
   - **Scope**: What's in and out of scope for this change.
   - **Approach**: Step-by-step implementation with specific file paths for each file to create or modify.
   - **Data model**: Any new dataclasses, Pydantic schemas, or database tables.
   - **API changes**: New or modified endpoints with request/response shapes.
   - **Testing strategy**: What tests to write and what they verify.
   - **Open questions**: Anything that needs clarification before starting.

5. **Present the plan** to the user for approval before writing any code.

## Checklist

- [ ] Relevant requirements doc (F1–F15) identified and referenced
- [ ] Architecture subsystems and trust boundaries identified
- [ ] Existing code explored — no duplicate implementations proposed
- [ ] File paths listed for every file to create or modify
- [ ] Data models and API contracts defined
- [ ] Testing strategy included
- [ ] Open questions surfaced (if any)
- [ ] Plan presented for user approval before implementation
