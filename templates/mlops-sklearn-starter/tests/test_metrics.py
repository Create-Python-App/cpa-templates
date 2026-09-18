"""Unit tests for compute_metrics — a plain function, no StepContext needed."""

from __future__ import annotations

import numpy as np

from mlops_sklearn.models.metrics import compute_metrics


def test_compute_metrics_perfect_predictions() -> None:
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 1])
    metrics = compute_metrics(y_true, y_pred)
    assert metrics["accuracy"] == 1.0
    assert metrics["f1_weighted"] == 1.0


def test_compute_metrics_all_wrong() -> None:
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([1, 0, 1, 0])
    metrics = compute_metrics(y_true, y_pred)
    assert metrics["accuracy"] == 0.0
