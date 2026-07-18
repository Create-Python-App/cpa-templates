# Maintenance: CI and Workflows

> How to diagnose, fix, and extend the CI workflows that validate the `create-python-app` ecosystem.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Workflows overview

### `create-python-app` (CLI monorepo)

| Workflow | Purpose |
|---|---|
| `test.yml` | Unit and integration tests |
| `type-check.yml` | Static type checking |
| `lint.yml` | Ruff and formatting checks |
| `mega-linter.yml` | MegaLinter across the repo |
| `osv-scanner.yml` | Security scanning |
| `publish.yml` | Tag-triggered PyPI release |
| `smoke-distribution.yml` | End-to-end install smoke (`uvx`, Docker, brew, AUR) |
| `pr-review.yml` | PR automation |

### `cpa-templates` (layered trust)

| Workflow | Purpose |
|---|---|
| `ci-integrity.yml` (L0) | Registry on-disk paths + curated profile validation |
| `ci-templates.yml` (L1) | Every template alone |
| `ci-extensions.yml` (L2) | One extension × canonical template |
| `ci-profiles.yml` (L3) | Curated realistic stacks (`ci/profiles/*.json`) |

**Hard contract:** scaffolding in `cpa-templates` CI always uses:

```sh
uvx create-awesome-python-app@latest …
```

Never check out `Create-Python-App/create-python-app`. Never fall back to source. Template CI must exercise the same binary users install from PyPI.

Retired: `smoke-test.yml`, `test-combinations.yml` (random + all-extensions stacks). See [#46](https://github.com/Create-Python-App/cpa-templates/issues/46).

---

## 2. Reading CI failures

```bash
gh run view <run-id> --repo Create-Python-App/cpa-templates --log-failed
gh run list --repo Create-Python-App/cpa-templates --limit 20
```

| Red cell pattern | Meaning |
|---|---|
| `L1 · <template>` | Baseline template broken (or empty scaffold) |
| `L2 · <ext> @ <template>` | That extension alone breaks the canonical template |
| `L3 · <profile>` | Curated stack broken (or profile JSON invalid — usually caught in L0) |

---

## 3. Running workflows manually

```bash
gh workflow run "CI Integrity (L0)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Templates (L1)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Extensions (L2)" --repo Create-Python-App/cpa-templates --ref main
gh workflow run "CI Profiles (L3)" --repo Create-Python-App/cpa-templates --ref main

gh run watch <run-id> --repo Create-Python-App/cpa-templates --exit-status
```

Use `--ref <branch>` to test a PR branch before merging.

---

## 4. Layer details

### L0 — Integrity

Runs `scripts/ci/validate-registry.py` and `generate-matrix.py --layer validate-profiles`.

### L1 — Templates

Matrix from `templates.json`. Each cell:

1. Asserts `file://…?subdir=templates/<dir>` exists (empty-scaffold guard).
2. `uvx create-awesome-python-app@latest … --no-install`
3. `uv sync` → `ruff` → optional `mypy`/`pyright` → `pytest`

### L2 — Extensions

One extension on `fastapi-starter` (canonical for `fastapi-backend`).  
PRs: `--changed-only` unless `templates.json` / `scripts/ci/` / `ci/profiles/` / `ci-*.yml` change (then full).  
Weekly / manual: full.

### L3 — Profiles

Curated JSON under `ci/profiles/`. Validator enforces **one extension per category** and type compatibility. Split categories (`ci`, `containers`, `database`, `editor`) so realistic stacks stay attributable.

---

## 5. Local runner

```bash
REPO="$PWD"
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$REPO?subdir=templates/fastapi-starter" \
  --addon-url "file://$REPO?subdir=extensions/fastapi-docker" \
  --workdir /tmp/cpa-check
```

Requires `uv` / `uvx` on `PATH`.

---

## 6. Common failures

| Symptom | Likely cause |
|---|---|
| Scaffold step fails | Invalid `templates.json`, broken `file://` path, CLI regression on PyPI |
| Empty-guard fails | Wrong `subdir` / silent no-op copy |
| `uv sync` fails | Conflicting `pyproject.toml` merge or bad version pin |
| `ruff` / `mypy` / `pytest` fails | Broken template or extension files |
| `uvx` cannot resolve package | PyPI outage or yanked release — **do not** work around with a source checkout; fix publish |

Reproduce with [docs/TESTING.md](./TESTING.md).
