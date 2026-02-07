"""FastAPI application factory for Tracelify."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from tracelify.errors import APIError
from tracelify.middleware import RequestIDMiddleware
from tracelify.routers import health


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Tracelify API",
        description=(
            "Open-source RAG knowledge vault with chat. "
            "Upload documents, ask questions, and get cited answers.\n\n"
            "All endpoints are prefixed with `/v1`. "
            "Every response includes an `X-Request-ID` header for tracing."
        ),
        version="0.1.0",
        openapi_tags=[
            {
                "name": "Health",
                "description": "Liveness and readiness checks. No authentication required.",
            },
            {
                "name": "Documents",
                "description": "Upload, list, and delete documents in the knowledge vault.",
            },
            {
                "name": "Chat",
                "description": "Ask questions and get answers with citations from ingested documents.",
            },
        ],
    )

    app.add_middleware(RequestIDMiddleware)

    app.include_router(health.router, prefix="/v1")

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """Return structured error responses for APIError exceptions."""
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "request_id": request_id,
                }
            },
        )

    return app


app = create_app()
