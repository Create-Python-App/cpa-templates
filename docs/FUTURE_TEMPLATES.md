# Future Templates

Planned templates and extensions not yet fully matured in `templates.json`. See open issues in [Create-Python-App/cpa-templates](https://github.com/Create-Python-App/cpa-templates/issues).

## Shipped (initial)

| Slug | Type | Status |
|------|------|--------|
| `cli-starter` | `cli-app` | Initial template landed (#37) |
| `celery-worker` | `celery-worker` | Initial template landed (#37) |

## Still planned

| Slug | Type (proposed) | Description | Phase |
|------|-----------------|-------------|-------|
| `django-api` | `django-backend` | Django REST / API starter | see #50 |

## Notes

- New templates must pass layered CI (L0–L3) with `uvx` from PyPI.
- Extend extension `type` arrays when a template should accept existing addons.
- Before adding more templates, read [AUTHORING.md](./AUTHORING.md) and [TESTING.md](./TESTING.md).
