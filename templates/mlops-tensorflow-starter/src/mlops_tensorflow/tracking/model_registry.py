"""MLflow Model Registry helpers — alias-based, never the deprecated stage API."""

from __future__ import annotations

from typing import cast

import mlflow.tensorflow
import numpy as np

from mlops_tensorflow.models.build import MLPClassifier, NormalizedMLP


def register_model_version(
    model: NormalizedMLP, name: str, run_id: str, input_example: np.ndarray
) -> str:
    """Log the trained model under the active run and register a new version.

    Returns the new model version number as a string. Never sets the
    `production` alias — promotion is a deliberate, separate gate, never
    automatic here.

    `run_id` is kept in the signature to document which run's fit this
    version corresponds to, and for drop-in compatibility with callers
    (`models/train.py` passes `run.info.run_id`). `input_example` must be a
    float32 NumPy batch: it is stored as the model's serving signature
    example.
    """
    _ = run_id
    info = mlflow.tensorflow.log_model(
        model,
        artifact_path="model",
        registered_model_name=name,
        input_example=input_example,
    )
    version = info.registered_model_version
    if version is None:
        raise RuntimeError(f"model registration for {name!r} did not return a version")
    return str(version)


def load_model(model_uri: str) -> NormalizedMLP:
    return cast(NormalizedMLP, mlflow.tensorflow.load_model(model_uri))


def load_weights(path: str, *, n_features: int, hidden_dim: int) -> MLPClassifier:
    """Rebuild the raw MLP architecture and load weights from a ``.keras`` file."""
    model: MLPClassifier = MLPClassifier(n_features=n_features, hidden_dim=hidden_dim)
    model.build((None, n_features))
    model.load_weights(path)
    return model
