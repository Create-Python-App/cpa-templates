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

Defines interactive CLI prompts. Answers are stored for future templating support; in CI/non-interactive mode, defaults are used.

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

## Extension layout

Extensions add files on top of a compatible template. Because CPA currently uses copy-only merge:

- Prefer adding new files (`.github/workflows`, `Dockerfile`, etc.)
- When overriding `pyproject.toml`, include the full merged content or document that users must reconcile manually until pyproject merge lands in core

Example extension:

```
extensions/python-docker/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

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

## Future conventions (planned in create-python-app core)

| Suffix | Behavior (planned) |
|---|---|
| `.template` | Jinja2 processing, suffix stripped |
| `.append` | Content appended to matching file |
| `[name]/` | Directory renamed from `customOptions` answer |

Until those land, author static files only.
