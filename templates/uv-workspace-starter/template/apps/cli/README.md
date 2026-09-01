# cli

Typer command-line app for the workspace. It depends on the `core` library
through the uv workspace source, so local changes to `packages/core` are picked
up immediately — no publish step required.

## Run

```bash
uv run <command> hello          # <command> is what you chose at scaffold time
uv run <command> hello Ada
python -m cli_app hello Ada     # module entrypoint
```

## Develop

```bash
uv run pytest apps/cli          # test just this app
uv run ruff check apps/cli      # lint just this app
```

Add commands in `src/cli_app/cli.py` with the `@app.command()` decorator.
