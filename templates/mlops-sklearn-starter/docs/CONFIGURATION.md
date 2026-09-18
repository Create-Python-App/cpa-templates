# Configuration

Edit `configs/default.yaml`. Every top-level section configures exactly one
module:

| Section | Configures |
|---|---|
| `loading` | `data/loading.py` — `n_samples`, `n_features`, `test_size` |
| `preprocessing` | `data/preprocessing.py` — `scale` |
| `features` | `data/features.py` — `polynomial_degree` |
| `model` | `models/build.py` — `type`, `max_iter` |
| `training` | `models/train.py` — `cv_folds` |
| `serving` | `serving/predict.py` (batch CLI) — `model_uri` |

`MLFLOW_TRACKING_URI` (`.env`) defaults to `sqlite:///./mlflow.db` — local,
offline tracking. Point it at a remote server only via env override.

> **Note:** `serving/app.py` (FastAPI) does not read `configs/default.yaml`.
> It reads `MODEL_URI` from the environment variable (`.env`), which defaults
> to the same value as `serving.model_uri`.

Additional configs (e.g. `configs/ci.yaml`) are full alternate
`ExperimentConfig` files, passed via `--config`, never merged overrides.
