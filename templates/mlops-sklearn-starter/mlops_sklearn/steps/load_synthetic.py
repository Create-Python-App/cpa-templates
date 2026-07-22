"""Generate a tiny synthetic classification dataset (offline)."""

from __future__ import annotations

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.steps.base import BaseStep, StepContext


class LoadSyntheticStep(BaseStep):
    name = "load_synthetic"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x, y = make_classification(
            n_samples=cfg.data.n_samples,
            n_features=cfg.data.n_features,
            n_informative=max(2, cfg.data.n_features // 2),
            n_redundant=0,
            random_state=cfg.random_seed,
        )
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=cfg.data.test_size,
            random_state=cfg.random_seed,
        )
        context.update(
            {
                "x_train": x_train,
                "x_test": x_test,
                "y_train": y_train,
                "y_test": y_test,
            }
        )
        return context
