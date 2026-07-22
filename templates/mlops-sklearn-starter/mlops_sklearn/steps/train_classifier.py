"""Train a sklearn classifier and log to local MLflow."""

from __future__ import annotations

import os

import mlflow
import mlflow.sklearn as mlflow_sklearn
from sklearn.linear_model import LogisticRegression

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.steps.base import BaseStep, StepContext


class TrainClassifierStep(BaseStep):
    name = "train_classifier"

    def validate(self, context: StepContext) -> None:
        for key in ("x_train", "y_train"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        self.validate(context)
        cfg: ExperimentConfig = context["config"]
        tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///./mlflow.db")
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(cfg.experiment_name)

        model = LogisticRegression(max_iter=cfg.model.max_iter, random_state=cfg.random_seed)
        with mlflow.start_run(run_name="train_classifier") as run:
            model.fit(context["x_train"], context["y_train"])
            mlflow.log_param("model_type", cfg.model.type)
            mlflow.log_param("max_iter", cfg.model.max_iter)
            mlflow_sklearn.log_model(model, artifact_path="model")
            context["model"] = model
            context["mlflow_run_id"] = run.info.run_id
        return context
