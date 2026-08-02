# CORS Guide

The **fastapi-cors** extension adds an easy way to configure Cross-Origin Resource Sharing (CORS) for your FastAPI application.

## Configuration

Set the `CORS_ORIGINS` environment variable in your `.env` file to a comma-separated list of allowed origins:

```env
CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

If `CORS_ORIGINS` is empty or not set, the middleware will not be registered.

## Wiring it up

Because middleware order matters, you must manually initialize CORS in `app/main.py`.

1. Import the helper at the top of `app/main.py`:

```python
from app.core.cors import setup_cors
```

2. Call it **after** all other `add_middleware` calls so that CORS is the
   outermost layer (FastAPI/Starlette applies middleware in LIFO order — the
   last one added is the first to handle each request):

```python
app = FastAPI(
    title=settings.app_name,
    # ...
)

app.add_middleware(RequestIDMiddleware)   # existing line
register_exception_handlers(app)         # existing line
setup_cors(app)                          # ← add after all middleware
```

Placing `setup_cors` before `RequestIDMiddleware` would wrap CORS inside
RequestID, meaning preflight `OPTIONS` requests would be processed by
RequestIDMiddleware before CORS could respond to them.

## Security Warning

Never use wildcard origins (`*`) in a production environment if your API requires authentication (`allow_credentials=True`), as this is rejected by modern browsers and constitutes a security risk. Always specify exact domains.
