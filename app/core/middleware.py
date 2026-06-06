import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.security import decode_token

logger = logging.getLogger("user_actions")


class UserActionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        username = "anonymous"

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            payload = decode_token(auth_header[7:])
            if payload:
                username = payload.get("sub", "anonymous")

        response = await call_next(request)
        duration = time.time() - start_time
        client_host = request.client.host if request.client else "unknown"

        logger.info(
            "user=%s method=%s path=%s status=%s duration=%.3fs ip=%s",
            username,
            request.method,
            request.url.path,
            response.status_code,
            duration,
            client_host,
        )
        return response
