# Maintenance: Release and Publishing

> How to manage releases and PyPI publishing for `create-python-app`.
>
> **Last refreshed:** 2026-10-05 (verified against `create-python-app` release workflows)
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Release model

`create-python-app` publishes two PyPI packages from one monorepo:

- `create-python-app-core` — scaffolding engine
- `create-awesome-python-app` — CLI entry point (`uvx create-awesome-python-app`)

Releases are prepared through the `Prepare release PR` workflow and published by the `Release` workflow in the [`create-python-app` monorepo](https://github.com/Create-Python-App/create-python-app). Do not run `uv publish` locally unless maintainers invoke a documented emergency break-glass procedure.

**Recent release cadence:** Three releases from 2026-07-28 through 2026-09-15 (v0.2.12, v0.3.0, and v0.3.1). Version 0.3.0 shipped CLI features (`--json`, `--category`, `--config`, `--skip-install`, Rich spinner, and shell completion docs); 0.3.1 was a maintenance release for Ruff and GitHub Actions updates.

Flow:

1. Run the `Prepare release PR` workflow with the version and release notes. It updates both package versions, the CLI's core dependency, and `CHANGELOG.md`.
2. Review and merge the generated release PR after CI passes.
3. Push the matching tag: `create-awesome-python-app@X.Y.Z`.
4. The `Release` workflow builds both packages, creates the GitHub Release, and publishes them to PyPI with OIDC trusted publishing.
5. After `Release` succeeds, Docker, AUR, and Homebrew distribution workflows run from `workflow_run`; verify those workflows and the distribution smoke tests.

---

## 2. Preparing a release

Before preparing a release:

1. Ensure `main` CI is green.
2. Run `Prepare release PR` with the proposed semantic version and release notes; the workflow updates both `pyproject.toml` files, the core version requirement in the CLI, and `CHANGELOG.md`.
3. Review the generated diff, confirm the versions are consistent, and merge the PR before tagging.
4. Confirm template catalog URLs in `cpa-templates` still resolve (templates are fetched from GitHub, not PyPI).

CPA uses an explicit release PR and tag, rather than Changesets. The release preparation workflow is the source of truth for version and changelog edits.

---

## 3. Publishing requirements

The `publish.yml` workflow (named **Release**) uses PyPI **Trusted Publishing** via OIDC. Requirements:

1. Every publishable `pyproject.toml` must declare correct project metadata and repository links.
2. The workflow job must request `id-token: write` permission.
3. The PyPI project must trust the GitHub environment (`pypi`) for this repository.
4. Tags must match the expected pattern: `create-awesome-python-app@*`.
5. The separate `publish-docker.yml` workflow runs after the Release workflow succeeds. It waits until the package appears in PyPI's JSON API and simple index and its wheel URL responds, then builds the image. This wait handles the observed PyPI CDN/indexing delay; do not add an arbitrary fixed sleep.
6. Docker actions are pinned by commit SHA in `publish-docker.yml`; check that workflow for the current versions. They are not part of the PyPI publish job.
7. MegaLinter runs in its own CI workflow and is not a step in `publish.yml`. Require the repository's configured CI checks to pass before merging the release PR.

No long-lived `PYPI_TOKEN` secret is required when trusted publishing is configured.

---

## 4. Troubleshooting release failures

### 4.1 Publish rejected or provenance mismatch

Check:

- Project URLs in `pyproject.toml` point to the correct GitHub repo.
- The workflow runs with `id-token: write`.
- The PyPI trusted publisher is configured for this repository and environment.
- The tag name matches `create-awesome-python-app@X.Y.Z`.

### 4.2 Build failures

Check:

- `uv sync --group dev` succeeds locally.
- `uv build --package create-python-app-core` and `uv build --package create-awesome-python-app` succeed.
- Version numbers are consistent across packages.

### 4.3 Tag push did not trigger workflow

Check:

- Tag matches `create-awesome-python-app@*` filter in `publish.yml`.
- Workflow file exists on the tagged commit.

### 4.4 PyPI indexing delay for Docker builds

`publish-docker.yml` starts only after the Release workflow succeeds and polls the PyPI JSON API, simple index, and wheel URL before building. If it times out, inspect those three checks in the run log and verify the package/version on PyPI before rerunning the workflow. The current workflow already handles the known indexing race; do not add a second wait without reproducing a remaining failure.

---

## 5. Verifying a release

### 5.1 PyPI registry

```bash
uv pip index versions create-awesome-python-app | head
curl -s "https://pypi.org/pypi/create-awesome-python-app/json" | jq -r '.info.version'
curl -s "https://pypi.org/pypi/create-python-app-core/json" | jq -r '.info.version'
```

### 5.2 Install smoke test

```bash
uvx create-awesome-python-app@latest --help
CI=true uvx create-awesome-python-app@latest smoke-verify \
  --template fastapi-starter --no-interactive
```

If all packages were published correctly, the latest CLI starts without errors and can scaffold from the catalog.

---

## 6. When to release

| Change | Release needed? |
|---|---|
| Docs only in `cpa-templates` | No |
| Template/extension in `cpa-templates` | No (templates are fetched from GitHub, not PyPI) |
| Fix in `create-awesome-python-app` CLI | Yes |
| Fix in `create-python-app-core` | Yes |
| Security fix in CLI dependency | Yes — release quickly |

---

## 7. Checklist

- [ ] Version fields updated for affected packages.
- [ ] `main` CI is green before tagging.
- [ ] Tag `create-awesome-python-app@X.Y.Z` pushed to GitHub.
- [ ] The publish workflow completed successfully.
- [ ] New versions appear on PyPI and `uvx create-awesome-python-app@latest` works.
- [ ] No personal PyPI token was used when trusted publishing is available.
