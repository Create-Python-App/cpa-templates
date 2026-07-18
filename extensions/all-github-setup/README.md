# GitHub Setup

Adds a complete GitHub automation setup to a generated Python/uv project: CI,
code quality, dependency updates, PR-review automation, and structured
issue/PR templates.

> **Authoring note:** everything that gets copied into the generated project
> lives under [`template/`](./template). This file (the extension's own README)
> stays at the extension root and is **not** copied — CPA copies from
> `template/` when it exists (see [`docs/AUTHORING.md`](../../docs/AUTHORING.md)),
> so it never overwrites the generated project's `README.md`.

## When to use

- You host the project on GitHub and want CI, linting, and PR automation from day one.
- You want Dependabot to keep both Python dependencies and GitHub Actions up to date.
- You want structured bug reports, feature requests, and PR descriptions without writing YAML by hand.

Skip this extension if you use another CI provider (GitLab CI, CircleCI, etc.).

## What it adds

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | uv → ruff → mypy/pyright (when configured) → pytest, on push/PR to `main` |
| `.github/workflows/mega-linter.yml` | MegaLinter (Python flavor) as a secondary quality pass |
| `.github/workflows/pr-review.yml` | Danger JS validates PR title, description, sections, and diff size |
| `.github/workflows/todo.yml` | Converts `# TODO:` comments into GitHub issues |
| `.mega-linter.yml` | Python-focused MegaLinter config (`APPLY_FIXES: none`) |
| `.github/dependabot.yml` | Weekly `pip` + `github-actions` updates, grouped |
| `.github/ISSUE_TEMPLATE/` | Bug report, feature request, and documentation forms + config |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR template matching the Danger checks |
| `.github/CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 |
| `tools/danger/` | Dangerfile, `package.json`, `tsconfig.json`, `.gitignore` |
| `docs/GITHUB_SETUP_GUIDE.md` | Full guide to the shipped files |

## Usage

Apply during scaffold:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons github-setup
```

Or add manually by copying the contents of this extension's `template/` directory
into an existing project.

## Verification

After scaffolding and pushing to GitHub:

1. Open the **Actions** tab — the CI, MegaLinter, and PR validation workflows appear.
2. Open a PR against `main` — CI runs, and Danger comments on the PR description.
3. Open **Issues → New issue** — bug, feature, and documentation templates are available.
4. Open a PR — the PR template body pre-fills.

Locally, before pushing (same checks CI runs):

```sh
uv sync
uv run ruff check .
uv run pytest
```

See [`template/docs/GITHUB_SETUP_GUIDE.md`](./template/docs/GITHUB_SETUP_GUIDE.md)
for full configuration and customization details.
