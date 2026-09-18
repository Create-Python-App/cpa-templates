# core

Shared library for the workspace. Apps under `apps/` depend on it through the
uv workspace source mechanism, so changes are picked up without publishing.

## Usage

```python
from core import greeting

greeting("Ada")  # "Hello, Ada!"
```

## Develop

```bash
uv run pytest packages/core        # test just this package
uv run ruff check packages/core    # lint just this package
```

Add modules under `src/core/` and export the public API from
`src/core/__init__.py`. This package ships `py.typed`, so downstream members get
type information automatically.
