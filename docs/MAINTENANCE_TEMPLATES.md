# Maintenance: Templates and Extensions

> How to inspect, fix, add, and update templates and extensions in `cpa-templates`.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Core concepts

These are defined in `AGENTS.md` and `docs/ARCHITECTURE.md`; the critical points are repeated here because they drive almost every maintenance decision.

### 1.1 Registry

- `templates.json` is the single registry of templates, extensions, and categories.
- `templates.schema.json` validates the registry.
- Every template/extension needs: `name`, `slug`, `description`, `url`, `type`, `category`, `labels`.
- Extensions may also have `incompatibleWith` to declare mutually exclusive extensions.

### 1.2 Type system

- A template has **one** `type` string.
- An extension has a `type` string **or array** of strings.
- An extension is compatible with a template when `template.type` is in `[ext.type].flat()`.

### 1.3 File conventions

| Convention | Behavior |
|---|---|
| `pyproject.toml` | Project manifest; extensions may ship partial manifests merged by core |
| `cpa.config.json` | Defines `customOptions` for interactive CLI prompts |
| `template/` subdirectory | When present, CPA copies from here instead of the layer root |
| `*.template` | Processed with Jinja2; output filename strips `.template` |
| `*.append` | Content is appended to the matching file in the project |
| `[name]/` directory | Renamed to the value of the `name` custom option (planned) |

### 1.4 Scaffold variables

Common variables available in `.template` files:

| Variable | Source |
|---|---|
| `{{ projectName }}` | User input or `--set projectName=...` |
| `{{ apiPrefix }}` | `cpa.config.json` custom option default or answer |
| Other keys | Each `customOptions[].key` in `cpa.config.json` |

In CI/non-interactive mode (`CI=true`), defaults from `cpa.config.json` are used.

### 1.5 Generation order

1. Resolve template + extension URLs from `templates.json`.
2. Copy template files (from `template/` when present).
3. Process `.template`, `.append`, and related suffixes as core supports them.
4. Rename `[bracket]/` directories based on `customOptions` (planned).
5. Merge `pyproject.toml` across layers (union deps; later wins on conflicts).
6. Run `uv sync` when `pyproject.toml` exists (unless `--no-install`).
7. Initialize git (unless `CPA_SKIP_GIT=1`).

---

## 2. How to inspect an existing template

```bash
cd repos/github.com/Create-Python-App/cpa-templates

# List templates
ls templates/

# Read the registry entry
grep -A 15 '"slug": "fastapi-starter"' templates.json

# Read the manifest
cat templates/fastapi-starter/pyproject.toml

# Read custom options
cat templates/fastapi-starter/cpa.config.json
```

Key questions:

- What `type` does it have?
- What `customOptions` does it define?
- What scripts and dev dependencies does `pyproject.toml` declare?
- Is there a `template/` subdirectory?

---

## 3. How to inspect an existing extension

```bash
# List extensions
ls extensions/

# Read the registry entry
grep -A 15 '"slug": "fastapi-docker"' templates.json

# Read partial manifest and files
cat extensions/fastapi-docker/pyproject.toml
ls -la extensions/fastapi-docker
```

Key questions:

- Which `type`s is it compatible with?
- Does it add dependencies that conflict with other extensions when merged?
- Does it have `.template` files needing scaffold variables?
- Does it have `.append` files that modify existing template files?

---

## 4. Fixing ruff / pytest / type errors in generated projects

When a generated project fails `ruff check`, `pytest`, or type checking, the cause is usually in the template or an extension.

### 4.1 Reproduce locally

```bash
REPO=/absolute/path/to/cpa-templates
CI=true uvx create-awesome-python-app@latest my-app \
  --template "file://$REPO?subdir=templates/<slug>" \
  --addons "file://$REPO?subdir=extensions/<ext1>" \
  --no-interactive

cd my-app
uv sync
uv run ruff check .
uv run pytest -q
```

### 4.2 Isolate the offending extension

Remove extensions one at a time until the project passes. Then fix the last removed extension.

### 4.3 Common fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Import error in tests | Missing dependency in merged `pyproject.toml` | Add dep to template or extension manifest |
| Ruff `F401` / style errors | Generated imports or config mismatch | Fix template source or ruff config |
| Pydantic validation error | Settings model vs env example mismatch | Align `.env.example` and settings class |
| pytest collection failure | Wrong test path or missing plugin | Fix `[tool.pytest.ini_options]` in template |
| `uv sync` conflict | Two extensions pin incompatible versions | Align versions or use `incompatibleWith` |

---

## 5. Adding or modifying a template

### 5.1 Adding a template

