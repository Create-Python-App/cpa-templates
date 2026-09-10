"""Train the MLP with a short deterministic CPU loop and register artifacts.

Exports both the raw ``state_dict`` (for ``serving/``) and a TorchScript
module (for runtimes without Python model code) under the active MLflow run.
"""

from __future__ import annotations

from pathlib import Path

import mlflow
import torch
from torch.utils.data import DataLoader

from mlops_pytorch.config import ExperimentConfig
from mlops_pytorch.data.preprocessing import normalize
from mlops_pytorch.models.build import MLPClassifier, NormalizedMLP
from mlops_pytorch.pipeline.base import BaseStep, StepContext
from mlops_pytorch.tracking.client import (
    configure_tracking,
    flatten_params,
    log_params,
)
from mlops_pytorch.tracking.model_registry import register_model_version


def train_epochs(
    model: MLPClassifier,
    train_loader: DataLoader,
    norm_mean: torch.Tensor,
    norm_std: torch.Tensor,
    epochs: int,
    lr: float,
    seed: int,
) -> None:
    torch.manual_seed(seed)
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    for _ in range(epochs):
        for xb, yb in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(normalize(xb, norm_mean, norm_std)), yb)
            loss.backward()
            optimizer.step()


def export_torchscript(model: torch.nn.Module) -> Path:
    """TorchScript the eval-mode model; returns the written ``model.ts`` path."""
    model.eval()
    with torch.no_grad():
        scripted = torch.jit.script(model)
    path = Path("model.ts")
    torch.jit.save(scripted, str(path))
    return path


class TrainStep(BaseStep):
    name = "training"

    def validate(self, context: StepContext) -> None:
        for key in ("model", "train_loader", "norm_stats"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        configure_tracking(cfg.experiment_name)

        model: MLPClassifier = context["model"]
        stats = context["norm_stats"]
        train_epochs(
            model,
            context["train_loader"],
            stats["mean"],
            stats["std"],
            epochs=cfg.training.epochs,
            lr=cfg.training.lr,
            seed=cfg.random_seed,
        )

        state_path = Path("model.pt")
        torch.save(model.state_dict(), state_path)
        served = NormalizedMLP(model, stats["mean"], stats["std"])
        ts_path = export_torchscript(served)

        with mlflow.start_run(run_name="train") as run:
            # Log the full config (minus `steps`, not a hyperparameter) so a
            # run's lineage is fully reconstructable from its logged params
            # alone, per docs/MLOPS_CONTRACT.md.
            log_params(flatten_params(cfg.model_dump(exclude={"steps"})))
            mlflow.log_artifact(str(state_path), artifact_path="state_dict")
            mlflow.log_artifact(str(ts_path), artifact_path="torchscript")
            version = register_model_version(served, cfg.experiment_name, run.info.run_id)
            context["model_version"] = version
            context["mlflow_run_id"] = run.info.run_id

        return context
