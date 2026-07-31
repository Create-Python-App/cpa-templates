"""Generate a tiny synthetic classification dataset (offline) and split it.

Split happens here, not as a separate step, to avoid data leakage: any
later preprocessing/feature fitting must only ever see the train split.
"""

from __future__ import annotations

import numpy as np
from mlflow.data.numpy_dataset import from_numpy
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from mlops_sklearn.config import ExperimentConfig
from mlops_sklearn.pipeline.base import BaseStep, StepContext


class LoadingStep(BaseStep):
    name = "loading"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x, y = make_classification(
            n_samples=cfg.loading.n_samples,
            n_features=cfg.loading.n_features,
            n_informative=max(2, cfg.loading.n_features // 2),
            n_redundant=0,
            random_state=cfg.random_seed,
        )
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=cfg.loading.test_size,
            random_state=cfg.random_seed,
        )
        # source= is omitted: this data is code-generated, not from a real
        # file/URL/table, so mlflow falls back to a CodeDatasetSource that
        # points at the calling code. Passing an arbitrary tag string here
        # (e.g. "synthetic:make_classification") raises MlflowException under
        # mlflow>=2.15, since registered resolvers expect a real URI/path.
        dataset = from_numpy(
            np.asarray(x_train),
            targets=np.asarray(y_train),
            name=cfg.experiment_name,
        )
        context.update(
            {
                "x_train": x_train,
                "x_test": x_test,
                "y_train": y_train,
                "y_test": y_test,
                "dataset": dataset,
            }
        )
        return context
