# FastAPI CORS Extension

Adds CORS (Cross-Origin Resource Sharing) middleware configuration to a FastAPI project. 

## What this adds

- `app/core/cors.py` | `setup_cors()` helper that reads `CORS_ORIGINS` from the environment.
- `docs/CORS_GUIDE.md` | Guide on how to configure and use CORS.

## Compatibility

- `fastapi-backend`

## How it works

This extension does not automatically inject middleware into `main.py` to ensure deterministic ordering. Instead, it provides the helper and instructions to wire it up manually in two lines of code, following the `fastapi-sentry` pattern.
