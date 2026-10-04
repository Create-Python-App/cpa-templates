# Maintenance: Release and Publishing

> How to manage releases and PyPI publishing for `create-python-app`.
>
> **Last refreshed:** 2026-09-21 (post-v0.3.0)
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Release model

`create-python-app` publishes two PyPI packages from one monorepo:

- `create-python-app-core` — scaffolding engine
- `create-awesome-python-app` — CLI entry point (`uvx create-awesome-python-app`)

Releases are tag-triggered via GitHub Actions. No manual `uv publish` from a local machine unless you are performing an emergency break-glass procedure documented by maintainers.

**Recent release cadence:** Two releases (v0.2.12 and v0.3.0) in ~3 months, with v0.3.0 (2026-09-10) shipping new CLI features (--json, --category, --config, --skip-install, Rich spinner, shell completion docs).

Flow:

1. Merge fixes to `main`.
2. Create and push a tag: `create-awesome-python-app@X.Y.Z`.
3. The `Release` workflow builds wheels, creates a GitHub Release, and publishes to PyPI with OIDC trusted publishing.

---

## 2. Preparing a release

Before tagging:

1. Ensure `main` CI is green.
2. Update version fields in `packages/create-awesome-python-app/pyproject.toml` and `packages/create-python-app-core/pyproject.toml` if not already bumped on `main`.
3. Update CHANGELOG or release notes when the project maintains them.
4. Confirm template catalog URLs in `cpa-templates` still resolve (templates are fetched from GitHub, not PyPI).

Unlike the CNA Changesets flow, CPA currently uses explicit version bumps and tags. Follow existing repo conventions when that evolves.

---

## 3. Publishing requirements

The `publish.yml` workflow uses PyPI **Trusted Publishing** via OIDC. Requirements:

1. Every publishable `pyproject.toml` must declare correct project metadata and repository links.
2. The workflow job must request `id-token: write` permission.
3. The PyPI project must trust the GitHub environment (`pypi`) for this repository.
4. Tags must match the expected pattern: `create-awesome-python-app@*`.
5. Docker actions in the build matrix are current as of v0.3.0 release:
   - `docker/setup-qemu-action@v4.3`
   - `docker/setup-buildx-action@v4.3`
   - `docker/login-action@v4.6`
6. MegaLinter is v10+ in the publish CI gate (upgraded from v9).

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

### 4.4 Docker CDN sync delays

**Status (v0.3.0):** Verify whether the CDN race condition (slow Docker layer availability post-publish) has been resolved upstream. If layers are not immediately available after push, add an explicit wait in the workflow before consuming freshly-published images. This was a known issue in earlier releases; check the current state with your infrastructure team.

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
