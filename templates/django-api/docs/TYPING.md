# Typing

This starter ships **mypy** (with `django-stubs` / `djangorestframework-stubs`) and
**pyright**.

```bash
uv run mypy apps config
uv run pyright
```

## Conventions

- Annotate public view methods and service functions
- Prefer concrete serializer fields over untyped `dict` at API boundaries
- Avoid unjustified `# type: ignore`

See also FastAPI starter `docs/TYPING.md` for the shared CPA typed-Python bar.
