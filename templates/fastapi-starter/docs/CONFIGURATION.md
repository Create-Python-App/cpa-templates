# Configuration

How to configure a project generated from `fastapi-starter`: environment variables, tooling, and common scripts.

## Environment variables

Copy `.env.example` to `.env` (never commit real secrets).

| Variable | Typical default | Purpose |
|----------|-----------------|---------|
| `API_PREFIX` | `/api/v1` | URL prefix for the composed API router |
| `ENABLE_CORS` | `true` / scaffold-dependent | Toggle CORS when settings read this flag |
| App-specific keys | — | Add in `app/core/config.py` (Pydantic Settings) and document here |

Scaffold-time options from `cpa.config.json` bake defaults into generated files:

| Option | Default | Effect |
|--------|---------|--------|
| `apiPrefix` | `/api/v1` | Mounted API prefix in `app/main.py` / settings |
| `enableCors` | `true` | Whether CORS middleware is registered |

Override at generation time with `--set apiPrefix=/api --set enableCors=false`.

## uv

```bash
uv sync                 # install project + dependency groups
uv sync --frozen        # CI / reproducible (requires lockfile)
uv sync --no-dev        # runtime-only
uv add <pkg>            # add runtime dependency
uv add --dev <pkg>      # add tool / test dependency
uv lock                 # refresh lockfile
```

Prefer committing `uv.lock` once the project is ready for reproducible CI.

## Ruff

Configured in `pyproject.toml` under `[tool.ruff]` / `[tool.ruff.lint]`.

```bash
uv run ruff check .              # lint
uv run ruff check . --fix        # lint + autofix
uv run ruff format .             # format
uv run ruff format --check .     # CI-friendly format check
```

## mypy

Intended static checker for gradual / strict Python typing. Typical setup:

```toml
[dependency-groups]
dev = [
  # ...
  "mypy>=1.13",
]

[tool.mypy]
python_version = "3.12"
strict = true
packages = ["app"]
```

```bash
uv run mypy app
```

See [TYPING.md](./TYPING.md) for how to introduce and tighten mypy.

## pyright

Complementary (or alternative) checker, often preferred in editor / CI for speed:

```toml
[dependency-groups]
dev = [
  # ...
  "pyright>=1.1",
]

[tool.pyright]
include = ["app"]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

```bash
uv run pyright
```

## Scripts cheat sheet

| Goal | Command |
|------|---------|
| Dev server | `uv run uvicorn app.main:app --reload` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Types (mypy) | `uv run mypy app` |
| Types (pyright) | `uv run pyright` |
| Tests | `uv run pytest` |
| Coverage | `uv run pytest --cov=app --cov-report=term-missing` |

## Related docs

- [TYPING.md](./TYPING.md) — mypy vs pyright strategy
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) — pytest patterns
- [DEPLOYMENT.md](./DEPLOYMENT.md) — production env and probes
