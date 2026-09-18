# Deployment

This template ships both serving modes from
[MLOPS_CONTRACT.md](https://github.com/Create-Python-App/cpa-templates/blob/main/docs/MLOPS_CONTRACT.md)'s
serving policy:

- **Batch**: `uv run mlops-predict --input features.csv`
- **FastAPI**: `uv run uvicorn mlops_sklearn.serving.app:app`, then
  `POST /predict` with `{"features": [[...], ...]}`

Both load the registered model **by URI** — they never retrain. Default URI
is `models:/<experiment_name>@production`.

## Promoting a trained version

Training (`uv run mlops-train`) always registers a new model version, but
**never** sets the `production` alias — that's a deliberate gate, not an
oversight (see [MLOPS_PIPELINE.md](./MLOPS_PIPELINE.md)). Promote manually
once you're satisfied with a version's metrics in `reports/metrics.json`:

```python
import os
from mlflow import MlflowClient

tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
MlflowClient(tracking_uri=tracking_uri).set_registered_model_alias(
    "mlops-sklearn-local", "production", "<version>"  # replace <version> with the actual number
)
```

CI/CD (automated training, quality gates, and deployment) is the
`all-mlops-github-actions` extension, not this template.

## GPU

Not required. This template is CPU-first; no CUDA-only dependency is ever
required for `uv sync` or tests to pass.
