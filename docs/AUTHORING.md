# Authoring Templates and Extensions

Guide for contributors adding or updating templates and extensions in `cpa-templates`. Parity reference: [cna-templates AUTHORING.md](https://github.com/Create-Node-App/cna-templates/blob/main/docs/AUTHORING.md).

## Template directory layout

```
my-template/
├── cpa.config.json       # Optional interactive prompts
├── pyproject.toml        # Project manifest (uv)
├── app/                  # Application code
├── tests/
└── README.md
```

You may also use a `template/` subdirectory; CPA copies from `template/` when it exists:

```
my-template/
├── cpa.config.json
└── template/
    ├── pyproject.toml
    └── app/
```

### `pyproject.toml` as the manifest

Unlike CNA templates that export `package/index.js`, CPA templates ship a **`pyproject.toml`** at the template root (or under `template/`). The CLI runs `uv sync` after generation.

Extensions may ship a **partial** `pyproject.toml` with only the keys they add (for example, a database driver). CPA merges overlays instead of overwriting — see [pyproject merge](#pyprojecttoml-merge) below.

## `cpa.config.json`

Defines interactive CLI prompts. Answers become scaffold / Jinja variables; in CI or non-interactive mode, defaults are used.

```json
{
  "name": "my-template",
  "customOptions": [
    {
      "key": "apiPrefix",
      "type": "string",
      "message": "API URL prefix",
      "default": "/api/v1"
    },
    {
      "key": "enableCors",
      "type": "boolean",
      "message": "Enable CORS middleware",
      "default": true
    }
  ]
}
```

| Field | Description |
|---|---|
| `key` | Option identifier (becomes a Jinja variable and matches `[key]/` directories when bracket renaming is enabled) |
| `type` | Prompt type (`string`, `boolean`, etc.) |
| `message` | Question shown in the CLI |
| `default` | Default when non-interactive (`CI=true`) |

> Co-locate `cpa.config.json` with the template so it works with both slug resolution and `file://` local URLs.
> Do **not** put `customOptions` in `templates.json` — it is only read from `cpa.config.json`.

Schema reference: [create-python-app `docs/cpa-config-schema.md`](https://github.com/Create-Python-App/create-python-app/blob/main/docs/cpa-config-schema.md).

## Jinja2 variables

All `.template` files are processed with Jinja2. The output filename strips the `.template` suffix. Undefined variables **fail the build** (`StrictUndefined`).

| Variable | Source | Example |
|---|---|---|
| `{{ projectName }}` | User input or `--set projectName=...` | `my-api` |
| `{{ apiPrefix }}` | `cpa.config.json` custom option | `/api/v1` |
| `{{ enableCors }}` | `cpa.config.json` custom option | `true` |
| Any `customOptions[].key` | Same as the option key | — |

Example from `fastapi-starter`:

```python
# app/core/config.py.template
api_prefix: str = "{{ apiPrefix }}"
enable_cors: bool = {{ "True" if enableCors | lower in ["1", "true", "yes", "on"] else "False" }}
```

Use Jinja filters and conditionals for booleans and derived values. Prefer explicit defaults in templates over optional variables.

## File conventions (create-python-app-core)

| Suffix | Behavior |
|---|---|
| `.template` | Jinja2 processing (`{{ var }}`), suffix stripped. Undefined vars fail (StrictUndefined). |
| `.append` | Content appended to the matching file already in the project |
| `.append.template` / `.template.append` | Render with Jinja, then append |
| `[name]/` | Directory renamed from `customOptions` answer (planned) |

Static files (no suffix) are copied as-is. Later layers overwrite earlier files on path conflict, except `pyproject.toml` which is merged.

## Naming conventions (parity with cna-templates)

### Compose / Docker file names

| Prefer | Avoid |
|--------|--------|
| `compose.yml` / `compose.prod.yml` | `docker-compose.yml` |
| `docker/<engine>/compose.yml` for DB services | Root `docker-compose.*.yml` overlays only |
| `.dockerignore` next to `Dockerfile` | Omitting ignore rules |

Compose is invoked as `docker compose -f compose.yml …` (Compose V2 file naming).

### Extension folder taxonomy (CNA parity)

**Folder name = coupling truth.** Catalog `slug` may be friendlier than the folder, but never claim universality when the overlay is stack-bound.

| Kind | Folder pattern | Catalog slug | `type` field |
|------|----------------|--------------|--------------|
| Universal | `all-{capability}` | often friendly (`github-setup`, `development-container`, `postgres`) | Broad list of all compatible template types |
| Stack-specific | `{stack}-{capability}` | usually matches folder (`fastapi-docker`, `fastapi-sqlalchemy`) | Only that stack's template `type` |

Examples:

| Folder | Slug | Meaning |
|--------|------|---------|
| `extensions/all-github-setup` | `github-setup` | Portable CI/repo automation |
| `extensions/all-devcontainer` | `development-container` | VS Code Dev Container for any CPA template |
| `extensions/all-postgres` | `postgres` | Infra-only Postgres Compose (no `app/` writes) |
| `extensions/fastapi-docker` | `fastapi-docker` | Dockerfile/Compose with `uvicorn app.main:app` |
| `extensions/django-docker` | `django-docker` | Dockerfile/Compose for Django/`gunicorn` |
| `extensions/celery-docker` | `celery-docker` | Dockerfile/Compose for Celery worker |
| `extensions/fastapi-sqlalchemy` | `fastapi-sqlalchemy` | FastAPI `app/db/` + Alembic |

**Never** use a generic `python-*` folder/slug for overlays that write FastAPI `app/` paths or a FastAPI-only `CMD`.

CI enforces this in `scripts/ci/validate-registry.py`:

- Extension folders must be `all-*`, or `{stack}-*` matching a single `type`
  (see `STACK_PREFIX_BY_TYPE`); `python-*` is rejected.
- Every catalog template must ship the quality-bar docs/files listed below
  (enforced on the maturity tip / after the template uplift PRs land).

### `incompatibleWith` (path collisions)

Use symmetric `incompatibleWith` when two extensions would overwrite the same
generated paths (for example two Docker overlays that both ship `Dockerfile` /
`compose.yml` for the **same** template `type`). Today stack Docker extensions
are isolated by `type`; when a type gains a second packaging strategy, declare
mutual incompatibility like cna-templates does for Redux saga/thunk. Example:
`celery-docker` and the upcoming `flower-docker` (PR #178) both target
`celery-worker` and ship a Compose stack for the same worker type — they must
declare `incompatibleWith` on both entries when `flower-docker` lands (validation
is symmetric; see `scripts/ci/validate-registry.py` and `templates.schema.json`).

**Authoring rules:**

1. **Declare on both sides.** If extension `A` is incompatible with `B`, then `A` must list `B` in its `incompatibleWith` array **and** `B` must list `A` in its `incompatibleWith` array. CPA validates this symmetry at registry load time.
2. **Use slugs, not names.** Reference entries by their `slug` string — not the human-readable `name` — so renames to display names don't silently break validation.
3. **Scope to the narrowest conflict surface.** Only declare incompatibility when the overlay truly overwrites shared paths (e.g. `Dockerfile`, `compose.yml`, `app/core/providers.py`). For softer constraints — version ranges, optional features, shared optional deps — prefer dependency versioning or optional `cpa.config.json` toggles rather than hard incompatibility.
4. **Same `type` first.** Most `incompatibleWith` declarations are within a single template `type` (e.g. two FastAPI Docker strategies). Cross-type incompatibility is rare and should be explicitly justified in the PR description.
5. **Document the rationale.** Record the colliding paths in the PR description, this document (`AUTHORING.md`), or `AI_ML_AUTHORING.md` so future maintainers know whether the constraint can be relaxed. (`templates.json` is strict JSON and does not support inline comments.)

**Checklist for new `incompatibleWith` entries:**

- [ ] Both entries list each other by `slug`
- [ ] Slugs referenced are valid entries in `templates.json`
- [ ] The collision path(s) are documented in the PR, `AUTHORING.md`, or `AI_ML_AUTHORING.md`
- [ ] An existing `incompatibleWith` wasn't already covering the pair
- [ ] If a new packaging strategy was introduced, it was discussed in the issue or Discord first

See [Registering in `templates.json`](#registering-in-templatesjson) for the JSON schema and the `templates.schema.json` validation.

### Template quality bar (every catalog template)

Every template registered in `templates.json` must ship at least:

| Area | Required |
|------|----------|
| Architecture | Feature/module layout appropriate to the stack (not a single flat hello-world module) |
| `docs/` | `README.md`, `PROJECT_STRUCTURE.md`, `CONFIGURATION.md`, `TESTING_GUIDE.md`, `DEPLOYMENT.md`, plus stack docs (e.g. `API.md` for HTTP APIs) |
| Root docs | Strong `README.md` (or `.template`), `AGENTS.md`, `CONTRIBUTING.md`, `.env.example` |
| Tooling | `pyproject.toml` with Ruff + pytest (and stack-native tools); typed Python documented |
| Tests | Real tests under `tests/` that exercise health/core paths |

`fastapi-starter` is the reference implementation. Raise new templates *to* that bar; do not dilute it.

Do **not** add a second FastAPI base template for strict typing. Typing tooling and
`docs/TYPING.md` live in `fastapi-starter` itself. If you need an optional stricter
overlay later, ship a thin `fastapi-strict-typing` **extension**, not a competing starter.

Reference quality bars outside this repo: [cna-templates `react-vite-starter`](https://github.com/Create-Node-App/cna-templates/tree/main/templates/react-vite-starter), [`nestjs-starter`](https://github.com/Create-Node-App/cna-templates/tree/main/templates/nestjs-starter).

## Extension layout

Extensions add files on top of a compatible template. They do **not** define `cpa.config.json` or interactive prompts.

### Prefer `template/` so bank README does not overwrite the project

CPA's loader prefers a `template/` subdirectory when present (`get_template_dir_path`). Put **generated-project artifacts** under `template/`, and keep the **bank-facing** `README.md` at the extension root. That matches Create-Node-App: the catalog README must not clobber the scaffolded project README.

```
extensions/fastapi-docker/
├── README.md                         # bank only (NOT copied)
└── template/
    ├── Dockerfile
    ├── .dockerignore
    ├── compose.yml
    ├── compose.prod.yml
    └── docs/
        ├── DOCKER_GUIDE.md           # long guide for the generated project
        └── README.md.append          # bullet appended into docs/README.md
```

Example — universal Postgres:

```
extensions/all-postgres/
├── README.md                         # bank only
└── template/
    ├── pyproject.toml                # partial — merged into project manifest
    ├── .env.example.append           # appended to template .env.example
    ├── docker/postgres/compose.yml
    ├── docker/postgres/.env.example
    └── docs/
        ├── POSTGRES_GUIDE.md
        └── README.md.append
```

### Docs convention (parity with cna-templates)

Every extension that teaches the generated project should ship:

| Path (under `template/` when using that pattern) | Role |
|---|---|
| `docs/<TOPIC>_GUIDE.md` | Long-form guide: Overview, What it adds, Usage, Configuration, Verification, Troubleshooting, Resources |
| `docs/README.md.append` | One bullet linking the guide into the project's `docs/README.md` index |

**Most common code pattern** — a partial `pyproject.toml` with deps to merge (under `template/`):

```toml
[project]
dependencies = [
  "psycopg[binary]>=3.2",
]
```

Everything under the copied root (`template/` or extension root) is copied into the project, respecting all file suffix conventions above.

### Typed Python is the default

New and updated **templates** should treat typed Python as the default quality bar:

- Annotate public APIs; use Pydantic models at boundaries
- Document mypy and/or pyright in README / `docs/TYPING.md` / CI
- Prefer shipping typing tooling in `pyproject.toml` dependency groups when practical

Extensions should not undo typing (avoid untyped overlays that fight strict checking).
## Extension auto-wiring

Extensions that contribute runtime behaviour (middleware, routers, instrumentation) use the existing `.append` / `.append.template` mechanism to wire themselves into the generated project automatically. No manual edits to the base template files are needed.

Two patterns cover all current use cases.

### FastAPI — provider registry

The `fastapi-starter` base template ships `app/core/providers.py` with a lightweight registry:

```python
# app/core/providers.py (generated)
AppProvider = Callable[[FastAPI], None]
_providers: list[AppProvider] = []

def register(fn: AppProvider) -> AppProvider: ...
def setup_app(app: FastAPI) -> None: ...
```

`app/main.py` calls `setup_app(app)` once, after base middleware is configured.

Extensions register their setup function by adding `template/app/core/providers.py.append.template`. Use the `@register` decorator with a lazy import to avoid ruff E402 (import-not-at-top):

```python
# extensions/fastapi-cors/template/app/core/providers.py.append.template

@register
def _cors(app: FastAPI) -> None:  # registered last — CORS wraps all others
    from app.core.cors import setup_cors
    setup_cors(app)
```

**Ordering:** providers are called in the order they are appended (scaffold addon order). Because FastAPI's `add_middleware` is LIFO, middleware added last becomes the outermost wrapper — `fastapi-cors` must be the last extension in the addon list when ordering matters.

### FastAPI — feature router registration

Feature extensions (auth, chat, …) add `template/app/api/router.py.append`:

```python
# extensions/fastapi-auth-jwt/template/app/api/router.py.append
from app.features.auth.router import router as auth_router
router.include_router(auth_router)
```

`router` is already defined in `app/api/router.py` before the appended content runs.

### Django — settings and URL append

Django loads `settings.py` as a Python module, so list concatenation and dict mutation are valid at module scope. Extensions append to `config/settings.py` and `config/urls.py`:

```python
# extensions/django-spectacular/template/config/settings.py.append
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
```

```python
# extensions/django-spectacular/template/config/urls.py.append
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
urlpatterns += [
    path(f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"),
    ...
]
```

`urlpatterns` and `api_prefix` are already defined in the base `urls.py`.

### Checklist additions for auto-wired extensions

- [ ] Append file targets a path that exists in the base template
- [ ] The append file contains only the minimal wiring or configuration — no logic already in the helper module (a `@register` call for FastAPI providers, `router.include_router()` for FastAPI routers, or a `+=` / dict-mutation statement for Django settings/URLs)
- [ ] For FastAPI middleware extensions that call `app.add_middleware()`, verify the extension is listed last in the addon order in CI profiles (last registered = outermost middleware via FastAPI's LIFO rule)

## `pyproject.toml` merge

When scaffolding layers include a `pyproject.toml`, CPA **merges** into the destination file instead of overwriting it.

| Key | Behavior |
|-----|----------|
| `[project].dependencies` | Union by package name; **later layer wins** on version conflict |
| `[project].optional-dependencies.*` | Same union-per-group |
| `[dependency-groups].*` | Same union-per-group (uv) |
| Nested tables (`[tool.ruff]`, etc.) | Deep merge; scalars: later wins |
| Other arrays | Later layer replaces |

Base template:

```toml
[project]
name = "my-api"
dependencies = ["fastapi>=0.115"]
```

Extension overlay:

```toml
[project]
dependencies = ["psycopg[binary]>=3.2"]

[dependency-groups]
dev = ["ruff>=0.8"]
```

Result keeps `name`, unions dependencies, and adds the dev group.

Full reference: [create-python-app `docs/PYPROJECT_MERGE.md`](https://github.com/Create-Python-App/create-python-app/blob/main/docs/PYPROJECT_MERGE.md).

## Registering in `templates.json`

### Template entry

```json
{
  "name": "FastAPI Starter",
  "slug": "fastapi-starter",
  "description": "Production-ready FastAPI API with uv, ruff, and pytest",
  "url": "https://github.com/Create-Python-App/cpa-templates?subdir=templates/fastapi-starter",
  "type": "fastapi-backend",
  "category": "backend-applications",
  "labels": ["FastAPI", "API", "Python", "uv"]
}
```

### Extension entry

```json
{
  "name": "GitHub Setup",
  "slug": "github-setup",
  "description": "GitHub Actions CI, issue templates, and Dependabot",
  "url": "https://github.com/Create-Python-App/cpa-templates?subdir=extensions/all-github-setup",
  "type": ["fastapi-backend", "django-backend", "cli-app", "celery-worker", "uv-workspace"],
  "category": "ci",
  "labels": ["GitHub", "CI", "DevOps"]
}
```

### Type compatibility

- A template has **one** `type` string.
- An extension has a `type` string **or array** of strings.
- An extension is compatible when `template.type` appears in `[extension.type].flat()`.

### `incompatibleWith` — when and how

Use `incompatibleWith` when two extensions would write the same file for the same `type` — e.g. `Dockerfile`, `compose.yml`, `.env.example`, or `pyproject.toml` overlay. Example: `celery-docker` vs `flower-docker` both target `celery-worker` and ship a Compose stack for the same worker (similarly, two FastAPI middleware extensions that both patch `app/core/providers.py`).

- **Symmetric (required):** if `A` lists `B`, then `B` must list `A`. Validated by [`scripts/ci/validate-registry.py`](../scripts/ci/validate-registry.py) (symmetry + existence).
- **Same `type` only:** both extensions must share the same `type` (e.g. `celery-worker`). Cross-type is rare and needs justification.
- **Slugs, not names:** reference the `slug` field.

```json
{
  "slug": "flower-docker",
  "incompatibleWith": ["celery-docker"]
},
{
  "slug": "celery-docker",
  "incompatibleWith": ["flower-docker"]
}
```

- **Validation:** `python scripts/ci/validate-registry.py` fails on unknown or asymmetric slugs.
- **Testing:** L2 fails if both extensions are selected together (combination rejected at scaffold time).
- **Schema:** [`templates.schema.json`](../templates.schema.json) → `extensions[].incompatibleWith`.

See also the [path-collision rules](#incompatiblewith-path-collisions) above.

## Generation order

1. Resolve template + extension URLs from `templates.json` (or `file://` / GitHub URL).
2. Clone or open source directories (cached under `~/.cache/cpa` for remote repos).
3. For each layer, copy from `template/` when present, otherwise from the layer root.
4. Process `.template`, `.append`, and related suffix files.
5. Merge `pyproject.toml` across layers.
6. Run `uv sync` when `pyproject.toml` exists (unless `--no-install`).
7. Initialize git (unless `CPA_SKIP_GIT=1`).

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full system overview.

## Testing locally

Point the CLI at a local checkout:

```sh
export CPA_TEMPLATES_URL="file:///path/to/cpa-templates"

uvx create-awesome-python-app my-app \
  --template fastapi-starter \
  --addons github-setup fastapi-docker \
  --yes
```

Verify generated output: `uv sync`, `uv run ruff check .`, `uv run pytest`, and any extension-specific checks documented in each extension README.

## Checklist for new templates

- [ ] `cpa.config.json` co-located with template (if prompts needed)
- [ ] `pyproject.toml` with valid uv project metadata
- [ ] Feature/module architecture (not a flat hello-world)
- [ ] Typed Python documented (and tooling configured when ready): mypy / pyright
- [ ] `.template` files use only defined Jinja variables
- [ ] Entry added to `templates.json` with correct `type` and `category`
- [ ] README + CONTRIBUTING + AGENTS + full `docs/` suite (see quality bar above)
- [ ] Local scaffold smoke test passes

## Checklist for new extensions

- [ ] Folder follows `all-*` or `{stack}-*` taxonomy (no misleading `python-*` for stack-bound code)
- [ ] Compatible `type`(s) match target template(s) — broad only when truly portable
- [ ] Artifacts under `template/`; bank `README.md` outside (does not overwrite project README)
- [ ] `docs/<TOPIC>_GUIDE.md` + `docs/README.md.append` for generated-project docs
- [ ] Partial `pyproject.toml` only when adding dependencies
- [ ] `.append` / `.append.template` files target paths that exist in the base template (use provider registry or router append for runtime wiring — see [Extension auto-wiring](#extension-auto-wiring))
- [ ] Compose files follow `compose.yml` / `docker/<engine>/` conventions
- [ ] `incompatibleWith` defined for mutually exclusive extensions
- [ ] Bank README covers when to use, what is copied, and verification pointers
- [ ] Entry added to `templates.json` (`url` subdir matches folder name)

## Future templates

Planned starters not yet in the registry are listed in [FUTURE_TEMPLATES.md](./FUTURE_TEMPLATES.md).

## AI/ML catalog

For AI/ML taxonomy, categories, and template-vs-extension rules see
[AI_ML_AUTHORING.md](./AI_ML_AUTHORING.md). MLOps templates and extensions must
also follow the shared feature-module, testing, CI-profile, environment, and
composition contract in [MLOPS_CONTRACT.md](./MLOPS_CONTRACT.md).
