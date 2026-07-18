# Contributing

## Setup

```bash
uv sync
uv run pytest
uv run my-cli --help
```

## Style

- Command groups under `cli_app/commands/`
- Ruff for lint/format
- Typed public functions

## Docs

Update the matching file under `docs/` when behaviour changes. Keep `AGENTS.md`
as a pointer table, not a second docs tree.

## Extensions

Optional: `github-setup`, `development-container`.
