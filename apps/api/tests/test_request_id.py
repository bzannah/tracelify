"""Tests for request ID middleware."""

from fastapi.testclient import TestClient


def test_response_includes_request_id_header(client: TestClient) -> None:
    response = client.get("/v1/health")
    assert "X-Request-ID" in response.headers


def test_generated_request_id_has_correct_format(client: TestClient) -> None:
    response = client.get("/v1/health")
    request_id = response.headers["X-Request-ID"]
    assert request_id.startswith("req_")
    assert len(request_id) == 16  # "req_" + 12 chars


def test_client_request_id_is_passed_through(client: TestClient) -> None:
    response = client.get("/v1/health", headers={"X-Request-ID": "req_myclient1234"})
    assert response.headers["X-Request-ID"] == "req_myclient1234"
