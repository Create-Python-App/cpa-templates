# FastAPI template quality (M1)

Track the maturity bar for `fastapi-starter` (typed by default).

The template ships a local [`QUALITY.md`](../templates/fastapi-starter/QUALITY.md)
checklist. Maintainers should keep that file in sync when acceptance criteria change.

## Verification

```bash
# L1 alone (templates are auto-included from templates.json)
python scripts/ci/generate-matrix.py --layer templates

# Manual scaffold check (uses published CLI via uvx)
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/fastapi-starter"
```

## Related issues

- cpa-templates#49 — FastAPI M1 maturity checklist
- cpa-templates#46 / #47 — layered CI trust
- cpa-templates#57 — typed tooling unified into `fastapi-starter`
