# uv-workspace-starter

Maintainer-facing notes for the **uv-workspace-starter** template in `cpa-templates`.

Python monorepo using [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/): shared `packages/` libraries and `apps/` deployables with one lockfile, [Ruff](https://docs.astral.sh/ruff/), [Pyright](https://github.com/microsoft/pyright), [mypy](https://mypy.readthedocs.io/), and [pytest](https://docs.pytest.org/).

## Apply

```sh
uvx create-awesome-python-app my-workspace --template uv-workspace-starter
```

## Verify

After scaffolding, run from the project root:

```sh
cd my-workspace
uv sync
make check
```

`make check` runs lint + typecheck (Pyright and mypy) + tests in one shot.
Individual targets are also available:

| Command | Description |
|---------|-------------|
| `make lint` | Lint every member with Ruff |
| `make typecheck` | Type-check every member with Pyright + mypy |
| `make test` | Run the test suite across all members |
| `make check` | Run lint + typecheck + tests |

## Compatible Extensions

| Slug | Adds |
|------|------|
| `github-setup` | GitHub Actions CI, MegaLinter, Dependabot, issue/PR templates |
| `development-container` | VS Code Dev Container with Python 3.12 and uv |
| `pre-commit` | Local quality gates with Ruff, YAML validation, and whitespace checks |
