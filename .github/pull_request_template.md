## Description

<!-- Summary of changes and related issue. List any dependencies required for this change. -->
Fixes # (issue)

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New template or extension
- [ ] Enhancement (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] CI / tooling

## How Has This Been Tested?

<!-- Describe tests that verify your changes. Provide reproduction instructions. -->

- [ ] `python scripts/ci/validate-registry.py`
- [ ] `python scripts/ci/generate-matrix.py --layer validate-profiles`
- [ ] Scaffolded template(s) locally (`uvx create-awesome-python-app --template file://...`)
- [ ] `uv run ruff check .` / `uv run mypy .` / `uv run pytest` in generated project (if applicable)

## Checklist

- [ ] Directory name matches the `slug` in `templates.json`
- [ ] `url` points to the correct path on the `main` branch
- [ ] `slug` is globally unique across templates and extensions
- [ ] All required fields present: `name`, `slug`, `description`, `url`, `type`, `category`, `labels`
- [ ] Extension `type` is an array if it supports multiple template types
- [ ] I have performed a self-review of my code
- [ ] I have made corresponding changes to the documentation
- [ ] New and existing checks pass locally
