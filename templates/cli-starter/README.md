# CLI Starter

Typer CLI starter with multi-command packages, [uv](https://docs.astral.sh/uv/),
[Ruff](https://docs.astral.sh/ruff/), and [pytest](https://docs.pytest.org/).

## Quick start

```sh
uv sync
uv run my-cli --help
uv run my-cli hello
uv run my-cli version
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run my-cli --help` | Show CLI help |
| `uv run my-cli hello [name]` | Sample greeting |
| `uv run my-cli version` | Print package version |
| `uv run ruff check .` | Lint |
| `uv run pytest` | Run tests |

## Project layout

```
cli_app/
  cli.py          # Typer root
  config.py       # env helpers
  commands/       # command groups (greet, info, …)
tests/
docs/
```

## Configuration

Scaffold-time option (`cpa.config.json`):

| Option | Default | Description |
|--------|---------|-------------|
| `commandName` | `my-cli` | Console script name written to `[project.scripts]` |

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

Compatible extensions: `github-setup`, `development-container`.

## Docs

- [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
- [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [AGENTS.md](AGENTS.md) · [CONTRIBUTING.md](CONTRIBUTING.md)
