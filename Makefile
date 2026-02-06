.PHONY: help install test dev-db dev-api lint format db-down db-logs

help:
	@echo "Tracelify Development Commands"
	@echo ""
	@echo "  make install    Install all dependencies"
	@echo "  make dev-db     Start PostgreSQL (pgvector)"
	@echo "  make dev-api    Start the FastAPI dev server"
	@echo "  make test       Run all tests"
	@echo "  make lint       Run ruff linter"
	@echo "  make format     Format code with ruff"
	@echo ""
	@echo "  make db-down    Stop PostgreSQL"
	@echo "  make db-logs    Tail database logs"

install:
	uv sync --all-packages

dev-db:
	docker compose up -d

dev-api:
	cd apps/api && uv run uvicorn tracelify.app:app --reload --host 0.0.0.0 --port 8000

test:
	cd apps/api && uv run pytest -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

db-down:
	docker compose down

db-logs:
	docker compose logs -f db
