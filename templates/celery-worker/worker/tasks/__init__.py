"""Example Celery tasks package.

Add new modules under ``worker/tasks/`` and import them from
``worker.tasks`` so autodiscovery registers them.
"""

from __future__ import annotations

from worker.tasks.health import ping
from worker.tasks.math import add

__all__ = ["add", "ping"]
