# Sentry Guide

## Overview

The **python-sentry** extension adds `sentry-sdk[fastapi]` and a small `init_sentry()` helper. Initialization is a **no-op** when `SENTRY_DSN` is empty, so local development stays quiet until you opt in.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sentry-sdk[fastapi]>=2.19.0` |
| `app/core/sentry.py` | `init_sentry()` with FastAPI and Starlette integrations |
| `.env.example.append` | `SENTRY_DSN`, traces sample rate, environment |

## Usage

Call once during app startup (for example in `app/main.py`):

```python
from app.core.sentry import init_sentry

init_sentry()
```

Then create the FastAPI app as usual. With an empty DSN, nothing is sent to Sentry.

### Enable in a real environment

1. Create a Sentry project and copy the DSN.
2. Set `SENTRY_DSN` in `.env` (never commit secrets).
3. Optionally raise `SENTRY_TRACES_SAMPLE_RATE` (for example `0.1`) in staging/production.
4. Restart the API and trigger an error or transaction.

## Configuration

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `SENTRY_DSN` | empty | Leave blank to disable |
| `SENTRY_TRACES_SAMPLE_RATE` | `0.0` | `0.0`–`1.0` performance sampling |
| `SENTRY_ENVIRONMENT` | `development` | e.g. `staging`, `production` |

## Verification

1. With empty `SENTRY_DSN`, `uv run python -c "from app.core.sentry import init_sentry; init_sentry()"` exits 0 and sends nothing.
2. `uv run python -c "import sentry_sdk"` succeeds after `uv sync`.
3. With a real DSN, raise a test exception in a request and confirm the event in the Sentry UI.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| No events in Sentry | Empty/wrong DSN | Set `SENTRY_DSN`; restart the process |
| Too much noise locally | DSN set in `.env` | Clear `SENTRY_DSN` for local work |
| Missing FastAPI transactions | `init_sentry()` never called | Call it before serving requests |
| High quota usage | Sample rate too high | Lower `SENTRY_TRACES_SAMPLE_RATE` |

## Resources

- [Sentry Python SDK](https://docs.sentry.io/platforms/python/)
- [FastAPI integration](https://docs.sentry.io/platforms/python/integrations/fastapi/)
