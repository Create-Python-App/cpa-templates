# FastAPI CORS Extension

Adds CORS (Cross-Origin Resource Sharing) middleware to a FastAPI project.

## What this adds

| Path | Purpose |
|------|---------|
| `app/core/cors.py` | `setup_cors()` — registers `CORSMiddleware` when `CORS_ORIGINS` is set |
| `app/core/providers.py.append.template` | Auto-registers `setup_cors` in the app provider registry |
| `.env.example.append` | `CORS_ORIGINS` placeholder |
| `docs/CORS_GUIDE.md` | Configuration guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

## Compatibility

- `fastapi-backend`

## How it works

`setup_cors` is registered automatically in `app/core/providers.py` via the `.append.template` mechanism. No changes to `app/main.py` are needed.

CORS is registered last in the provider chain so it becomes the outermost middleware layer — consistent with FastAPI's LIFO `add_middleware` execution order and correct preflight handling.

## Apply

```sh
CI=true uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-cors \
  --no-interactive
```

## Verify after scaffold

```sh
uv sync
uv run pytest
```

See `template/docs/CORS_GUIDE.md` for full configuration and troubleshooting.
