# GitHub Setup Guide

This project ships a GitHub automation setup for a Python/uv codebase: CI, code
quality, dependency updates, PR review automation, and structured issue/PR
templates. This guide documents the **actual files** that were added and how to
work with them.

## What was added

### Workflows (`.github/workflows/`)

| File | Trigger | What it does |
|------|---------|--------------|
| `ci.yml` | push + PR to `main` | Installs uv, runs `ruff check`, runs `mypy`/`pyright` (only when configured in `pyproject.toml`), then `pytest`. |
| `mega-linter.yml` | PR to `main` | Runs [MegaLinter](https://megalinter.io) (Python flavor) as a secondary quality pass. Fixes are **not** auto-applied. |
| `pr-review.yml` | PR to `main` | Runs [Danger JS](https://danger.systems/js/) against the PR description and diff. |
| `todo.yml` | push to `main` | Converts `# TODO:` comments into GitHub issues; opens a bot PR for inserted issue links (does **not** push directly to `main`). |

### Configuration

| File | Purpose |
|------|---------|
| `.mega-linter.yml` | MegaLinter config. Keeps linting Python-focused and disables linters already covered by Ruff or CI type checks. |
| `.github/dependabot.yml` | Weekly `pip` and `github-actions` updates, each grouped into a single PR. |

### Templates (`.github/`)

| File | Purpose |
|------|---------|
| `ISSUE_TEMPLATE/bug-report.yml` | Structured bug report (repro, expected/actual, environment). |
| `ISSUE_TEMPLATE/feature-request.yml` | Feature request with use case and proposed solution. |
| `ISSUE_TEMPLATE/documentation.yml` | Documentation issue report. |
| `ISSUE_TEMPLATE/config.yml` | Disables blank issues so contributors pick a template. |
| `PULL_REQUEST_TEMPLATE.md` | PR description with Description / Type of Change / How Has This Been Tested? / Checklist sections. |
| `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1. |

### Danger tooling (`tools/danger/`)

| File | Purpose |
|------|---------|
| `dangerfile.ts` | Danger rules (see below). |
| `package.json` | Danger + TypeScript dev dependencies (installed on-demand by `pr-review.yml`). |
| `tsconfig.json` | TypeScript config for the Dangerfile. |
| `.gitignore` | Ignores `node_modules/` and the generated lockfile. |

## CI workflow (`ci.yml`)

The `quality` job runs on every push and pull request to `main`:

1. Checkout
2. Install [uv](https://docs.astral.sh/uv/) via `astral-sh/setup-uv@v5` (cached)
3. `uv python install 3.12`
4. `uv sync`
5. `uv run ruff check .`
6. `uv run mypy .` — **only if** `[tool.mypy]` exists in `pyproject.toml`
7. `uv run pyright` — **only if** `[tool.pyright]` exists in `pyproject.toml`
8. `uv run pytest`

The type-check steps are gated so the same workflow works for both the plain and
the strictly-typed starter without failing on missing tools.

Run the same checks locally before pushing:

```sh
uv sync
uv run ruff check .
uv run pytest
# If your project configures them:
uv run mypy .
uv run pyright
```

## PR review with Danger (`pr-review.yml`)

`pr-review.yml` moves `tools/danger/*` to the repository root, runs `npm install`,
and executes the [Danger JS action](https://github.com/danger/danger-js). The
`dangerfile.ts` enforces:

- A non-empty PR **title** and **description**.
- Presence of the required PR template sections (`## Description`,
  `## Type of Change`, `## How Has This Been Tested?`, `## Checklist`).
- Reminders for unchecked checklist items.
- Small-PR encouragement and large-PR warnings (>200 changed lines or >10 files).
- Warnings when `pyproject.toml` or `uv.lock` change, so dependency updates get an
  extra look.

Keep the checklist items in `PULL_REQUEST_TEMPLATE.md` in sync with the
`checklistItems` array in `dangerfile.ts`.

### Optional: `DANGER_GITHUB_API_TOKEN`

Danger works with the default `GITHUB_TOKEN`. If you want Danger comments to post
from a bot account instead of `github-actions`, add a `DANGER_GITHUB_API_TOKEN`
repository secret.

## Dependabot (`.github/dependabot.yml`)

- **pip** — weekly updates for Python dependencies, grouped into one PR.
- **github-actions** — weekly updates for workflow action versions, grouped.

Adjust the `interval` or add `ignore` rules as your project matures.

## MegaLinter (`mega-linter.yml` + `.mega-linter.yml`)

Runs the Python flavor image on PRs. `APPLY_FIXES: none` keeps it advisory — it
reports issues but never commits changes back, avoiding noisy auto-commits in
scaffolded repos. Ruff remains the primary linter; MegaLinter disables the
Python linters that would duplicate Ruff or the CI type checks.

## TODO to issue (`todo.yml`)

On push to `main`, `# TODO:` comments become tracked GitHub issues (and issues
are closed when their TODO is removed). Inserted issue-URL edits are proposed
via a bot pull request (`chore/todo-issue-links`) instead of a direct push to
`main`. See the [action docs](https://github.com/alstr/todo-to-issue-action)
for the comment format.

## Recommended branch protection

Once the workflows have run at least once, protect `main`:

- Require the **CI** check to pass before merging.
- Require a pull request review.
- Require branches to be up to date before merging.

## Resources

- [GitHub Actions](https://docs.github.com/en/actions)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [MegaLinter](https://megalinter.io)
- [Danger JS](https://danger.systems/js/)
- [todo-to-issue](https://github.com/alstr/todo-to-issue-action)
