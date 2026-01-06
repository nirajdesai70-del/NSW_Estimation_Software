"""
Request ID Middleware

Generates a UUIDv4 request_id for every request and stores it on request.state.
Also returns it in the X-Request-ID response header.
"""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Generates a UUIDv4 request_id for every request and stores it on request.state.
    Also returns it in the X-Request-ID response header.
    
    If client sends X-Request-ID, we reuse it (helps tracing across systems).
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response

