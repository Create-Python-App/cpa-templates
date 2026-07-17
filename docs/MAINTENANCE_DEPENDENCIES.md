# Maintenance: Dependencies

> How to update, investigate, and resolve dependency conflicts in templates and extensions.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Investigating a dependency

Before bumping a version, verify that it exists on PyPI and that its requirements are compatible with the template's Python version.

```bash
# Latest published version
curl -s "https://pypi.org/pypi/<pkg>/json" | jq -r '.info.version'

# List recent releases
uv pip index versions <pkg>

# Inspect requires-python and dependencies (PyPI metadata)
curl -s "https://pypi.org/pypi/<pkg>/<version>/json" | jq '.info | {requires_python, requires_dist}'

# Show what uv would resolve in a generated project
cd my-app && uv tree
```

Example:

```bash
uv pip index versions fastapi
curl -s "https://pypi.org/pypi/pydantic-settings/json" | jq -r '.info.requires_python'
cd smoke-test-app && uv tree --package fastapi
```

If a version is missing, PyPI returns 404 or `uv pip index versions` omits it. That immediately tells you the range in `pyproject.toml` is invalid.

---

## 2. Dependency resolution failures

### 2.1 Version not found

**Meaning:** The requested version does not exist on PyPI.

**Common cause:** A template or extension pins a version that was yanked, never published, or mistyped.

**Fix:**

1. Verify the exact package name and version on PyPI.
2. Either:
   - Drop the dependency if it is no longer needed.
   - Pin to the latest compatible release.
   - Rename the package if upstream renamed it in a new major line.

### 2.2 `uv sync` resolution conflict

**Meaning:** uv cannot satisfy the dependency graph, usually because two packages require incompatible versions of the same dependency or different Python versions.

**Common cause:** Two extensions add conflicting version constraints to merged `pyproject.toml` keys, or a template pins a major version that an extension's extras cannot use.

**Fix strategies (in order of preference):**

1. **Align both sides** to a mutually compatible version. This is the cleanest fix.
2. **Downgrade the more aggressive requirement** if the newer major is not strictly needed.
3. **Constrain the conflict in `pyproject.toml`** using `[tool.uv]` overrides or explicit pins in the extension layer that owns the dependency.
4. **Mark extensions as incompatible** if they truly cannot coexist (`incompatibleWith` in `templates.json`).

### 2.3 Python version mismatch

**Meaning:** A package requires `requires-python` newer (or older) than the template declares.

**Fix:** Update `requires-python` in the template `pyproject.toml` consistently, and ensure CI uses a matching Python version.

---

## 3. Updating dependencies

### 3.1 In an extension

1. Edit `extensions/<slug>/pyproject.toml` (partial manifest with only the keys the extension adds).
2. Use conservative ranges: `>=x.y.z,<next-major` or compatible caret-style bounds where appropriate.
3. Avoid major-version bumps unless you have validated breaking changes.
4. Re-scaffold the extension with each compatible template and run validation.

### 3.2 In a template

Templates ship a full `pyproject.toml` (or under `template/`). Update dependency versions there.

When core supports manifest merge, extensions union dependencies by package name; later layers win on conflicts. See create-python-app `docs/PYPROJECT_MERGE.md`.

### 3.3 Major updates

A major dependency update is high-risk. For each major:

1. Read the changelog or migration guide.
2. Check `requires-python` and transitive requirements.
3. Test with L2 isolation for the affected extension(s) and the relevant curated L3 profile(s).
4. If breaking changes affect generated code, update template `.template` files or extension files.

---

## 4. Lockfiles

Generated projects **do** commit `uv.lock` when the template or extension includes one, but CI smoke tests often run fresh `uv sync` without a pre-existing lock. If a transitive dependency starts breaking installs, consider:

- Pinning the transitive dependency in the template or extension `pyproject.toml`.
- Adding a constraint group or override in `create-python-app` core (see [MAINTENANCE_SECURITY.md](./MAINTENANCE_SECURITY.md)).

Avoid relying on transient PyPI states; pin when reproducibility matters.

---

## 5. Dependabot PRs

### 5.1 Reviewing

```bash
gh pr list --repo Create-Python-App/create-python-app --author dependabot --state open
gh pr list --repo Create-Python-App/cpa-templates --author dependabot --state open
gh pr view <pr> --repo Create-Python-App/<repo>
```

### 5.2 Rebasing if conflicted

```bash
gh pr comment <pr> --repo Create-Python-App/<repo> --body "@dependabot rebase"
```

### 5.3 Merging

Only merge if CI passes. Security-related bumps take priority. If a Dependabot PR fails CI, treat it as a bug fix: reproduce, adjust the dependency range or lockfile, and push to the same PR rather than opening a duplicate.

---

## 6. Tools for complex resolution

```bash
# Why a version was chosen
cd my-app && uv tree --package <pkg>

# Show outdated packages (when lock exists)
cd my-app && uv lock --upgrade-package <pkg> --dry-run

# Verbose sync for debugging
cd my-app && UV_LOG=debug uv sync

# Export resolved requirements
cd my-app && uv export --format requirements-txt
```

---

## 7. Checklist

- [ ] The target version exists on PyPI for every related package.
- [ ] `requires-python` is satisfied across template and extensions.
- [ ] Peer/extra conflicts are resolved or explicitly worked around.
- [ ] The change is scoped to the affected template/extension.
- [ ] Local validation passes (`uv sync`, ruff, pytest).
- [ ] Full matrix passes for affected templates.
- [ ] If security-related, the CVE is actually addressed by the bump.
