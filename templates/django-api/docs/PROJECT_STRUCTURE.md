# Project structure

```
apps/
  health/                 # example feature app
    serializers.py
    services.py
    views.py
    urls.py
config/                   # Django project package (settings, urls, asgi/wsgi)
docs/
  examples/feature-app/   # copy-me scaffold (not installed)
manage.py
tests/
```

## Adding a feature

1. Copy `docs/examples/feature-app/` → `apps/<name>/`.
2. Set `name = "apps.<name>"` in `apps.py` and fix imports.
3. Register in `INSTALLED_APPS`.
4. Wire urls under `API_PREFIX` in `config/urls.py`.
5. Add tests; keep the `{data, error, meta}` envelope for JSON APIs.

## Conventions

- Business logic in `services.py`; HTTP in `views.py`; shapes in `serializers.py`.
- Do not put domain logic in `config/`.
- Prefer one Django app per bounded context.
