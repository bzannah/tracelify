"""Structured error handling for the Tracelify API."""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Individual error details."""

    code: str = Field(description="Machine-readable error code (snake_case)", examples=["document_not_found"])
    message: str = Field(description="Human-readable error description", examples=["No document found with ID 'my-doc'"])
    request_id: str = Field(description="Request ID for tracing", examples=["req_a1b2c3d4e5f6"])


class ErrorResponse(BaseModel):
    """Standard error response returned by all endpoints on failure."""

    error: ErrorDetail


class APIError(Exception):
    """Raise to return a structured error response."""

    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)
