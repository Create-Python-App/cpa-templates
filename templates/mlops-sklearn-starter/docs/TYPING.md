# Typing

The package uses pydantic v2 models and type hints throughout. Run:

```sh
uv run mypy .
uv run pyright
```

`sklearn`/`mlflow` third-party stubs are incomplete — see
`[[tool.mypy.overrides]]` in `pyproject.toml` for the modules where missing
imports are ignored.
