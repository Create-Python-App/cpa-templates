# Deployment

## Process model

Run one or more Celery worker processes against a shared broker:

```bash
uv run celery -A worker.celery_app worker --loglevel=INFO --concurrency=2
```

Add beat only when you introduce periodic schedules:

```bash
uv run celery -A worker.celery_app beat --loglevel=INFO
```

## Containers

Scaffold with the `celery-docker` extension for a Dockerfile that launches the
worker CMD. Pair with Redis (and optionally Postgres) via Compose.

## Production checklist

- [ ] Broker / backend URLs from secrets, not committed `.env`
- [ ] Concurrency and prefetch tuned for task mix
- [ ] Health: expose a probe task (`ping`) or process-level liveness
- [ ] Logs structured; avoid dumping PII in task args
- [ ] Graceful shutdown (`SIGTERM`) so in-flight tasks finish or requeue

## Observability

Wire metrics / Sentry at the Celery signal layer when you outgrow stdout logs.
Do not reuse FastAPI-only `fastapi-sentry` overlays on this stack without adapting
imports.
