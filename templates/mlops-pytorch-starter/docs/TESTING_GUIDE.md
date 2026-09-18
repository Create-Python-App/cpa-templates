# Testing

```sh
uv run pytest
```

- `test_config.py` — config loads and validates.
- `test_pipeline.py` — data-stage step shapes, and the full pipeline smoke
  test (`run_pipeline()` end-to-end, `tmp_path`-backed MLflow store).
- `test_metrics.py` — `compute_metrics()` unit tests.
- `test_predict.py` / `test_app.py` — serving tests. Both simulate promoting
  a trained version to the `production` alias before serving from it —
  promotion is never automatic (see [MLOPS_PIPELINE.md](./MLOPS_PIPELINE.md)).

All tests use synthetic data and a temporary file-backed MLflow store — no
network access, no real credentials.
