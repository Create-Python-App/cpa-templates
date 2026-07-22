# MLOps GitHub Actions guide

Workflows added:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `mlops-ci.yml` | push/PR | `uv sync` + pytest |
| `mlops-train.yml` | manual | Continuous training |
| `mlops-model-gate.yml` | manual | Quality gate via tests |
| `mlops-deploy.yml` | manual | Deploy stub |

All jobs are CPU-only by default.
