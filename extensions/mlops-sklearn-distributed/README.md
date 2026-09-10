# mlops-sklearn-distributed

Parallel hyperparameter search for sklearn starters (joblib only — ships
with scikit-learn, no Dask/Ray dependency).

## Generated layout

- `mlops_sklearn_distributed/parallel.py` — `run_grid_search()` with
  `sequential`/`threads`/`processes` backends.
- `template/pyproject.toml` — partial: `force-include`s the helpers into
  the wheel.
- `tests/test_sklearn_distributed.py` — backend agreement + fallback tests.
- `docs/DISTRIBUTED_TRAINING_GUIDE.md` — local execution, cluster notes,
  Dask/Ray graduation.

## Usage (generated project)

```python
from mlops_sklearn_distributed.parallel import run_grid_search

result = run_grid_search(fit_score, {"a": [0, 1]}, backend="sequential")
```
