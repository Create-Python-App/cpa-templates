"""Redis client helper (python-redis extension)."""

from __future__ import annotations

import os

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis() -> redis.Redis:
    """Return a response-decoded Redis client."""
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)
