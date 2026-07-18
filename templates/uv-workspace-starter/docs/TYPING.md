# Typing

Workspace members are typed by default (`py.typed` on libraries). From the root:

```bash
uv run pyright
uv run mypy
```

Avoid unjustified `Any` and `# type: ignore` in shared packages.
