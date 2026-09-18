# Project Structure

This is a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/):
a single repository with multiple Python packages that share one lockfile and one
virtual environment.

## Directory layout

```txt
.
├── apps/                     # Deployable applications
│   └── cli/                  # Typer CLI that consumes packages/core
│       ├── src/cli_app/
│       ├── tests/
│       └── pyproject.toml
├── packages/                 # Shared libraries
│   └── core/                 # Example shared library
│       ├── src/core/
│       ├── tests/
│       └── pyproject.toml
├── docs/
├── Makefile
├── pyproject.toml            # Virtual workspace root (tooling + members)
└── .python-version
```

## Roles

### Workspace root (`pyproject.toml`)

A **virtual** root — it has no `[project]` table and is never published. It
declares the members and the shared tooling:

```toml
[tool.uv.workspace]
members = ["packages/*", "apps/*"]
```

Ruff, Pyright, pytest, and the `dev` dependency group are all configured once
here and apply to every member.

### `packages/`

Reusable libraries. Each is a real distribution with its own `pyproject.toml`
and a `src/<module>/` layout, and ships a `py.typed` marker.

### `apps/`

Deployable applications (CLIs, services, workers). They depend on libraries in
`packages/` through the workspace.

## Referencing a local library

A consumer lists the library's distribution name in its `dependencies` and marks
it as a workspace source so uv links the local copy instead of fetching from an
index:

```toml
[project]
dependencies = ["app-core", "typer>=0.15.0"]

[tool.uv.sources]
"app-core" = { workspace = true }
```

`uv sync` then installs every member into a single `.venv`, so edits to a library
are visible to its consumers immediately — no publish step required.

## Adding a member

1. Create `packages/<name>/` (library) or `apps/<name>/` (app). The workspace
   globs (`packages/*`, `apps/*`) pick it up automatically.
2. Add a `pyproject.toml` with `requires-python = ">=3.12"`, a `hatchling`
   build system, and `[tool.hatch.build.targets.wheel] packages = ["src/<module>"]`.
3. Add code under `src/<module>/` and tests under `tests/`.
4. Run `uv sync` to relink the workspace.
