# Django Spectacular (extension bank)

Maintainer-facing notes for the **django-spectacular** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `drf-spectacular` into project dependencies |
| `docs/SPECTACULAR_GUIDE.md` | Long-form guide for the generated project |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template django-api \
  --addons django-spectacular \
  --yes
```

## Verify after scaffold

See `template/docs/SPECTACULAR_GUIDE.md` for full manual wiring instructions.
