"""Health / probe tasks."""

from __future__ import annotations

from worker.celery_app import app


@app.task(name="worker.tasks.ping")
def ping() -> str:
    """Health-style probe task."""
    return "pong"
