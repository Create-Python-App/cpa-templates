# Celery Worker docs

- Unit tests run with `task_always_eager=True` so CI does not need Redis.
- For local/runtime checks, start Redis and run the worker process.
- Add new tasks in `worker/tasks.py` and include modules via `celery_app.py`.
