# Sentry (extension bank)

Maintainer-facing notes for the **fastapi-sentry** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `sentry-sdk[fastapi]` into project dependencies |
| `app/core/sentry.py` | `init_sentry()` helper (no-op without `SENTRY_DSN`) |
| `.env.example.append` | `SENTRY_DSN`, sample rate, environment |
| `docs/SENTRY_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-sentry \
  --yes
```

## Verify after scaffold

```sh
uv sync
uv run python -c "from app.core.sentry import init_sentry; init_sentry()"
```

See `template/docs/SENTRY_GUIDE.md` for full usage, configuration, and troubleshooting.
