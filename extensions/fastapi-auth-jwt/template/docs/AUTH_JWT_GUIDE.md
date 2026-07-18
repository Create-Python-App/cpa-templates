# Auth JWT Guide

## Overview

The **fastapi-auth-jwt** extension adds a JWT + password-hashing skeleton for FastAPI starters: Pydantic schemas, `pwdlib` (Argon2) helpers, PyJWT encode/decode, and a demo `/auth` router with an in-memory user.

Replace the demo user and secret before any production use.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `PyJWT[crypto]`, `pwdlib[argon2]`, and `email-validator` |
| `app/features/auth/schemas.py` | `LoginRequest`, `TokenResponse`, `UserPublic` |
| `app/features/auth/service.py` | Hash/verify password; create/decode access tokens |
| `app/features/auth/router.py` | Demo `POST /auth/login` and `GET /auth/me` |
| `.env.example.append` | `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES` |

## Usage

### Mount the router

Include the router from `app/api/router.py` (or equivalent):

```python
from app.features.auth.router import router as auth_router

api_router.include_router(auth_router)
```

### Demo credentials

The scaffolded router uses:

- Email: `demo@example.com`
- Password: `password123`

Issue a token:

```sh
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"demo@example.com","password":"password123"}'
```

### Service helpers

```python
from app.features.auth.service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
```

## Configuration

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `JWT_SECRET` | `change-me` | **Must** change for any shared/deployed environment |
| `JWT_ALGORITHM` | `HS256` | Prefer asymmetric algorithms for multi-service setups |
| `JWT_EXPIRE_MINUTES` | `60` | Access-token lifetime |

## Verification

1. `uv run python -c "from app.features.auth.service import create_access_token; print(create_access_token('a@b.co'))"` prints a JWT.
2. After mounting the router, `POST /auth/login` with the demo user returns `access_token`.
3. Invalid credentials return HTTP 401.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `401 Invalid credentials` | Wrong demo email/password | Use `demo@example.com` / `password123` or replace the store |
| Token decode fails | Secret/algorithm mismatch | Align `JWT_SECRET` and `JWT_ALGORITHM` across encode/decode |
| Router 404 | Not included in API router | `include_router(auth_router)` under your API prefix |
| Weak secret in production | Left default `change-me` | Generate a long random secret; store in a secret manager |

## Resources

- [PyJWT documentation](https://pyjwt.readthedocs.io/)
- [pwdlib](https://github.com/frankie567/pwdlib)
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/)
