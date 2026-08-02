"""Evaluate the fitted pipeline on the holdout split — thin orchestrator only."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow

from mlops_sklearn.models.metrics import compute_metrics
from mlops_sklearn.pipeline.base import BaseStep, StepContext
from mlops_sklearn.visualization.plots import plot_confusion_matrix


class EvaluateStep(BaseStep):
    name = "evaluate"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "x_test", "y_test"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        pipeline = context["model"]
        y_pred = pipeline.predict(context["x_test"])
        metrics = compute_metrics(context["y_test"], y_pred)

        run_id = context.get("mlflow_run_id")
        if run_id:
            with mlflow.start_run(run_id=run_id):
                mlflow.log_metrics(metrics)
                figure = plot_confusion_matrix(context["y_test"], y_pred)
                mlflow.log_figure(figure, "confusion_matrix.png")
                plt.close(figure)

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        (reports_dir / "metrics.json").write_text(
            json.dumps(metrics, indent=2), encoding="utf-8"
        )

        context["metrics"] = metrics
        return context
