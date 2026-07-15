"""Middleware to inject correlation ID and request ID."""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request_id = str(uuid.uuid4())
        # Store in request state for later use
        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        # Inject into log records via filter
        class ContextFilter(logging.Filter):
            def filter(self, record):
                record.correlation_id = correlation_id
                record.request_id = request_id
                return True

        context_filter = ContextFilter()
        logger.addFilter(context_filter)

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Request-ID"] = request_id
        return response