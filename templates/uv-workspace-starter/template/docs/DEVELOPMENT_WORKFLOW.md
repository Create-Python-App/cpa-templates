# Development Workflow

## Getting started

```bash
uv sync          # install every member into one .venv
uv run pytest    # verify the workspace is healthy
```

## Everyday commands

Run these from the workspace root (or use the `Makefile` shortcuts):

| Command | `make` | Description |
| ------- | ------ | ----------- |
| `uv sync` | `make sync` | Install/relink all members |
| `uv run ruff check .` | `make lint` | Lint all members |
| `uv run ruff format .` | `make format` | Format the workspace |
| `uv run pyright && uv run mypy` | `make typecheck` | Type-check all members (Pyright + mypy) |
| `uv run pytest` | `make test` | Test all members |
| — | `make check` | Lint + typecheck + test |
| `uv build --all-packages` | `make build` | Build all members |

## Scoping to a single member

```bash
uv run pytest packages/core        # test one member
uv run ruff check apps/cli         # lint one member
```

## Managing dependencies

- **Add an external dependency to a member:**

  ```bash
  uv add --package app-core httpx
  ```

- **Add a dev tool shared across the workspace:**

  ```bash
  uv add --dev pytest-cov
  ```

- **Make one member depend on another (local) member:**

  Add its distribution name to `dependencies`, then declare the workspace source:

  ```toml
  [tool.uv.sources]
  "app-core" = { workspace = true }
  ```

  Run `uv sync` to relink.

## Adding a new member

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md#adding-a-member). In short: create
`packages/<name>/` or `apps/<name>/`, add a `pyproject.toml` and `src/<module>/`,
then `uv sync`.

## Troubleshooting

- **`ModuleNotFoundError` for a local member** — run `uv sync`; a new member is
  only linked after a sync.
- **Pyright/mypy can't resolve a member** — confirm the module is under
  `src/<module>/` and its `src/` is listed in the root `[tool.pyright] extraPaths`
  and `[tool.mypy] mypy_path` (add new members to both).
- **Circular imports between members** — extract the shared piece into a third
  library under `packages/`.
