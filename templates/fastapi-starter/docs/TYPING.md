# Typing

Typed Python is the **intended default** for projects generated from this starter. Prefer annotated public APIs, Pydantic models at boundaries, and CI type checks alongside Ruff and pytest.

This guide explains mypy vs pyright, how to enable them, and how to tighten over time — even if a given scaffold revision has not yet wired both tools into `pyproject.toml`.

## Goals

- Catch type errors before runtime
- Keep feature routers/services readable without sacrificing safety
- Match the quality bar of typed Create-Node-App starters (TypeScript strict)

## mypy vs pyright

| Tool | Strengths | Typical use |
|------|-----------|-------------|
| **mypy** | Mature ecosystem, gradual typing, rich plugins (Pydantic, etc.) | CI gate, library-style packages |
| **pyright** | Fast, excellent editor DX (Pylance), strict modes | Local feedback, optional second CI job |

Recommended approach for FastAPI apps:

1. Annotate application code under `app/` from day one.
2. Run **at least one** checker in CI (`mypy app` and/or `uv run pyright`).
3. Prefer **both** when the project is mature — they catch overlapping but not identical issues.

## Enabling mypy

```bash
uv add --dev mypy
```

Example `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
packages = ["app"]
warn_unused_ignores = true
```

```bash
uv run mypy app
```

Optional: `uv add --dev pydantic` plugins / `mypy` stubs as needed (`types-*` packages).

## Enabling pyright

```bash
uv add --dev pyright
```

Example:

```toml
[tool.pyright]
include = ["app"]
exclude = ["**/__pycache__", ".venv"]
pythonVersion = "3.12"
typeCheckingMode = "basic"   # start here; move to "strict"
```

```bash
uv run pyright
```

## How to tighten

1. **Start with `basic` / non-strict** if migrating a large untyped tree; keep new modules fully annotated.
2. Enable **`strict`** (mypy) or **`typeCheckingMode = "strict"`** (pyright) once the core package is clean.
3. Ban silent escapes: treat `# type: ignore` as temporary — require a comment with ticket/reason.
4. Prefer `TypedDict` / Pydantic models over `dict[str, Any]` at API edges.
5. Keep FastAPI route signatures concrete (`-> APIResponse[HealthStatus]`, not bare `dict`).

## CI commands

Suggested quality job steps (after `uv sync`):

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app          # when configured
uv run pyright           # when configured
uv run pytest
```

If only one type checker is configured, keep that one green rather than documenting both as mandatory in CI.

## FastAPI / Pydantic tips

- Use `pydantic.BaseModel` (or settings) for request/response bodies — they are already typed.
- Prefer `APIResponse[T]` generics from `app.schemas.common.responses`.
- Annotate service functions with return types so routers stay thin and checkable.
- Avoid importing `Any` in feature modules; if needed, isolate it behind a clearly typed adapter.

## Related docs

- [CONFIGURATION.md](./CONFIGURATION.md) — tool install and scripts
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) — runtime verification alongside types
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) — where typed modules live
