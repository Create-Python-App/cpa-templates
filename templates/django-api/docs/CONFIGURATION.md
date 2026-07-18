# Configuration

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `DJANGO_SECRET_KEY` | `dev-only-change-me` | Django secret |
| `DJANGO_DEBUG` | `true` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts |

Scaffold option `apiPrefix` (default `/api/v1`) becomes `API_PREFIX` in settings.

## Tooling

| Tool | Command |
|------|---------|
| Ruff | `uv run ruff check .` |
| mypy | `uv run mypy apps config` |
| pyright | `uv run pyright` |
| pytest | `uv run pytest` |

## Database

Default is SQLite. With the `postgres` extension, add `psycopg` (merged via extension `pyproject.toml`) and point Django `DATABASES` (or a URL helper) at the Compose service hostname `db`.
