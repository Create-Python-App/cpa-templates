# Rate Limiting Guide

This project uses [slowapi](https://slowapi.readthedocs.io/en/latest/) (a FastAPI port of Flask-Limiter) to protect endpoints from abuse.

## 1. Wiring the Rate Limiter

Because rate limiting often interacts with other middlewares (like CORS and Request IDs), this extension requires manual wiring into `app/main.py`.

Open `app/main.py`, import the setup function, and call it below your `app = FastAPI(...)` initialization:

```python
from app.core.rate_limit import setup_rate_limit

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    root_path=settings.api_prefix,
)

# Add this line:
setup_rate_limit(app)
```

## 2. Protecting Endpoints

To rate limit an endpoint, use the `@limiter.limit` decorator.

> [!WARNING]
> The decorator **strictly requires** your route handler function to accept the FastAPI `Request` object as a parameter, even if you do not use it in the function body. Without it, the route will crash.

```python
from fastapi import APIRouter, Request
from app.core.rate_limit import limiter

router = APIRouter()

@router.get("/sensitive-data")
@limiter.limit("5/minute")
async def sensitive_data(request: Request):
    return {"data": "This is protected"}
```

## 3. Production Edge Cases & Architecture

### The Multi-Worker Memory Trap
By default, the rate limiter uses an **in-memory** backend. Memory is strictly isolated per process. If you run Uvicorn/Gunicorn with multiple workers (e.g. `--workers 4`), a limit of `5/minute` actually allows `20/minute` across the cluster because each worker has its own independent memory bucket. 
**Fix:** For multi-worker or Kubernetes environments, you MUST uncomment and provide `RATE_LIMIT_REDIS_URL` in your `.env` file to synchronize rate limits globally.

### The Reverse Proxy "Global Ban" Trap
The rate limiter identifies clients by their IP address (`request.client.host`). If your application is deployed behind a Reverse Proxy, Load Balancer, or API Gateway (like NGINX, AWS ALB, or Cloudflare), the IP address will be the proxy's internal IP.
**Danger:** If the proxy IP is used, the rate limiter will instantly ban *all* users globally if traffic exceeds the limit.
**Fix:** Ensure your proxy forwards the `X-Forwarded-For` header, and ensure you run Uvicorn with `--proxy-headers` (or configure `ProxyHeadersMiddleware`) so FastAPI automatically trusts and parses the true client IP.

## 4. Disabling the Limiter
You can completely bypass the rate limiter during local testing or CI by setting `RATE_LIMIT_ENABLED=false` in your `.env`.

## 5. Why this extension uses an in-memory limiter by default

This extension intentionally defaults to an in-memory backend to keep the generated
project lightweight and dependency-free.

For production deployments using multiple workers or multiple instances,
memory-based rate limiting is no longer globally consistent because each process
maintains its own counters.

In those environments, use a shared backend such as Redis or move rate limiting
to an API Gateway.

This extension intentionally does not bundle Redis because CPA keeps extensions
modular. If Redis is required, compose this extension with the appropriate Redis
support rather than increasing the dependency footprint for every project.
