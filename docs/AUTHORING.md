# Authoring Templates and Extensions

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

## `cpa.config.json`

Defines interactive CLI prompts. Answers become scaffold / Jinja variables; in CI/non-interactive mode, defaults are used.

```json
{
  "name": "my-template",
  "customOptions": [
    {
      "key": "apiPrefix",
      "type": "string",
      "message": "API URL prefix",
      "default": "/api/v1"
    }
  ]
}
```

| Field | Description |
|---|---|
| `key` | Option identifier (becomes a scaffold variable) |
| `type` | Prompt type (`string`, etc.) |
| `message` | Question shown in the CLI |
| `default` | Default when non-interactive (`CI=true`) |

> Co-locate `cpa.config.json` with the template so it works with both slug resolution and `file://` local URLs.

## Naming conventions (parity with cna-templates)

| Prefer | Avoid |
|--------|--------|
| `compose.yml` / `compose.prod.yml` | `docker-compose.yml` |
| `docker/<engine>/compose.yml` for DB services | Root `docker-compose.*.yml` overlays only |
| `.dockerignore` next to `Dockerfile` | Omitting ignore rules |
| Extension dir that matches the files you ship | Mixing unrelated stacks in one extension |

Compose is invoked as `docker compose -f compose.yml …` (Compose V2 file naming).

## Extension layout

Extensions add files on top of a compatible template.

Example — Docker (mirrors `react-compose` file names):

```
extensions/python-docker/
├── Dockerfile
├── .dockerignore
├── compose.yml
├── compose.prod.yml
└── README.md
```

Example — Postgres (mirrors `nestjs-drizzle-postgres` path):

```
extensions/python-postgres/
├── docker/postgres/compose.yml
├── docker/postgres/.env.example
└── README.md
```

Until pyproject merge lands in `create-python-app-core`, prefer adding new files over shipping a full replacement `pyproject.toml`.

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
  "url": "https://github.com/Create-Python-App/cpa-templates?subdir=extensions/github-setup",
  "type": ["fastapi-backend"],
  "category": "tooling",
  "labels": ["GitHub", "CI", "DevOps"]
}
```

## File conventions (create-python-app-core)

| Suffix | Behavior |
|---|---|
| `.template` | Jinja2 processing, suffix stripped (when core supports it) |
| `.append` | Content appended to the matching file |
| `[name]/` | Directory renamed from `customOptions` answer (planned) |

Use static files when the core version you target does not yet process a suffix.
