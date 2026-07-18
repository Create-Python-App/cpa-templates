"""Math-related tasks."""

from __future__ import annotations

from worker.celery_app import app


@app.task(
    name="worker.tasks.add",
    autoretry_for=(ValueError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def add(left: int, right: int) -> int:
    """Return the sum of two integers (retries on ValueError for demo)."""
    if not isinstance(left, int) or not isinstance(right, int):
        raise ValueError("add expects integers")
    return left + right
