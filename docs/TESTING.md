# Testing Templates and Extensions

## Testing with published slugs

After entries are registered in `templates.json` and the CLI catalog points to this repo:

```sh
CI=true uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons github-setup python-docker \
  --no-interactive
cd my-app && uv sync && uv run ruff check . && uv run pytest
```

## Testing local changes with `file://`

Use `file://` URLs to test unpublished templates or extensions without pushing to GitHub.
`customOptions` defaults are read from `cpa.config.json` inside the template directory.

```sh
REPO=/absolute/path/to/cpa-templates

# Local template only
CI=true uv run create-awesome-python-app my-app \
  --template "file://$REPO?subdir=templates/fastapi-starter" \
  --no-interactive

# Local template + local extensions
CI=true uv run create-awesome-python-app my-app \
  --template "file://$REPO?subdir=templates/fastapi-starter" \
  --addons \
    "file://$REPO?subdir=extensions/github-setup" \
    "file://$REPO?subdir=extensions/python-docker" \
  --no-interactive
cd my-app && uv sync && uv run pytest

# Remote template slug + local extension (extension-only development)
CI=true uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons "file://$REPO?subdir=extensions/my-new-extension" \
  --no-interactive
```

### Environment variables

| Variable | Purpose |
|----------|---------|
| `CI=true` | Non-interactive mode; use `customOptions` defaults |
| `CPA_SKIP_GIT=1` | Skip `git init` after scaffold |
| `CPA_CACHE_DIR` | Override template download cache |

### Debug output

Add `--verbose` to scaffold commands when supported by the CLI.

## Smoke test CI

`.github/workflows/smoke-test.yml` runs on pull requests to `main`. It scaffolds projects with `file://` URLs from the PR checkout and runs `uv sync`, lint, and tests.

To reproduce locally:

```sh
REPO="$PWD"
CI=true CPA_SKIP_GIT=1 uvx create-awesome-python-app smoke-test-app \
  --template "file://$REPO?subdir=templates/fastapi-starter" \
  --no-interactive --no-install
cd smoke-test-app && uv sync && uv run ruff check . && uv run pytest
```

## Checklist before opening a PR

- [ ] Scaffold succeeds with `file://` URL
- [ ] `uv sync` completes without errors
- [ ] `uv run ruff check .` passes (when ruff is configured)
- [ ] `uv run pytest` passes (when tests exist)
- [ ] Entry added or updated in `templates.json`
