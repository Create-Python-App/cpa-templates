"""Config-driven parallel hyperparameter search for sklearn starters.

Backends: ``sequential`` (default, single process — always available),
``threads`` (shared-memory parallelism), ``processes`` (multi-process via
joblib, which ships with scikit-learn). No Dask/Ray dependency: graduate
to those only when a cluster is real — see DISTRIBUTED_TRAINING_GUIDE.md.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from joblib import Parallel, delayed  # type: ignore[import-untyped]
from sklearn.model_selection import ParameterGrid

_BACKENDS = ("sequential", "threads", "processes")


def run_grid_search(
    fit_score: Callable[..., float],
    param_grid: Mapping[str, list[Any]],
    *,
    backend: str = "sequential",
    n_jobs: int = 1,
) -> dict[str, Any]:
    """Evaluate every grid point, return ``{"best_params": ..., "best_score": ...}``.

    ``fit_score(**params)`` returns a higher-is-better score. Deterministic
    for a fixed grid order: ties resolve to the first grid point, and
    ``sequential``/``threads``/``processes`` agree because results are
    collected in grid order, not completion order.
    """
    if backend not in _BACKENDS:
        raise ValueError(f"unknown backend {backend!r}; supported: {_BACKENDS}")
    if n_jobs < 1:
        raise ValueError(f"n_jobs must be >= 1, got {n_jobs}")
    # Note: `ParameterGrid({})` yields one empty combination, so an empty
    # grid means a single default evaluation — never an error.
    grid = list(ParameterGrid(dict(param_grid)))

    def _evaluate(params: dict[str, Any]) -> float:
        return float(fit_score(**params))

    if backend == "sequential" or (backend == "threads" and n_jobs == 1):
        scores = [_evaluate(params) for params in grid]
    else:
        prefer = "threads" if backend == "threads" else "processes"
        scores = Parallel(n_jobs=n_jobs, prefer=prefer)(
            delayed(_evaluate)(params) for params in grid
        )
    best_index = int(max(range(len(scores)), key=lambda i: scores[i]))
    return {"best_params": grid[best_index], "best_score": scores[best_index]}
