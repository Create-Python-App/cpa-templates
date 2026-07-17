# CLI Starter

Typer CLI starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), and [pytest](https://docs.pytest.org/).

## Quick start

```sh
uv sync
uv run my-cli --help
uv run my-cli hello
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run my-cli --help` | Show CLI help |
| `uv run my-cli hello [name]` | Sample command |
| `uv run ruff check .` | Lint |
| `uv run pytest` | Run tests |

## Project layout

```
cli_app/     # Typer application package
tests/       # CLI invocation tests
```

## Configuration

Scaffold-time option (`cpa.config.json`):

| Option | Default | Description |
|--------|---------|-------------|
| `commandName` | `my-cli` | Console script name written to `[project.scripts]` |

Compatible extensions: `github-setup`, `python-devcontainer`, `python-docker`.
