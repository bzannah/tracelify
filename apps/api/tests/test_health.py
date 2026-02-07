"""Tests for the health check endpoint."""

from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200


def test_health_returns_expected_fields(client: TestClient) -> None:
    data = client.get("/v1/health").json()
    assert "status" in data
    assert "service" in data
    assert "version" in data


def test_health_status_is_healthy(client: TestClient) -> None:
    data = client.get("/v1/health").json()
    assert data["status"] == "healthy"
    assert data["service"] == "tracelify-api"
