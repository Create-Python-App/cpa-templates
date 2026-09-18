# Rate Limiting Guide

This project uses [slowapi](https://slowapi.readthedocs.io/en/latest/) (a FastAPI port of Flask-Limiter) to protect endpoints from abuse.

## How it works

Rate limiting is configured automatically at scaffold time — no edits to `app/main.py` are needed. The extension registers `setup_rate_limit` in `app/core/providers.py` via the CPA auto-wiring mechanism; `app/main.py` calls `setup_app(app)` which runs all registered providers at startup.

## Protecting Endpoints

To rate limit an endpoint, use the `@limiter.limit` decorator.

> [!WARNING]
> The decorator **strictly requires** your route handler to accept the FastAPI `Request` object as a parameter, even if you don't use it in the body. Without it, the route will crash.

```python
from fastapi import APIRouter, Request
from app.core.rate_limit import limiter

router = APIRouter()

@router.get("/sensitive-data")
@limiter.limit("5/minute")
async def sensitive_data(request: Request):
    return {"data": "This is protected"}
```

## Production Edge Cases

### The Multi-Worker Memory Trap

By default, the rate limiter uses an **in-memory** backend. Memory is strictly isolated per process. If you run Uvicorn/Gunicorn with multiple workers (e.g. `--workers 4`), a limit of `5/minute` actually allows `20/minute` across the cluster because each worker has its own independent counter.

**Fix:** Set `RATE_LIMIT_REDIS_URL` in `.env` to synchronize rate limits globally across workers.

### The Reverse Proxy "Global Ban" Trap

The rate limiter identifies clients by their IP address (`request.client.host`). Behind a reverse proxy (NGINX, AWS ALB, Cloudflare), this is the proxy's internal IP — meaning all users share the same bucket.

**Fix:** Ensure your proxy forwards the `X-Forwarded-For` header and run Uvicorn with `--proxy-headers` so FastAPI parses the true client IP.

## Disabling the Limiter

Set `RATE_LIMIT_ENABLED=false` in `.env` to bypass rate limiting during local testing or CI.

## Why in-memory by default

This extension defaults to in-memory storage to keep the generated project lightweight. For multi-worker or multi-instance deployments, use `RATE_LIMIT_REDIS_URL` to point to a shared Redis instance, or move rate limiting to an API Gateway. Redis support is intentionally not bundled — compose with the `fastapi-redis` extension if needed.
