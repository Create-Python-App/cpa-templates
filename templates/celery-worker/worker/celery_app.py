"""Celery application factory."""

from celery import Celery

from worker.config import settings

app = Celery(
    "celery_worker",
    broker=settings.broker_url,
    backend=settings.result_backend,
    include=["worker.tasks"],
)

app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_always_eager=settings.task_always_eager,
)
