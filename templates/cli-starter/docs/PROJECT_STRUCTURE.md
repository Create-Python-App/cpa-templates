# Project structure

```
cli_app/
  __init__.py          # package version
  __main__.py          # python -m cli_app
  cli.py               # Typer root app + callbacks
  config.py            # env-based settings helpers
  commands/
    greet.py           # `hello` command group
    info.py            # `info` command group
tests/
  test_cli.py
docs/
pyproject.toml         # [project.scripts] console entry
```

## Adding a command

1. Create `cli_app/commands/<domain>.py` with a `typer.Typer()` group.
2. Register commands in `cli_app/cli.py` (thin Typer wrappers calling `commands/`).
3. Add CliRunner tests in `tests/`.
4. Document user-facing flags in the root README when they are part of the UX.

## Conventions

- Prefer Rich for user-visible output.
- Keep parsing/validation at the Typer boundary; put reusable logic in plain functions.
- Avoid a single mega-`cli.py` — split by domain under `commands/`.
