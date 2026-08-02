"""Plain metric-computation functions — directly unit-testable, no StepContext needed."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
    }
