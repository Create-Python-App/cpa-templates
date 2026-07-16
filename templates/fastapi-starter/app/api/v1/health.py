"""Health check routes."""

from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def health_check() -> dict[str, str]:
    """Service health endpoint."""
    return {
        "status": "healthy",
        "service": "fastapi-starter",
        "timestamp": datetime.now(UTC).isoformat(),
    }
