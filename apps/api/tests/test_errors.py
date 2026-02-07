"""Tests for structured error handling."""

from fastapi import APIRouter
from fastapi.testclient import TestClient

from tracelify.app import create_app
from tracelify.errors import APIError


def _create_client_with_error_route() -> TestClient:
    """Create a test client with a route that raises APIError."""
    app = create_app()
    error_router = APIRouter()

    @error_router.get("/v1/fail")
    async def fail_endpoint() -> None:
        raise APIError(404, "document_not_found", "No document found with ID 'test'")

    app.include_router(error_router)
    return TestClient(app)


def test_api_error_returns_correct_status_code() -> None:
    client = _create_client_with_error_route()
    response = client.get("/v1/fail")
    assert response.status_code == 404


def test_api_error_returns_structured_json() -> None:
    client = _create_client_with_error_route()
    data = client.get("/v1/fail").json()
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "request_id" in data["error"]


def test_api_error_contains_correct_values() -> None:
    client = _create_client_with_error_route()
    error = client.get("/v1/fail").json()["error"]
    assert error["code"] == "document_not_found"
    assert error["message"] == "No document found with ID 'test'"
    assert error["request_id"].startswith("req_")


def test_api_error_includes_client_request_id() -> None:
    client = _create_client_with_error_route()
    response = client.get(
        "/v1/fail", headers={"X-Request-ID": "req_clienterr123"}
    )
    error = response.json()["error"]
    assert error["request_id"] == "req_clienterr123"
