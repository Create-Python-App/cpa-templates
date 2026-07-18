# Testing Guide

Uses **pytest-django** with `DJANGO_SETTINGS_MODULE=config.settings`.

## Patterns

- Prefer `APIClient` for DRF views.
- Keep feature tests close to behaviour (status codes + envelope keys).
- Use eager, isolated DB — default SQLite is fine for unit tests.

## Commands

```bash
uv run pytest
uv run pytest -k healthz
```
