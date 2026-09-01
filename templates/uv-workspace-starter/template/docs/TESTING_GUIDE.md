# Testing guide

Run the full workspace suite from the root:

```bash
uv sync
uv run pytest
# or
make check   # lint + typecheck + tests when Makefile is present
```

## Layout

- Shared library tests: `packages/<name>/tests/`
- App tests: `apps/<name>/tests/`
- Prefer testing libraries in isolation; apps may depend on path/workspace deps.

## Conventions

- One logical assertion focus per test
- Type-check both packages and apps (`uv run pyright` / `uv run mypy`)
- Do not skip members in CI without documenting why

## Adding coverage

When you add a member, ensure pytest discovers its `tests/` (or configure
`testpaths` / `pythonpath` accordingly) and that `make check` stays green.
