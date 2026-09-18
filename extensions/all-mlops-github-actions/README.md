# All MLOps GitHub Actions (extension bank)

Maintainer-facing notes for the **all-mlops-github-actions** extension in `cpa-templates`.

## Compatible types

| Template type | Compatible? | Notes |
|---------------|-------------|-------|
| `mlops-sklearn` | ✅ Yes | Uses the `mlops-train --config <path>` entrypoint contract |
| `mlops-pytorch` | 🔜 Planned | Gains this type when the PyTorch starter lands (#85) |
| `mlops-tensorflow` | 🔜 Planned | Gains this type when the TensorFlow starter lands (#86) |

## Copied into generated projects (via `template/`)

| Path | Purpose |
|------|---------|
| `.github/workflows/mlops-ci.yml` | Lint + pytest + pipeline smoke on push/PR |
| `docs/MLOPS_GITHUB_ACTIONS_GUIDE.md` | Long-form guide for the generated project |

The bank `README.md` (this file) stays **outside** `template/` so it does not
overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-ml \
  --template mlops-sklearn-starter \
  --addons all-mlops-github-actions \
  --no-interactive
```
