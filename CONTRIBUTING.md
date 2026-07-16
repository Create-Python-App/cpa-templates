# Contributing

Thanks for contributing! This repo powers [create-awesome-python-app](https://github.com/Create-Python-App/create-python-app).

For a full explanation of how templates, extensions, and the file system work, read [docs/AUTHORING.md](./docs/AUTHORING.md).

## Adding an extension

1. Create `extensions/<your-slug>/`
2. Add files to copy into the generated project (use `template/` if you only want a subset copied)
3. Register it in `templates.json` under `"extensions"`:

```json
{
  "name": "My Extension",
  "slug": "my-extension",
  "description": "Adds X to your project",
  "url": "https://github.com/Create-Python-App/cpa-templates/tree/main/extensions/my-extension",
  "type": ["fastapi-backend"],
  "category": "tooling",
  "labels": ["FastAPI", "Tooling"]
}
```

## Adding a template

1. Create `templates/<your-slug>/` with a `pyproject.toml` (and optional `template/` subdirectory)
2. Add `cpa.config.json` for interactive options when needed
3. Register it in `templates.json` under `"templates"` (same fields as extensions)

## Commit messages

Use [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.

## PR checklist

- [ ] Directory name matches the `slug` in `templates.json`
- [ ] `url` points to the correct path on the `main` branch
- [ ] `slug` is globally unique across templates and extensions
- [ ] All required fields present: `name`, `slug`, `description`, `url`, `type`, `category`, `labels`
- [ ] Extension `type` is an array if it supports multiple template types
- [ ] Tested locally — see [docs/TESTING.md](./docs/TESTING.md)

## Questions?

Open an [issue](https://github.com/Create-Python-App/cpa-templates/issues) or start a [discussion](https://github.com/Create-Python-App/cpa-templates/discussions).
