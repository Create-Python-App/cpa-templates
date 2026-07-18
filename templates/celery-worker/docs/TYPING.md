# Typing

```bash
uv run mypy worker
uv run pyright
```

Annotate public task signatures. Celery/kombu imports are ignored in mypy via
`pyproject.toml` overrides when stubs are missing.
