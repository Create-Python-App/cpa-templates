"""Health check business logic."""

from __future__ import annotations


def get_health_status() -> dict[str, str]:
    return {"status": "healthy"}
