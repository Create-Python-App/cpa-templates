# Deployment

## Local process

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

## Containers

Add the `django-docker` extension for `Dockerfile` + Compose (`runserver` locally, `gunicorn config.wsgi` in prod overlay).

Pair with `postgres` when you need a database service. Inside Compose, use hostname `db` instead of `localhost`.

## Checklist

- [ ] Set a strong `DJANGO_SECRET_KEY`
- [ ] `DJANGO_DEBUG=false` in production
- [ ] Restrict `DJANGO_ALLOWED_HOSTS`
- [ ] Run migrations before traffic
- [ ] Terminate TLS at the proxy / platform
