"""FastAPI application factory for Tracelify."""

from fastapi import FastAPI

from tracelify.routers import health


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Tracelify API",
        description="Open-source RAG knowledge vault with chat",
        version="0.1.0",
    )
    app.include_router(health.router)
    return app


app = create_app()
