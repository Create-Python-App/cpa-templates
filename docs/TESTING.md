# Testing Templates and Extensions

## Testing with published slugs

After entries are registered in `templates.json` and the CLI catalog points to this repo:

```sh
CI=true uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons github-setup fastapi-docker \
  --no-interactive
cd my-app && uv sync && uv run ruff check . && uv run pytest
```

## Testing local changes with `file://`

Use `file://` URLs to test unpublished templates or extensions without pushing to GitHub.
`customOptions` defaults are read from `cpa.config.json` inside the template directory.

```sh
REPO=/absolute/path/to/cpa-templates

# Local template only (always use published CLI via uvx)
CI=true uvx create-awesome-python-app my-app \
  --template "file://$REPO?subdir=templates/fastapi-starter" \
  --no-interactive

# Local template + local extensions
CI=true uvx create-awesome-python-app my-app \
  --template "file://$REPO?subdir=templates/fastapi-starter" \
  --addons \
    "file://$REPO?subdir=extensions/all-github-setup" \
    "file://$REPO?subdir=extensions/fastapi-docker" \
  --no-interactive
cd my-app && uv sync && uv run pytest
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `CI=true` | Non-interactive mode; use `customOptions` defaults |
| `CPA_SKIP_GIT=1` | Skip `git init` after scaffold |
| `CPA_CACHE_DIR` | Override template download cache |

## Layered CI (L0–L3)

CI must always scaffold with **`uvx create-awesome-python-app@latest` from PyPI**. It never checks out `create-python-app` and never falls back to source.

| Layer | Workflow | What green means |
|-------|----------|------------------|
| **L0** | `ci-integrity.yml` | Registry paths exist; categories valid; curated profiles valid |
| **L1** | `ci-templates.yml` | Every template scaffolds alone + `uv sync` + ruff (+ mypy/pyright when configured) + pytest |
| **L2** | `ci-extensions.yml` | Each extension alone on the canonical template (`fastapi-starter`) |
| **L3** | `ci-profiles.yml` | Curated one-per-category stacks in `ci/profiles/*.json` |

**Not run:** stacking every compatible extension at once (that is not a user journey and hides attribution).

### Local reproduction of CI

```sh
REPO="$PWD"
python scripts/ci/validate-registry.py
python scripts/ci/generate-matrix.py --layer validate-profiles

# Same runner the Actions use
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$REPO?subdir=templates/fastapi-starter" \
  --workdir /tmp/cpa-check
```

## Checklist before opening a PR

- [ ] Scaffold succeeds with `file://` URL via `uvx` (PyPI CLI)
- [ ] `uv sync` completes without errors
- [ ] `uv run ruff check .` passes (when ruff is configured)
- [ ] Typed templates: `uv run mypy .` / `uv run pyright` pass
- [ ] `uv run pytest` passes (when tests exist)
- [ ] Entry added or updated in `templates.json`
- [ ] New extension has a distinct `category` (ci / containers / database / editor / …)
