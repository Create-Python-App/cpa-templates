# Distributed Training (sklearn)

Config-driven parallel hyperparameter search for sklearn starters
(`mlops_sklearn_distributed/`, joblib only — ships with scikit-learn).

## What it adds

- `run_grid_search()` — grid evaluation with `sequential` (default),
  `threads`, and `processes` backends; results collected in grid order so
  every backend agrees.
- `n_jobs` parallelism without new dependencies.

## Usage

```python
from mlops_sklearn_distributed.parallel import run_grid_search

result = run_grid_search(
    fit_score,
    {"max_depth": [3, 5], "n_estimators": [50, 100]},
    backend="processes",  # or "sequential" (default) / "threads"
    n_jobs=4,
)
print(result["best_params"], result["best_score"])
```

## Local execution

Default `backend="sequential"` runs everything in-process — CI-safe and
deterministic. Raise `n_jobs` with `threads` for shared-memory parallelism
or `processes` for multi-core search on one machine.

## Cluster / GPU runner notes

This extension covers single-machine parallelism. For clusters, graduate
to Dask (`dask-ml` grid search) or Ray Tune: keep `fit_score(**params)`
as the unit of work — it maps directly onto `dask.delayed` or
`tune.with_parameters`. GPUs are irrelevant for this sklearn path.

## Troubleshooting

- `ValueError: unknown backend` — use `sequential`, `threads`, or `processes`.
- Hangs with `processes` — prefer `threads` for tiny/fast `fit_score`
  functions where spawn overhead dominates; keep `n_jobs` at physical cores.
- Divergent backends — results are gathered in grid order, so a mismatch
  means `fit_score` itself is nondeterministic (unseeded RNG); seed it.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (CPU-first/offline CI policy).
- joblib docs: threading vs. multiprocessing backends.
