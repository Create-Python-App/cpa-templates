# AGENTS.md – AI Interaction & Execution Guide (Humans: see CONTRIBUTING.md & docs/)

## Authoritative references

| Topic | Source |
|-------|--------|
| Architecture | docs/PROJECT_STRUCTURE.md |
| Configuration | docs/CONFIGURATION.md |
| Testing | docs/TESTING_GUIDE.md |
| Deployment | docs/DEPLOYMENT.md |
| Typing | docs/TYPING.md |

## Key commands

| Command | Purpose |
|---------|---------|
| `uv run my-cli --help` | CLI help (name from scaffold) |
| `uv run pytest` | Tests |
| `uv run ruff check .` | Lint |
| `uv run mypy cli_app` | Types |

## Command work protocol

1. Add modules under `cli_app/commands/`.
2. Register thin Typer wrappers in `cli_app/cli.py` that call `commands/`.
3. Cover with CliRunner tests.
4. Update docs when introducing config or packaging changes.

## Guardrails

- Prefer Rich for user output; avoid print noise in libraries.
- Do not dump secrets to stdout.
- Flag large dependency additions for human confirmation.
