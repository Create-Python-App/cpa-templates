# FastAPI Rate Limit Extension

Adds rate limiting using `slowapi` to a FastAPI project, with optional Redis backing for multi-worker environments.

## What this adds

- `app/core/rate_limit.py` | `setup_rate_limit()` helper that instantiates `Limiter` and maps 429 exceptions to standard CPA APIResponses.
- `docs/RATE_LIMIT_GUIDE.md` | Guide on how to configure and use the `@limiter.limit` decorator securely.
- `pyproject.toml` | Injects `slowapi` dependency via deep merge.

## Compatibility

- `fastapi-backend`

## How it works

This extension avoids blanket middleware by default, instead providing the `@limiter.limit("5/minute")` decorator for granular endpoint control. It gracefully defaults to in-memory limiting, but allows seamless upgrade to Redis via environment variables.
