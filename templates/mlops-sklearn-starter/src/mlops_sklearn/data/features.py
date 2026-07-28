"""Build an unfitted feature transformer for the training pipeline.

Like preprocessing, fitting happens once as part of the composite
sklearn.Pipeline in models/train.py.
"""

from __future__ import annotations

from sklearn.base import BaseEstimator
from sklearn.preprocessing import PolynomialFeatures

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.pipeline.base import BaseStep, StepContext


def build_features(cfg: ExperimentConfig) -> BaseEstimator | str:
    if cfg.features.polynomial_degree > 1:
        return PolynomialFeatures(degree=cfg.features.polynomial_degree, include_bias=False)
    return "passthrough"


class FeaturesStep(BaseStep):
    name = "features"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        context["feature_transformer"] = build_features(cfg)
        return context
