"""Example Celery tasks."""

from __future__ import annotations

from worker.celery_app import app


@app.task(name="worker.tasks.add")
def add(left: int, right: int) -> int:
    """Return the sum of two integers."""
    return left + right


@app.task(name="worker.tasks.ping")
def ping() -> str:
    """Health-style probe task."""
    return "pong"
