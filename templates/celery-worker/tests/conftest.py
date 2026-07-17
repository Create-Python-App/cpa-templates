"""Configure Celery for eager in-process tests (no broker required)."""

import pytest

from worker.celery_app import app


@pytest.fixture(autouse=True)
def _celery_eager() -> None:
    app.conf.task_always_eager = True
    app.conf.task_eager_propagates = True
