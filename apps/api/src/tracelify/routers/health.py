"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Return API health status."""
    return {
        "status": "healthy",
        "service": "tracelify-api",
        "version": "0.1.0",
    }
