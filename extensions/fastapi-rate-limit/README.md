# FastAPI Rate Limit Extension

Adds rate limiting using `slowapi` to a FastAPI project, with optional Redis backing for multi-worker environments.

## What this adds

| Path | Purpose |
|------|---------|
| `app/core/rate_limit.py` | `setup_rate_limit()` + `limiter` instance + 429 exception handler |
| `app/core/providers.py.append.template` | Auto-registers `setup_rate_limit` in the app provider registry |
| `pyproject.toml` | Merges `slowapi` dependency |
| `.env.example.append` | `RATE_LIMIT_ENABLED`, `RATE_LIMIT_DEFAULT`, `RATE_LIMIT_REDIS_URL` |
| `docs/RATE_LIMIT_GUIDE.md` | Configuration and `@limiter.limit` usage guide |
| `docs/README.md.append` | Index bullet for `docs/README.md` |
| `tests/test_rate_limit.py` | Unit tests for the rate limit handler |

## Compatibility

- `fastapi-backend`

## How it works

`setup_rate_limit` is registered automatically in `app/core/providers.py` via the `.append.template` mechanism — no changes to `app/main.py` are needed.

The extension provides the `@limiter.limit("5/minute")` decorator for granular per-endpoint control, and gracefully defaults to in-memory storage with seamless upgrade to Redis via `RATE_LIMIT_REDIS_URL`.

## Apply

```sh
CI=true uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-rate-limit \
  --no-interactive
```

## Verify after scaffold

```sh
uv sync
uv run pytest
```

See `template/docs/RATE_LIMIT_GUIDE.md` for full configuration and `@limiter.limit` usage.
