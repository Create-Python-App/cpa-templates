# Sentry

Adds `sentry-sdk[fastapi]` and a small `init_sentry()` helper.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sentry-sdk[fastapi]` |
| `app/core/sentry.py` | No-op unless `SENTRY_DSN` is set |
| `.env.example.append` | `SENTRY_DSN`, sample rate, environment |

## Wire-up

Call once during app startup (for example in `app/main.py`):

```python
from app.core.sentry import init_sentry

init_sentry()
```

## Verification

1. With empty `SENTRY_DSN`, `init_sentry()` is a no-op.
2. `uv run python -c "from app.core.sentry import init_sentry; init_sentry()"`
