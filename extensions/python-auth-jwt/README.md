# Auth JWT (extension bank)

Maintainer-facing notes for the **python-auth-jwt** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `PyJWT[crypto]`, `pwdlib[argon2]`, and `email-validator` |
| `app/features/auth/` | Schemas, service helpers, demo `/auth` router |
| `.env.example.append` | `JWT_SECRET`, algorithm, expiry |
| `docs/AUTH_JWT_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-auth-jwt \
  --yes
```

## Verify after scaffold

```sh
uv sync
uv run python -c "from app.features.auth.service import create_access_token; print(create_access_token('a@b.co'))"
```

See `template/docs/AUTH_JWT_GUIDE.md` for full usage, configuration, and troubleshooting.
