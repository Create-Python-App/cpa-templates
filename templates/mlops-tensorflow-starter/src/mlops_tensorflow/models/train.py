"""Train the MLP with a short deterministic CPU fit and register artifacts.

Exports both the native Keras file (for ``serving/``) and a SavedModel
directory (for runtimes without Python model code) under the active MLflow
run.
"""

from __future__ import annotations

from pathlib import Path

import mlflow
import numpy as np
import tensorflow as tf

from mlops_tensorflow.config import ExperimentConfig
from mlops_tensorflow.data.preprocessing import normalize
from mlops_tensorflow.models.build import MLPClassifier, NormalizedMLP
from mlops_tensorflow.pipeline.base import BaseStep, StepContext
from mlops_tensorflow.tracking.client import (
    configure_tracking,
    flatten_params,
    log_params,
)
from mlops_tensorflow.tracking.model_registry import register_model_version


def train_epochs(
    model: MLPClassifier,
    x_train: np.ndarray,
    y_train: np.ndarray,
    norm_mean: np.ndarray,
    norm_std: np.ndarray,
    epochs: int,
    lr: float,
    batch_size: int,
    seed: int,
) -> None:
    tf.keras.utils.set_random_seed(seed)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    )
    # shuffle=False: the loader is pre-shuffled, so the fit stays fully
    # deterministic under the configured seed.
    model.fit(
        normalize(x_train, norm_mean, norm_std),
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        shuffle=False,
        verbose=0,
    )


def export_savedmodel(
    model: NormalizedMLP, export_dir: Path, example_input: np.ndarray
) -> Path:
    """Export the serving wrapper as SavedModel; returns the directory.

    The SavedModel carries the normalization variables plus the MLP graph,
    so runtimes without this package's Python code can still serve it.
    """
    # A forward pass builds the wrapper's variables before export.
    model(np.asarray(example_input[:1], dtype=np.float32))
    model.export(str(export_dir))
    return export_dir


class TrainStep(BaseStep):
    name = "training"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "x_train", "y_train", "norm_stats"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        configure_tracking(cfg.experiment_name)

        model: MLPClassifier = context["model"]
        stats = context["norm_stats"]
        train_epochs(
            model,
            context["x_train"],
            context["y_train"],
            stats["mean"],
            stats["std"],
            epochs=cfg.training.epochs,
            lr=cfg.training.lr,
            batch_size=cfg.training.batch_size,
            seed=cfg.random_seed,
        )

        weights_path = Path("model.keras")
        model.save(str(weights_path))
        served: NormalizedMLP = NormalizedMLP(model, stats["mean"], stats["std"])
        # Raw features: the wrapper normalizes internally, like serving input.
        sm_path = export_savedmodel(
            served, Path("model.savedmodel"), context["x_train"]
        )

        with mlflow.start_run(run_name="train") as run:
            # Log the full config (minus `steps`, not a hyperparameter) so a
            # run's lineage is fully reconstructable from its logged params
            # alone, per docs/MLOPS_CONTRACT.md.
            log_params(flatten_params(cfg.model_dump(exclude={"steps"})))
            mlflow.log_artifact(str(weights_path), artifact_path="weights")
            mlflow.log_artifact(str(sm_path), artifact_path="savedmodel")
            version = register_model_version(
                served,
                cfg.experiment_name,
                run.info.run_id,
                input_example=np.asarray(context["x_train"][:1], dtype=np.float32),
            )
            context["model_version"] = version
            context["mlflow_run_id"] = run.info.run_id

        return context
