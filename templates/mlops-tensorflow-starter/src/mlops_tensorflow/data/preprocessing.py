"""Compute train-split normalization statistics for the training loop.

Statistics are computed once, here, on the train split only — never on the
holdout — and travel in the context so train/eval/serve normalize
identically.
"""

from __future__ import annotations

import numpy as np

from mlops_tensorflow.config import ExperimentConfig
from mlops_tensorflow.pipeline.base import BaseStep, StepContext


def normalize(x: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    result: np.ndarray = (np.asarray(x, dtype=np.float32) - mean) / np.maximum(std, 1e-8)
    return result


class PreprocessingStep(BaseStep):
    name = "preprocessing"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x_train: np.ndarray = context["x_train"]
        if cfg.preprocessing.scale:
            mean = x_train.mean(axis=0).astype(np.float32)
            std = x_train.std(axis=0).astype(np.float32)
        else:
            mean = np.zeros(x_train.shape[1], dtype=np.float32)
            std = np.ones(x_train.shape[1], dtype=np.float32)
        context["norm_stats"] = {"mean": mean, "std": std}
        return context
