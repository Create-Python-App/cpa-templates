"""Rate limit initialization helper (fastapi-rate-limit extension)."""

from __future__ import annotations

import os

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.schemas.common.responses import make_error_response


def _get_limiter() -> Limiter:
    """Initialize the SlowAPI limiter from environment configuration."""
    redis_url = os.getenv("RATE_LIMIT_REDIS_URL", "").strip()
    storage_uri = redis_url if redis_url else "memory://"

    enabled_str = os.getenv("RATE_LIMIT_ENABLED", "true").lower()
    enabled = enabled_str in ("1", "true", "yes", "on")

    default_limits = os.getenv("RATE_LIMIT_DEFAULT", "").strip()
    limits = [default_limits] if default_limits else []

    return Limiter(
        key_func=get_remote_address,
        storage_uri=storage_uri,
        default_limits=limits,
        enabled=enabled,
    )


limiter = _get_limiter()


def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Map rate limit exceptions to the standard CPA APIResponse envelope."""
    request_id = getattr(request.state, "request_id", "unknown")
    response = make_error_response(
        status_code=429,
        dev_code="RATE_LIMIT_EXCEEDED",
        message=f"Rate limit exceeded: {exc.detail}",
        request_id=request_id,
    )

    resp = JSONResponse(
        status_code=429,
        content=jsonable_encoder(response),
    )

    # Inject countdown headers (Retry-After, X-RateLimit-Reset, etc.)
    if hasattr(request.state, "view_rate_limit") and hasattr(request.app.state, "limiter"):
        resp = request.app.state.limiter._inject_headers(resp, request.state.view_rate_limit)

    return resp


def setup_rate_limit(app: FastAPI) -> None:
    """Register rate limiter state and exception handler on the FastAPI app."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
