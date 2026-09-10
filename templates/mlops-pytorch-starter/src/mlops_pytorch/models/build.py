"""Assemble the (untrained) tabular MLP classifier — CPU-first, tiny by design."""

from __future__ import annotations

import torch
from torch import nn

from mlops_pytorch.config import ExperimentConfig
from mlops_pytorch.pipeline.base import BaseStep, StepContext

_SUPPORTED_MODEL_TYPES = ("mlp_classifier",)


class MLPClassifier(nn.Module):
    def __init__(self, n_features: int, hidden_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class NormalizedMLP(nn.Module):
    """Serving wrapper: applies train-split normalization, then the MLP.

    Bundling normalization with the weights (like sklearn's Pipeline)
    keeps serving correct without a sidecar stats file.
    """

    def __init__(self, model: MLPClassifier, mean: torch.Tensor, std: torch.Tensor) -> None:
        super().__init__()
        self.model = model
        self.register_buffer("mean", mean)
        self.register_buffer("std", std.clamp_min(1e-8))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model((x - self.mean) / self.std)


def build_model(cfg: ExperimentConfig, n_features: int) -> MLPClassifier:
    if cfg.model.type not in _SUPPORTED_MODEL_TYPES:
        raise ValueError(
            f"unsupported model.type {cfg.model.type!r}; supported: {_SUPPORTED_MODEL_TYPES}"
        )
    torch.manual_seed(cfg.random_seed)
    return MLPClassifier(n_features=n_features, hidden_dim=cfg.model.hidden_dim)


class BuildModelStep(BaseStep):
    name = "model"

    def validate(self, context: StepContext) -> None:
        if "n_features" not in context:
            raise ValueError("missing n_features in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        context["model"] = build_model(cfg, context["n_features"])
        return context
