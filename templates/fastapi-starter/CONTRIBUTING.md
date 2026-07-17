# Contributing

Thanks for your interest in contributing to this project! This document is the human entry point after reading the README. It explains how to work effectively inside a project generated from the FastAPI starter template.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Bootstrap](#project-bootstrap)
- [Scripts & Tooling](#scripts--tooling)
- [Architecture Conventions](#architecture-conventions)
- [Coding Standards](#coding-standards)
- [Git / Branch Workflow](#git--branch-workflow)
- [Commit Messages](#commit-messages)
- [Adding Dependencies](#adding-dependencies)
- [Testing Strategy](#testing-strategy)
- [Documentation](#documentation)
- [Pull Request Checklist](#pull-request-checklist)

## Prerequisites

- Python matching `requires-python` in `pyproject.toml` (3.12+)
- [uv](https://docs.astral.sh/uv/) installed
- Optional: Docker if using `python-docker` / `python-postgres` extensions

## Project Bootstrap

```sh
uv sync
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to verify the API is up.

## Scripts & Tooling

| Command | Purpose |
|---------|---------|
| `uv run uvicorn app.main:app --reload` | Dev server |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run mypy app` | Type check (mypy) |
| `uv run pyright` | Type check (pyright) |
| `uv run pytest` | Tests |

Keep a clean working tree before opening a PR. See [docs/CONFIGURATION.md](./docs/CONFIGURATION.md) and [docs/TYPING.md](./docs/TYPING.md).

## Architecture Conventions

Read [docs/PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md) first. Each feature lives under `app/features/<domain>/` with:

- `router.py` — HTTP endpoints
- `service.py` — business logic
- `schemas.py` — Pydantic request/response models

Shared envelopes live in `app/schemas/common/`. Mount new feature routers from `app/api/router.py`.

## Coding Standards

- Prefer typed Python end-to-end: annotate public functions, avoid untyped `Any` unless justified
- Use Pydantic models at API boundaries; keep services free of FastAPI request objects when practical
- Prefer composition over inheritance
- Keep routers thin — push logic into services
- Return `APIResponse[T]` from feature routes for a consistent client contract

## Git / Branch Workflow

- Create feature branches from `main`: `feat/short-description`
- Rebase (or merge) with `main` before opening a PR

## Commit Messages

Follow Conventional Commits: `feat: add user listing endpoint`, `fix: handle missing request id`. Squash locally if you produced noisy commits.

## Adding Dependencies

```sh
uv add <package>
# or for tooling:
uv add --dev <package>
```

Before adding a dependency, check whether an existing package already solves the problem. Document the rationale in the PR when adding something substantial.

## Testing Strategy

- Add tests under `tests/` (or `tests/features/`) for new endpoints and services
- Assert on the response envelope (`success`, `dev_code`, `metadata.request_id`) not only raw payloads
- See [docs/TESTING_GUIDE.md](./docs/TESTING_GUIDE.md)

## Documentation

Update or add docs in `docs/` when introducing new concepts, configuration, or architectural changes. Keep [docs/README.md](./docs/README.md) indexed when you add a new guide.

## Pull Request Checklist

- [ ] Feature / fix scoped and documented
- [ ] Lint + format pass (`ruff`)
- [ ] Type checks pass (mypy and/or pyright when configured)
- [ ] Added / updated tests (or documented why not)
- [ ] Updated docs if needed
- [ ] No unused or dead code

Happy hacking!
