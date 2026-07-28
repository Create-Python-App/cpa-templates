"""Assemble the (unfitted) end-to-end sklearn pipeline: preprocessor + features + estimator."""

from __future__ import annotations

from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.pipeline.base import BaseStep, StepContext


def build_model(
    cfg: ExperimentConfig,
    preprocessor: BaseEstimator | str,
    feature_transformer: BaseEstimator | str,
) -> Pipeline:
    classifier = LogisticRegression(max_iter=cfg.model.max_iter, random_state=cfg.random_seed)
    return Pipeline(
        [
            ("scaler", preprocessor),
            ("features", feature_transformer),
            ("classifier", classifier),
        ]
    )


class BuildModelStep(BaseStep):
    name = "model"

    def validate(self, context: StepContext) -> None:
        for key in ("preprocessor", "feature_transformer"):
            if key not in context:
                raise ValueError(f"missing {key} in context")

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        context["model"] = build_model(
            cfg, context["preprocessor"], context["feature_transformer"]
        )
        return context
