"""Plain metric-computation functions — directly unit-testable, no StepContext needed."""

from __future__ import annotations

import numpy as np


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    accuracy = float((y_true == y_pred).mean()) if y_true.size else 0.0
    f1_scores = []
    for label in np.unique(np.concatenate([y_true, y_pred])):
        tp = int(((y_pred == label) & (y_true == label)).sum())
        fp = int(((y_pred == label) & (y_true != label)).sum())
        fn = int(((y_pred != label) & (y_true == label)).sum())
        denom = 2 * tp + fp + fn
        f1_scores.append(2 * tp / denom if denom else 0.0)
    weights = np.array([(y_true == label).sum() for label in np.unique(np.concatenate([y_true, y_pred]))])
    f1_weighted = float(np.average(f1_scores, weights=weights)) if weights.sum() else 0.0
    return {"accuracy": accuracy, "f1_weighted": f1_weighted}
