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

CI enforces this in `scripts/ci/validate-registry.py`: folders must be `all-*`, or
`{stack}-*` matching the extension's single `type` (see `STACK_PREFIX_BY_TYPE`).

### `incompatibleWith` (path collisions)

Use symmetric `incompatibleWith` when two extensions would overwrite the same
generated paths (for example two Docker overlays that both ship `Dockerfile` /
`compose.yml` for the **same** template `type`). Today stack Docker extensions
are isolated by `type`; when a type gains a second packaging strategy, declare
mutual incompatibility like cna-templates does for Redux saga/thunk.

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

### `incompatibleWith`

Declare mutually exclusive extensions in `templates.json`. CPA validates selected combinations at scaffold time.

```json
{
  "name": "Example A",
  "slug": "example-a",
  "incompatibleWith": ["example-b"],
  "...": "..."
}
```

When two extensions logically conflict (two middleware choices, two container runtimes), add `incompatibleWith` on **both** entries. Use this for logical conflicts; use semver or dependency constraints for softer peer restrictions.

Schema: `templates.schema.json` → `extensions[].incompatibleWith`.

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
- [ ] `.append` files target paths that exist in the base template
- [ ] Compose files follow `compose.yml` / `docker/<engine>/` conventions
- [ ] `incompatibleWith` defined for mutually exclusive extensions
- [ ] Bank README covers when to use, what is copied, and verification pointers
- [ ] Entry added to `templates.json` (`url` subdir matches folder name)

## Future templates

Planned starters not yet in the registry are listed in [FUTURE_TEMPLATES.md](./FUTURE_TEMPLATES.md).
