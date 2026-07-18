# Docker guide (Django)

## Overview

The **django-docker** extension adds a reproducible container workflow for Django + DRF APIs. Compose files follow Create-Node-App naming: **`compose.yml`** / **`compose.prod.yml`**.

## What it adds

- `Dockerfile` — Python 3.12 + uv; copies `manage.py`, `config/`, `apps/`; runs `gunicorn config.wsgi`
- `compose.yml` — local `runserver` with bind mount
- `compose.prod.yml` — `gunicorn` without reload

## Usage

```sh
docker compose up --build
curl -s http://localhost:8000/api/healthz/
```

Production-style:

```sh
docker compose -f compose.prod.yml up --build -d
```

## Configuration

| Variable | Purpose |
|----------|---------|
| `.env` | Loaded by Compose (`env_file`) |
| `DATABASE_URL` / Django `DATABASES` | Wire via settings; use hostname `db` when stacked with `postgres` |

## Verification

1. `docker compose up --build`
2. Hit `/api/healthz/`
3. `docker compose down`

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Module not found `apps` | Ensure Dockerfile `COPY apps` matches project layout |
| DB connection refused | Use Compose service hostname, not `localhost`, inside containers |

## Resources

- [Docker Compose](https://docs.docker.com/compose/)
- [Gunicorn](https://docs.gunicorn.org/)
