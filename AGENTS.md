# AGENTS.md

This repo is the template and extension bank for [create-awesome-python-app](https://github.com/Create-Python-App/create-python-app).

## Key concepts

- **`templates.json`** — single registry of all templates, extensions, and categories. Every entry needs `name`, `slug`, `description`, `url`, `type`, `category`, `labels`. Slugs must be globally unique.
- **`type`** — links templates to extensions. A template has one type string; extensions list one or more compatible types. Only matching extensions appear when a template is selected.
- **`cpa.config.json`** — lives in the template directory, defines `customOptions` (interactive CLI prompts). Answers become scaffold variables for future templating support.
- **`template/` subdirectory** — optional; when present, CPA copies from `template/` instead of the template root.
- **Copy-only merge** — Prefer new files; core is adding Jinja `.template`, `.append`, and `pyproject.toml` merge.

## How to test

```sh
# Scaffold from a local checkout (CI=1 uses customOptions defaults)
CI=true uv run create-awesome-python-app my-app \
  --template "file://$PWD?subdir=templates/fastapi-starter" \
  --no-interactive
cd my-app && uv sync && uv run pytest

# Add a local extension
CI=true uv run create-awesome-python-app my-app \
  --template "file://$PWD?subdir=templates/fastapi-starter" \
  --addons "file://$PWD?subdir=extensions/github-setup" \
  --no-interactive
```

See [docs/TESTING.md](./docs/TESTING.md) for more examples and CI details.

## Docs

| File | Contents |
|---|---|
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System overview, type system, generation flow |
| [docs/AUTHORING.md](./docs/AUTHORING.md) | Directory layout, `cpa.config.json`, extensions |
| [docs/TESTING.md](./docs/TESTING.md) | Local testing commands and CI workflow |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to add templates and extensions |
