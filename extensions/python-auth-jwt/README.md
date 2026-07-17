# Auth JWT

JWT + password hashing skeleton for FastAPI starters.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `PyJWT[crypto]` + `pwdlib[argon2]` |
| `app/features/auth/` | Schemas, service helpers, demo `/auth` router |
| `.env.example.append` | `JWT_SECRET`, algorithm, expiry |

## Wire-up

Include the router from `app/api/router.py` (or equivalent):

```python
from app.features.auth.router import router as auth_router

api_router.include_router(auth_router)
```

Replace the in-memory demo user before production use.

## Verification

```sh
uv run python -c "from app.features.auth.service import create_access_token; print(create_access_token('a@b.co'))"
```
