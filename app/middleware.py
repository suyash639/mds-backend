from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start_time = time.time()
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"}
            )
            await response(scope, receive, send)

class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        method = scope.get("method")
        path = scope.get("path")
        logger.info(f"{method} {path}")

        await self.app(scope, receive, send)
