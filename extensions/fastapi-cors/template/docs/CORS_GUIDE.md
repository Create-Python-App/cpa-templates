# CORS Guide

The **fastapi-cors** extension adds CORS (Cross-Origin Resource Sharing) middleware to your FastAPI application.

## How it works

CORS is wired automatically at scaffold time — no edits to `app/main.py` are needed. The extension registers `setup_cors` as the last provider in `app/core/providers.py`, which ensures it becomes the outermost middleware layer (FastAPI applies middleware in LIFO order — last registered = first to execute on each request). This guarantees preflight `OPTIONS` requests are handled by CORS before any other middleware.

## Configuration

Set the `CORS_ORIGINS` environment variable in your `.env` file to a comma-separated list of allowed origins:

```env
CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

If `CORS_ORIGINS` is empty or not set, the middleware is not registered — local development stays unrestricted until you opt in.

## Security Warning

Never use wildcard origins (`*`) with `allow_credentials=True`. This is rejected by modern browsers and constitutes a security risk. Always specify exact domains in `CORS_ORIGINS`.

## Verification

```sh
uv sync
CORS_ORIGINS="http://localhost:3000" uv run uvicorn app.main:app --port 8001 &
curl -s -H "Origin: http://localhost:3000" -I http://localhost:8001/ping 2>&1 | grep -i "access-control"
```

You should see `Access-Control-Allow-Origin: http://localhost:3000` in the response headers.

## Resources

- [FastAPI CORS middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
