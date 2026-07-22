"""Evaluate trained model on holdout split."""

from __future__ import annotations

import mlflow
from sklearn.metrics import accuracy_score, f1_score

from mlops_sklearn.steps.base import BaseStep, StepContext


class EvaluateStep(BaseStep):
    name = "evaluate"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "x_test", "y_test"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        self.validate(context)
        preds = context["model"].predict(context["x_test"])
        metrics = {
            "accuracy": float(accuracy_score(context["y_test"], preds)),
            "f1_weighted": float(f1_score(context["y_test"], preds, average="weighted")),
        }
        run_id = context.get("mlflow_run_id")
        if run_id:
            with mlflow.start_run(run_id=run_id):
                mlflow.log_metrics(metrics)
        context["metrics"] = metrics
        return context
