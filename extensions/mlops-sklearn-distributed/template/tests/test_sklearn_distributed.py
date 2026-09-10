"""Tests for config-driven parallel search (fallback behavior is the default)."""

from __future__ import annotations

import pytest

from mlops_sklearn_distributed.parallel import run_grid_search


def _quadratic(a: int = 0, b: int = 0) -> float:
    # Peak at a=1, b=2 — deterministic, no data needed.
    return float(-((a - 1) ** 2) - ((b - 2) ** 2))


def test_sequential_finds_best_params() -> None:
    result = run_grid_search(_quadratic, {"a": [0, 1, 2], "b": [0, 2]})
    assert result["best_params"] == {"a": 1, "b": 2}
    assert result["best_score"] == pytest.approx(0.0)


def test_backends_agree_on_best() -> None:
    grid = {"a": [0, 1, 2], "b": [0, 1, 2]}
    sequential = run_grid_search(_quadratic, grid, backend="sequential")
    threads = run_grid_search(_quadratic, grid, backend="threads", n_jobs=2)
    assert threads["best_params"] == sequential["best_params"]
    assert threads["best_score"] == pytest.approx(sequential["best_score"])


def test_processes_backend_matches_sequential() -> None:
    grid = {"a": [0, 1], "b": [0, 2]}
    expected = run_grid_search(_quadratic, grid, backend="sequential")
    actual = run_grid_search(_quadratic, grid, backend="processes", n_jobs=2)
    assert actual == expected


def test_empty_grid_evaluates_once_with_defaults() -> None:
    result = run_grid_search(lambda: 3.0, {})
    assert result == {"best_params": {}, "best_score": 3.0}


def test_rejects_unknown_backend_and_bad_jobs() -> None:
    with pytest.raises(ValueError, match="unknown backend"):
        run_grid_search(_quadratic, {"a": [1]}, backend="dask")
    with pytest.raises(ValueError, match="n_jobs"):
        run_grid_search(_quadratic, {"a": [1]}, n_jobs=0)
