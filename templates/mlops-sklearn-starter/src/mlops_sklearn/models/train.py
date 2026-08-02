"""Fit the assembled pipeline and register it as a new MLflow model version."""

from __future__ import annotations

import mlflow

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.data.preprocessing import PREPROCESSING_VERSION
from mlops_sklearn.pipeline.base import BaseStep, StepContext
from mlops_sklearn.tracking.client import (
    configure_tracking,
    flatten_params,
    log_dataset,
    log_params,
)
from mlops_sklearn.tracking.model_registry import register_model_version


class TrainStep(BaseStep):
    name = "training"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "x_train", "y_train", "dataset"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        configure_tracking(cfg.experiment_name)

        with mlflow.start_run(run_name="train") as run:
            # Log the full config (minus `steps`, not a hyperparameter) so a
            # run's lineage is fully reconstructable from its logged params
            # alone, per docs/MLOPS_CONTRACT.md.
            log_params(flatten_params(cfg.model_dump(exclude={"steps"})))
            mlflow.set_tag("preprocessing_version", PREPROCESSING_VERSION)
            log_dataset(context["dataset"], context="training")

            pipeline = context["model"]
            pipeline.fit(context["x_train"], context["y_train"])

            version = register_model_version(pipeline, cfg.experiment_name, run.info.run_id)
            context["model_version"] = version
            context["mlflow_run_id"] = run.info.run_id

        return context
