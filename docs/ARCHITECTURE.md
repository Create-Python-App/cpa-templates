# Architecture

## How the system works

A user runs:

```sh
uvx create-awesome-python-app --template <slug> --addons <ext1> <ext2>
```

CPA resolves each slug to a `url` in `templates.json`, downloads the directories, merges them with copy-only semantics, and writes the final project to disk. The merge order is: base template files → each extension in order (later layers overwrite).

## `templates.json` structure

Three top-level keys: `categories`, `templates`, `extensions`.

Every template and extension requires: `name`, `slug`, `description`, `url`, `type`, `category`, `labels`.

Interactive options live in `cpa.config.json` inside the template directory (not in `templates.json`).

## The type system

`type` connects templates to extensions. A template has a single string type. An extension has a string or array of strings. An extension is compatible with a template when the template's type appears in the extension's type list.

```
compatible = [ext.type].flat().includes(template.type)
```

### Template types

| Slug | Type |
|---|---|
| `fastapi-starter` | `fastapi-backend` |

## Generation flow

1. Resolve `url` for template and each selected extension from `templates.json` (or `file://` / GitHub URL)
2. Clone or open the source directory (cached under `~/.cache/cpa` for remote repos)
3. For each layer, copy files from `template/` subdirectory when present, otherwise from the layer root
4. Run `uv sync` when `pyproject.toml` exists (unless `--no-install`)
5. Initialize a git repository (unless `CPA_SKIP_GIT=1`)

### Current limitations (vs CNA)

| Feature | CNA | CPA |
|---------|-----|-----|
| EJS / Jinja `.template` files | EJS | Jinja2 in create-python-app-core (rolling out) |
| `.append` files | Yes | Rolling out in core |
| Manifest merge for extensions | `package/index.js` | `pyproject.toml` merge in core (rolling out) |
| Bracket `[dir]/` renaming | Yes | Planned |

Compose file naming matches CNA: prefer `compose.yml`, not `docker-compose.yml`.

## Repository layout

```
cpa-templates/
├── templates.json          # Registry (served to CLI via raw GitHub URL)
├── templates.schema.json   # JSON Schema for templates.json
├── templates/              # Base project starters
├── extensions/             # Optional layers
└── docs/                   # Authoring and testing guides
```

## Related repositories

- **create-python-app** — CLI monorepo (`create-awesome-python-app`, `create-python-app-core`)
- **cpa-templates** (this repo) — template and extension bank
