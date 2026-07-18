# Project structure

```
worker/
  __init__.py
  celery_app.py          # Celery application + conf
  config.py              # pydantic-settings (from env / .env)
  tasks/
    __init__.py          # re-exports registered tasks
    health.py            # probe tasks (ping)
    math.py              # example compute tasks (add)
tests/
  conftest.py            # eager-mode autouse fixture
  test_tasks.py
docs/                    # this documentation suite
.env.example             # broker / backend defaults
pyproject.toml
```

## Adding a task module

1. Create `worker/tasks/<domain>.py` with `@app.task(...)` functions.
2. Import the new symbols from `worker/tasks/__init__.py` (or rely on
   `include=["worker.tasks"]` plus side-effect imports).
3. Add tests under `tests/` that call `.delay(...).get()` (eager in CI).
4. Document retries / routing in CONFIGURATION.md when introducing new patterns.

## Conventions

- Task names use a stable dotted path (`worker.tasks.<name>`).
- Keep business logic in plain functions; wrap with `@app.task` at the edge.
- Do not put Redis/broker I/O in unit tests — use eager mode.
