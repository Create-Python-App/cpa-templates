# Testing guide

Unit tests run **without Redis** via Celery eager mode.

## How it works

`tests/conftest.py` sets:

```python
app.conf.task_always_eager = True
app.conf.task_eager_propagates = True
```

Calls like `add.delay(2, 3).get()` execute in-process and raise errors immediately.

## Commands

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy worker
```

## Integration smoke (optional)

With Redis running:

```bash
uv run celery -A worker.celery_app worker --loglevel=INFO
# another shell
uv run python -c "from worker.tasks import ping; print(ping.delay().get(timeout=5))"
```

## What to cover

- Happy path for each public task
- Failure / validation cases when you add retries or soft time limits
- Avoid asserting on broker transport details in unit tests
