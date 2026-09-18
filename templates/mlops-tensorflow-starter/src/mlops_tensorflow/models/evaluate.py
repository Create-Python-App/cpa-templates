"""Evaluate the trained MLP on the holdout split — thin orchestrator only."""

from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import numpy as np

from mlops_tensorflow.data.preprocessing import normalize
from mlops_tensorflow.models.build import MLPClassifier
from mlops_tensorflow.models.metrics import compute_metrics
from mlops_tensorflow.pipeline.base import BaseStep, StepContext
from mlops_tensorflow.visualization.plots import plot_confusion_matrix


def predict_all(
    model: MLPClassifier,
    x: np.ndarray,
    mean: np.ndarray,
    std: np.ndarray,
) -> np.ndarray:
    logits = model(normalize(x, mean, std), training=False)
    return np.asarray(np.argmax(np.asarray(logits), axis=1))


class EvaluateStep(BaseStep):
    name = "evaluate"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "x_test", "y_test", "norm_stats"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        model: MLPClassifier = context["model"]
        stats = context["norm_stats"]
        y_pred = predict_all(model, context["x_test"], stats["mean"], stats["std"])
        y_test = np.asarray(context["y_test"])
        metrics = compute_metrics(y_test, y_pred)

        run_id = context.get("mlflow_run_id")
        if run_id:
            with mlflow.start_run(run_id=run_id):
                mlflow.log_metrics(metrics)
                figure = plot_confusion_matrix(y_test, y_pred)
                mlflow.log_figure(figure, "confusion_matrix.png")
                plt.close(figure)

        reports_dir = Path(os.environ.get("MLOPS_REPORTS_DIR", "reports"))
        reports_dir.mkdir(exist_ok=True)
        (reports_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        context["metrics"] = metrics
        return context
