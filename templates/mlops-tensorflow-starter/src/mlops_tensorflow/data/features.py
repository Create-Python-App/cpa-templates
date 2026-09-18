"""Feature step — passthrough for the tabular MLP baseline.

Polynomial expansion is intentionally unsupported here: keep this starter
tabular-MLP-only and add modality/feature extensions separately.
"""

from __future__ import annotations

from mlops_tensorflow.config import ExperimentConfig
from mlops_tensorflow.pipeline.base import BaseStep, StepContext


class FeaturesStep(BaseStep):
    name = "features"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        if cfg.features.polynomial_degree > 1:
            raise ValueError(
                "mlops-tensorflow-starter supports only polynomial_degree: 1 "
                "(passthrough); add a feature extension for expansions"
            )
        context["feature_transformer"] = "passthrough"
        return context
