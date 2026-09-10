"""MLflow Model Registry helpers — alias-based, never the deprecated stage API."""

from __future__ import annotations

from typing import cast

import mlflow.pytorch
import torch

from mlops_pytorch.models.build import MLPClassifier, NormalizedMLP


def register_model_version(
    model: torch.nn.Module, name: str, run_id: str, input_example: object = None
) -> str:
    """Log the trained model under the active run and register a new version.

    Returns the new model version number as a string. Never sets the
    "production" alias — promotion is a deliberate, separate gate, never
    automatic here.

    `run_id` is kept in the signature to document which run's fit this
    version corresponds to, and for drop-in compatibility with callers
    (`models/train.py` passes `run.info.run_id`). `input_example` is
    required by mlflow>=3 pt2 serialization (traced-graph format).

    The registry model uses pickle serialization (not pt2): pt2 loads as a
    GraphModule that refuses `.eval()`, while serving needs a real
    nn.Module. The traced `model.ts` artifact covers runtimes without
    Python model code.
    """
    _ = run_id
    info = mlflow.pytorch.log_model(
        model,
        artifact_path="model",
        registered_model_name=name,
        input_example=input_example,
        serialization_format="pickle",
    )
    version = info.registered_model_version
    if version is None:
        raise RuntimeError(f"model registration for {name!r} did not return a version")
    return str(version)


def load_model(model_uri: str) -> NormalizedMLP:
    return cast(NormalizedMLP, mlflow.pytorch.load_model(model_uri))


def load_state_dict(path: str, *, n_features: int, hidden_dim: int) -> MLPClassifier:
    """Rebuild the raw MLP architecture and load weights from a ``state_dict`` file."""
    model = MLPClassifier(n_features=n_features, hidden_dim=hidden_dim)
    state = torch.load(path, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model
