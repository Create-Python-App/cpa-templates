# GitHub Setup Guide

## Overview

The **github-setup** extension configures GitHub Actions CI, Dependabot, issue forms, and a pull request template for a professional Python repository setup.

## What it adds

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Lint + test on push/PR to `main` |
| `.github/dependabot.yml` | Weekly GitHub Actions updates |
| `.github/ISSUE_TEMPLATE/` | Bug report and feature request forms |
| `.github/PULL_REQUEST_TEMPLATE.md` | Default PR description |

## Usage

Apply during scaffold:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons github-setup \
  --yes
```

Or copy the `.github/` tree into an existing project.

### CI workflow

The `ci.yml` workflow runs on push and pull requests targeting `main`:

1. Checkout
2. Install [uv](https://docs.astral.sh/uv/) via `astral-sh/setup-uv`
3. `uv python install 3.12`
4. `uv sync`
5. `uv run ruff check .`
6. `uv run pytest`

Customize steps as the project grows (type checking, coverage, Docker builds).

## Configuration

| Knob | Where | Notes |
|------|-------|-------|
| Python version | `ci.yml` → `uv python install` | Match `requires-python` |
| Branches | `on.push` / `on.pull_request` | Default `main` |
| Dependabot ecosystem | `dependabot.yml` | Default: GitHub Actions weekly |
| Issue forms | `ISSUE_TEMPLATE/*.yml` | Edit fields/labels as needed |

## Verification

After pushing to GitHub:

1. Open the **Actions** tab — the CI workflow should appear.
2. Push a commit or open a PR against `main` — **CI** should run and pass.
3. **Issues → New issue** — bug report and feature request templates available.
4. Open a PR — the PR template body should pre-fill.

Locally (same commands CI runs):

```sh
uv sync
uv run ruff check .
uv run pytest
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CI cannot find uv | Action version / network | Confirm `astral-sh/setup-uv` step and runner network |
| Ruff fails in CI only | Local format drift | Run `uv run ruff check .` and `ruff format .` before push |
| Dependabot PRs noisy | Too many ecosystems | Limit `package-ecosystem` entries |
| Templates missing | Files not under `.github/` | Confirm paths after scaffold |

## Resources

- [GitHub Actions](https://docs.github.com/en/actions)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [uv in CI](https://docs.astral.sh/uv/guides/integration/github/)
