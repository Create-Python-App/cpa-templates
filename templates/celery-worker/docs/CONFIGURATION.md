# Configuration

Settings live in `worker/config.py` (pydantic-settings) and load from the
environment / `.env`.

| Variable | Default (scaffold) | Purpose |
|----------|--------------------|---------|
| `BROKER_URL` | `redis://localhost:6379/0` | Celery broker |
| `RESULT_BACKEND` | `redis://localhost:6379/1` | Result store |
| `TASK_ALWAYS_EAGER` | `false` | Run tasks in-process (tests / local debug) |

Scaffold-time options in `cpa.config.json`:

| Option | Default | Description |
|--------|---------|-------------|
| `brokerUrl` | `redis://localhost:6379/0` | Written into config template |
| `resultBackend` | `redis://localhost:6379/1` | Written into config template |

## Celery conf highlights

Set in `worker/celery_app.py`:

- JSON serializers only
- UTC timezone
- `task_track_started=True`
- `task_always_eager` driven by settings

## Retries

Example: `worker.tasks.add` uses `autoretry_for=(ValueError,)`, `retry_backoff=True`,
and `max_retries=3`. Prefer the same pattern for I/O-bound work; use `bind=True`
when you need `self.retry(...)` / request metadata.

## Compatible extensions

- `celery-docker` — container image with worker CMD
- `postgres` — Compose Postgres (if you later store results / app state)
- `github-setup`, `development-container`
