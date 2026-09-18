"""Build an unfitted scaler for the training pipeline.

Fitting happens once, as part of the composite sklearn.Pipeline in
models/train.py — never here — so the fitted parameters (mean_/scale_)
travel with the persisted model artifact instead of being lost.
"""

from __future__ import annotations

from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.pipeline.base import BaseStep, StepContext

PREPROCESSING_VERSION = "v1"


def build_preprocessor(cfg: ExperimentConfig) -> BaseEstimator | str:
    if cfg.preprocessing.scale:
        return StandardScaler()
    return "passthrough"


class PreprocessingStep(BaseStep):
    name = "preprocessing"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        context["preprocessor"] = build_preprocessor(cfg)
        return context
