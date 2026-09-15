# MLOps template quality (M1)

Track the maturity bar for `mlops-sklearn-starter`, `mlops-pytorch-starter`,
and `mlops-tensorflow-starter` (typed by default, per
[MLOPS_CONTRACT.md](./MLOPS_CONTRACT.md)).

Each template ships a local `QUALITY.md` checklist:

- [`mlops-sklearn-starter`](../templates/mlops-sklearn-starter/QUALITY.md)
- [`mlops-pytorch-starter`](../templates/mlops-pytorch-starter/QUALITY.md)
- [`mlops-tensorflow-starter`](../templates/mlops-tensorflow-starter/QUALITY.md)

Maintainers should keep those files in sync when acceptance criteria change.

## Verification

```bash
# L1 alone (templates are auto-included from templates.json)
python scripts/ci/generate-matrix.py --layer templates

# Manual scaffold checks (uses published CLI via uvx)
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/mlops-sklearn-starter"
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/mlops-pytorch-starter"
python scripts/ci/run-scaffold-check.py \
  --template-url "file://$PWD?subdir=templates/mlops-tensorflow-starter"
```

## Related issues

- cpa-templates#223 — MLOps M1 maturity checklist
- cpa-templates#83 — MLOps template contract (layout, `BaseStep`, required docs)
- cpa-templates#71 — parent MLOps epic
- cpa-templates#87 — `all-mlops-github-actions` extension (CI/CD quality gates)
