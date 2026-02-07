"""Request ID middleware for the Tracelify API."""

import secrets
import string

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"
_ALPHABET = string.ascii_lowercase + string.digits


def _generate_request_id() -> str:
    """Generate a request ID in the format req_<12 alphanumeric chars>."""
    suffix = "".join(secrets.choice(_ALPHABET) for _ in range(12))
    return f"req_{suffix}"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a request ID to every request and include it in the response."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or _generate_request_id()
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
