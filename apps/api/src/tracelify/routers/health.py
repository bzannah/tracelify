"""Health check endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Service health status", examples=["healthy"])
    service: str = Field(description="Service name", examples=["tracelify-api"])
    version: str = Field(description="API version", examples=["0.1.0"])


router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API health",
    responses={200: {"description": "API is healthy and accepting requests"}},
)
async def health_check() -> HealthResponse:
    """Return the current health status of the Tracelify API.

    This endpoint does not require authentication and is intended for
    load balancers, uptime monitors, and readiness probes.
    """
    return HealthResponse(
        status="healthy",
        service="tracelify-api",
        version="0.1.0",
    )
