"""Compute train-split normalization statistics for the training loop.

Statistics are computed once, here, on the train split only — never on the
holdout — and travel in the context so train/eval/serve normalize
identically.
"""

from __future__ import annotations

import torch

from mlops_pytorch.config import ExperimentConfig
from mlops_pytorch.pipeline.base import BaseStep, StepContext


def normalize(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    return (x - mean) / std.clamp_min(1e-8)


class PreprocessingStep(BaseStep):
    name = "preprocessing"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x_train: torch.Tensor = context["x_train"]
        if cfg.preprocessing.scale:
            mean = x_train.mean(dim=0)
            std = x_train.std(dim=0)
        else:
            mean = torch.zeros(x_train.shape[1])
            std = torch.ones(x_train.shape[1])
        context["norm_stats"] = {"mean": mean, "std": std}
        return context
