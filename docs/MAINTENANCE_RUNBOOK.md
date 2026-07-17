# Maintenance Runbook

> Single source of truth for operating, extending, and fixing the `create-python-app` ecosystem.
>
> Scope: [`Create-Python-App/create-python-app`](https://github.com/Create-Python-App/create-python-app) (CLI + monorepo) and [`Create-Python-App/cpa-templates`](https://github.com/Create-Python-App/cpa-templates) (template and extension bank).

---

## 1. Why this runbook exists

The project is two repositories that must stay in sync:

- `create-python-app` — the CLI scaffolding tool, published to PyPI as `create-awesome-python-app`.
- `cpa-templates` — the template and extension bank consumed by the CLI.

Both have automated CI, automated releases, and a growing surface area of dependencies. A change in one repo (a new FastAPI version, a conflicting extra in an extension, a Python requirement bump) can break layered CI in the other. This runbook makes that work repeatable and traceable.

---

## 2. Operating constraints

Read these before any change:

- **Start with an issue.** Every significant fix, dependency update, security hardening, or new template/extension must begin as a GitHub issue. Break complex work into sub-issues when needed. The issue is the canonical place for analysis and decision history before any code is written.
- **If unsure, open an issue.** Do not start implementation when the solution is unclear. Use the issue to document the problem, options, and the chosen path.
- **One fix per PR.** If two issues are unrelated, open two PRs.
- **PRs must be ready for review.** Do not open PRs as drafts. Open them as **ready for review** so automated reviewers (CodeRabbit, AI tools, etc.) can inspect them.
- **Wait for AI review comments before merging.** After CI passes, allow a reasonable window for CodeRabbit or any configured AI reviewer to comment. If a blocking comment is raised, resolve it before merging. Only merge once both CI and AI reviews are quiet.
- **Link issues.** PR bodies must include `Closes #<issue>` when applicable.
- **English for all artifacts.** Commits, PRs, issues, docs, and comments are written in English.
- **Do not commit directly to `main`.** Always open a PR and let CI pass before merging.
- **Do not leave CI red on `main`.** If a merge breaks `main`, treat it as the next P0 fix.
- **Prefer minimal changes.** Do not refactor unrelated code while fixing a bug.
- **Document decisions.** If a choice is non-obvious (e.g., pinning a FastAPI major, constraining a transitive dependency in `pyproject.toml`, or adding `incompatibleWith`), document the rationale in the issue, the PR, and—if recurrent—in this runbook.

---

## 3. Pre-flight checklist for every session

Before writing code, run through this list. It is designed to be executed by a human or an AI agent.

```text
1. Read AGENTS.md in the target repository.
2. Review open issues:
   gh issue list --repo Create-Python-App/create-python-app --state open --limit 20
   gh issue list --repo Create-Python-App/cpa-templates --state open --limit 20
3. Review recent failed CI runs:
   gh run list --repo Create-Python-App/create-python-app --limit 10
   gh run list --repo Create-Python-App/cpa-templates --limit 10
4. Identify whether the task is:
   a) Bug fix (CI/templates/extensions broken)
   b) Dependency update (security, compatibility, features)
   c) New template or extension
   d) Security hardening
   e) Release/maintenance task
   f) Research/spike
5. Route to the right section of this runbook.
```

---

## 4. Decision tree

Use this to decide which procedure to follow:

```text
CI is red
├── Failure is in .github/workflows/ci-*.yml (L0–L3)
│   └── Read MAINTENANCE_CI.md
├── Failure is dependency resolution (uv sync, version conflict, Python requirement)
│   └── Read MAINTENANCE_DEPENDENCIES.md
├── Failure is ruff / pytest / type-check in a generated project
│   └── Read MAINTENANCE_TEMPLATES.md
└── Failure is in create-python-app core workflows (test, lint, publish)
    └── Read MAINTENANCE_RELEASE.md

Security alert received
└── Read MAINTENANCE_SECURITY.md

New template/extension requested
└── Read MAINTENANCE_TEMPLATES.md

Need to publish a release
└── Read MAINTENANCE_RELEASE.md
```

---

## 5. Generic workflow

Every task should follow these phases:

### 5.1 Discovery and issue creation

- Open a GitHub issue that describes the problem, its impact, and any known context. For large items, create sub-issues.
- Reproduce the failure locally when possible.
- Collect exact error messages, CI run IDs, and package versions.
- Check whether the issue is a regression (recent PR) or an external change (new dependency release on PyPI).
- If the fix is not obvious, keep the analysis in the issue and ask for human input before coding.

### 5.2 Plan

- Decide the fix strategy.
- Identify affected templates/extensions and the CI matrix.
- Estimate risk. If the change is high-risk, run L2 for touched extensions and the relevant L3 profile(s) before merging.

### 5.3 Implement

- Create a feature/fix branch.
- Make the smallest change that resolves the issue.
- Add or update tests/docs as needed.

### 5.4 Validate locally

- For `cpa-templates`: scaffold the affected template + extensions with `file://` URLs and run the full validation command.
- For `create-python-app`: run `uv run pytest`, `uv run ruff check .`, and any type-check workflow targets.

### 5.5 Open PR

- Open the PR as **ready for review** (not draft).
- Use a descriptive title.
- Include `Closes #<issue>` and a clear description of the change, validation performed, and risks.
- Ensure CI passes on the PR branch.
- Wait for automated AI reviews (e.g., CodeRabbit) to finish before merging. Address any blocking feedback; do not bypass it silently.

### 5.6 Merge and monitor

- Merge with squash or merge commit as appropriate.
- Watch `main` CI after merge.
- If `main` fails, start a hotfix immediately.

### 5.7 Sync knowledge

- If a new pattern, decision, or shortcut was learned, update this runbook or the workspace knowledge base.

---

## 6. Repositories at a glance

| Repo | What it is | Critical files | Critical CI |
|---|---|---|---|
| `create-python-app` | CLI + monorepo | `packages/*/pyproject.toml`, `.github/workflows/publish.yml` | `test.yml`, `lint.yml`, `type-check.yml`, `publish.yml`, `osv-scanner.yml` |
| `cpa-templates` | Template/extension bank | `templates.json`, `templates.schema.json`, `templates/`, `extensions/`, `ci/profiles/` | `ci-integrity.yml`, `ci-templates.yml`, `ci-extensions.yml`, `ci-profiles.yml` |

---

## 7. Quick reference: most common commands

```bash
# --- Scaffold locally from cpa-templates ---
REPO=/absolute/path/to/cpa-templates
CI=true uvx create-awesome-python-app@latest smoke-test-app \
  --template "file://$REPO?subdir=templates/<slug>" \
  --addons "file://$REPO?subdir=extensions/<ext1>" \
         "file://$REPO?subdir=extensions/<ext2>" \
  --no-interactive

cd smoke-test-app
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest -q

# --- Inspect CI failures ---
gh run view <run-id> --repo Create-Python-App/<repo> --log-failed

# --- Run cpa-templates CI manually ---
gh workflow run "CI Integrity (L0)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Templates (L1)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Extensions (L2)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Profiles (L3)" --repo Create-Python-App/cpa-templates --ref main
gh run watch <run-id> --repo Create-Python-App/cpa-templates --exit-status

# --- Inspect package versions on PyPI ---
uv pip index versions <pkg>
curl -s "https://pypi.org/pypi/<pkg>/json" | jq -r '.info.version'

# --- create-python-app monorepo ---
uv sync --group dev
uv run pytest
uv run ruff check .
```

---

## 8. Related documentation

| File | Use |
|---|---|
| [docs/ARCHITECTURE.md](./ARCHITECTURE.md) | How templates and extensions are composed |
| [docs/AUTHORING.md](./AUTHORING.md) | File conventions, Jinja, `cpa.config.json`, `pyproject.toml` merge |
| [docs/TESTING.md](./TESTING.md) | Local test commands |
| [docs/MAINTENANCE_TEMPLATES.md](./MAINTENANCE_TEMPLATES.md) | Working with templates and extensions |
| [docs/MAINTENANCE_DEPENDENCIES.md](./MAINTENANCE_DEPENDENCIES.md) | Updating and resolving dependencies |
| [docs/MAINTENANCE_SECURITY.md](./MAINTENANCE_SECURITY.md) | Security alerts, audits, Dependabot |
| [docs/MAINTENANCE_CI.md](./MAINTENANCE_CI.md) | CI workflows, troubleshooting |
| [docs/MAINTENANCE_RELEASE.md](./MAINTENANCE_RELEASE.md) | PyPI releases and tagging |

---

## 9. Runbook changelog

| Date | Change | PR |
|---|---|---|
| 2026-07-16 | Initial CPA maintenance runbook suite (ported from cna-templates) | TBD |