1. Create `templates/<directory>/`.
2. Add `pyproject.toml` and application source files (under `template/` if you prefer).
3. Add `cpa.config.json` with `customOptions` if interactive prompts are needed.
4. Add an entry to `templates.json` under `templates`.
5. Ensure the `url` matches the directory structure (`?subdir=templates/<directory>`).
6. Run local validation against the new template.
7. After merge, confirm L1 (and L2 if applicable) are green on `main`.

### 5.2 Directory naming caveat

The directory name in `templates/` and the slug in `templates.json` may differ. The CLI resolves via `url`, not slug. When generating locally with `file://`, use the directory name:

```bash
--template "file://$REPO?subdir=templates/fastapi-starter"
```

### 5.3 Modifying a template

1. Re-scaffold the template with a representative set of extensions.
2. Apply the change.
3. Validate ruff and pytest.
4. Re-scaffold with the relevant **curated L3 profile** (or L2 isolation for each touched extension) — do not stack every extension at once.

---

## 6. Adding or modifying an extension

### 6.1 Adding an extension

1. Create `extensions/<slug>/`.
2. Add a partial `pyproject.toml` with dependencies and optional scripts to merge.
3. Add files, templates, or appends as needed.
4. Add the extension to `templates.json` under `extensions`.
5. Set `type` to match compatible template types.
6. Set `category` so curated L3 profiles can pick one extension per category (`ci`, `containers`, `database`, `editor`, …).
7. Define `incompatibleWith` if it cannot coexist with other extensions.
8. Validate locally with **each** compatible template (L2-style isolation).
9. Confirm L2/L3 stay green after merge.

### 6.2 Modifying an extension

1. Identify all templates compatible with the extension (`type` match).
2. Test the extension against **at least one** template locally.
3. If the change affects dependencies, also test the relevant curated L3 profile(s) for that template — not an all-extensions stack.

---

## 7. Handling incompatible extensions

When two extensions cannot be used together, declare it explicitly.

### 7.1 Via `incompatibleWith`

In `templates.json`, add `incompatibleWith` to both extensions:

```json
{
  "slug": "extension-a",
  "incompatibleWith": ["extension-b"]
}
```

The CI profile validator and L2 isolation honor `incompatibleWith`. Do not rely on stacking every extension.

### 7.2 Via dependency constraints

If the incompatibility is only a version-resolution issue at `uv sync` time, aligning pins in `pyproject.toml` may be enough. Prefer that when both extensions are logically compatible but declare overlapping deps at different versions.

### 7.3 Decision matrix

| Situation | Use |
|---|---|
| Extensions logically conflict (e.g., two ORM choices) | `incompatibleWith` |
| Version disagreement that resolves with aligned pins | Update `pyproject.toml` in the owning extension |
| Extension breaks a specific template but works elsewhere | Fix template-specific files or narrow `type` |
| Extension is obsolete | Remove from `templates.json` or archive |

---

## 8. Updating dependencies inside a template or extension

1. Open the relevant `pyproject.toml`.
2. Use `uv pip index versions <pkg>` or PyPI JSON to find the latest compatible version.
3. Update the range conservatively (prefer bounded minors, not arbitrary majors).
4. Re-scaffold locally and run validation.
5. If the update is security-related, also read [MAINTENANCE_SECURITY.md](./MAINTENANCE_SECURITY.md).

See [MAINTENANCE_DEPENDENCIES.md](./MAINTENANCE_DEPENDENCIES.md) for deeper dependency troubleshooting.

---

## 9. Local validation command

Use this exact sequence after every template or extension change:

```bash
REPO=/absolute/path/to/cpa-templates
CI=true uvx create-awesome-python-app@latest my-app \
  --template "file://$REPO?subdir=templates/<slug>" \
  --addons "file://$REPO?subdir=extensions/<ext1>" \
         "file://$REPO?subdir=extensions/<ext2>" \
  --no-interactive

cd my-app
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

If any step fails, fix the template or extension, then regenerate from scratch. Do not reuse `my-app` between attempts because files are merged, not reset.

---

## 10. Checklist

- [ ] Registry entry is valid against `templates.schema.json`.
- [ ] `type` matches between template and compatible extensions.
- [ ] `category` is set to avoid random CI selecting duplicates.
- [ ] `incompatibleWith` is defined for mutually exclusive extensions.
- [ ] `.template` files use available scaffold variables.
- [ ] Local validation passes.
- [ ] Risky changes are covered by L2 isolation + relevant L3 profile(s), not an all-extensions stack.

## Quality checklist

See [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md) for the FastAPI M1 bar and per-template `QUALITY.md` files.
