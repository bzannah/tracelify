"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from tracelify.app import create_app


@pytest.fixture
def client() -> TestClient:
    """Create a FastAPI test client."""
    app = create_app()
    return TestClient(app)
