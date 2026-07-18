# Docker guide (Celery)

## Overview

The **celery-docker** extension packages the Celery worker for local and
production-style containers, including a Redis broker service.

## What it adds

- `Dockerfile` — Python 3.12 + uv; copies `worker/`; runs Celery worker
- `compose.yml` / `compose.prod.yml` — `redis` + `worker` services
- Env overrides in Compose: `BROKER_URL` / `RESULT_BACKEND` point at the
  `redis` service (not `localhost`)

These names match `worker/config.py` (pydantic-settings fields `broker_url` /
`result_backend`). Do **not** use `CELERY_BROKER_URL` unless you also rename the
settings fields.

## Usage

```sh
docker compose up --build
```

## Verification

1. `docker compose up --build`
2. Confirm Redis is healthy and the worker log shows it is ready
3. Enqueue a task (another shell / one-off container):

```sh
docker compose exec worker uv run python -c \
  "from worker.tasks import ping; print(ping.delay().get(timeout=10))"
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Cannot connect to Redis | Use `redis://redis:6379/0` inside Compose (service name), not `localhost` |
| Import errors for `worker` | Confirm `COPY worker` matches the template layout |
| Wrong env var name | Template reads `BROKER_URL` / `RESULT_BACKEND` |

## Resources

- [Celery first steps](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
