# CPA Templates

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.12+-green.svg)
[![Discord](https://img.shields.io/discord/1527933660764831825?label=Discord&logo=discord&logoColor=white)](https://discord.gg/bR5VyATgka)

Official templates and extensions for [create-awesome-python-app](https://github.com/Create-Python-App/create-python-app).

## Quick start

Scaffold locally with the CLI:

```sh
# Interactive mode
uvx create-awesome-python-app

# With template and extensions
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons github-setup fastapi-docker
```

For local development against this checkout:

```sh
CI=true uvx create-awesome-python-app my-api \
  --template "file://$PWD?subdir=templates/fastapi-starter" \
  --no-interactive
```

## Available templates

| Template | Type | Use case |
|----------|------|----------|
| [fastapi-starter](./templates/fastapi-starter) | `fastapi-backend` | Production-ready FastAPI API with feature-based layout, uv, Ruff, pytest, mypy, and pyright |
| [cli-starter](./templates/cli-starter) | `cli-app` | Typer CLI with multi-command layout, uv, Ruff, pytest, and a console script entry point |
| [celery-worker](./templates/celery-worker) | `celery-worker` | Celery worker with modular tasks, Redis defaults, pydantic-settings, and eager-mode tests |
| [django-api](./templates/django-api) | `django-backend` | Django + DRF API with feature apps, OpenAPI-friendly health probes, uv, and Ruff |
| [uv-workspace-starter](./templates/uv-workspace-starter) | `uv-workspace` | Python monorepo using uv workspaces: shared packages and apps with one lockfile, Ruff, and Pyright |

## Documentation

| File | Contents |
|---|---|
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System overview, type system, generation flow |
| [docs/AUTHORING.md](./docs/AUTHORING.md) | Directory layout, `cpa.config.json`, extensions |
| [docs/TESTING.md](./docs/TESTING.md) | Local testing and CI workflow |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to add templates and extensions |

## Registry

The canonical catalog is [`templates.json`](./templates.json), consumed by the CLI from:

`https://raw.githubusercontent.com/Create-Python-App/cpa-templates/main/templates.json`

## CI

| Workflow | Trigger | Scope |
|----------|---------|-------|
| [CI Integrity (L0)](./.github/workflows/ci-integrity.yml) | PR + `main` + weekly | Registry paths + curated profiles |
| [CI Templates (L1)](./.github/workflows/ci-templates.yml) | PR + `main` + weekly | Every template alone via `uvx` (PyPI) |
| [CI Extensions (L2)](./.github/workflows/ci-extensions.yml) | PR (changed) + weekly | One extension × canonical template |
| [CI Profiles (L3)](./.github/workflows/ci-profiles.yml) | PR (changed) + weekly | Curated stacks in `ci/profiles/` |

Scaffolding always uses `uvx create-awesome-python-app@latest` from PyPI (never a source checkout of the CLI). Details: [docs/TESTING.md](./docs/TESTING.md), [#46](https://github.com/Create-Python-App/cpa-templates/issues/46).

## Related repositories

- [create-python-app](https://github.com/Create-Python-App/create-python-app) — CLI monorepo (scaffolding engine)
- [Create-Python-App](https://github.com/Create-Python-App) — organization home

## 👥 Contributors

<a href="https://github.com/Create-Python-App/cpa-templates/contributors">
  <img src="https://contrib.rocks/image?repo=Create-Python-App/cpa-templates"/>
</a>

Made with [contributors-img](https://contrib.rocks).
