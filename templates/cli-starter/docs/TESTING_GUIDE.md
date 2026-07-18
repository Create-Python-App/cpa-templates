# Testing guide

Use Typer's `CliRunner` for in-process invocation (no subprocess).

```python
from typer.testing import CliRunner
from cli_app.cli import app

runner = CliRunner()
result = runner.invoke(app, ["hello", "CPA"])
assert result.exit_code == 0
```

Strip ANSI codes when asserting Rich output (see `tests/test_cli.py`).

## Commands

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy cli_app
```

## What to cover

- `--version` / help paths
- Happy path for each command group
- Error exits (`raise typer.Exit(code=1)`) when you add validation
