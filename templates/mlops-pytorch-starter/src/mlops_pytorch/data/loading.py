"""Generate a tiny synthetic classification dataset (offline) and split it.

Split happens here, not as a separate step, to avoid data leakage: any
later preprocessing/statistic fitting must only ever see the train split.

Pure PyTorch — no scikit-learn dependency in this template.
"""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset

from mlops_pytorch.config import ExperimentConfig
from mlops_pytorch.pipeline.base import BaseStep, StepContext


def _make_blobs(n_samples: int, n_features: int, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
    generator = torch.Generator().manual_seed(seed)
    half = n_samples // 2
    means = torch.tensor([2.0] * n_features + [-2.0] * n_features).view(2, n_features)
    first = torch.randn(half, n_features, generator=generator) + means[0]
    second = torch.randn(n_samples - half, n_features, generator=generator) + means[1]
    x = torch.cat([first, second])
    y = torch.cat(
        [torch.zeros(half, dtype=torch.long), torch.ones(n_samples - half, dtype=torch.long)]
    )
    perm = torch.randperm(n_samples, generator=generator)
    return x[perm], y[perm]


class LoadingStep(BaseStep):
    name = "loading"

    def run(self, context: StepContext) -> StepContext:
        cfg: ExperimentConfig = context["config"]
        x, y = _make_blobs(cfg.loading.n_samples, cfg.loading.n_features, cfg.random_seed)
        n_train = round(cfg.loading.n_samples * (1 - cfg.loading.test_size))
        x_train, x_test = x[:n_train], x[n_train:]
        y_train, y_test = y[:n_train], y[n_train:]

        train_loader = DataLoader(
            TensorDataset(x_train, y_train),
            batch_size=cfg.training.batch_size,
            shuffle=True,
            generator=torch.Generator().manual_seed(cfg.random_seed),
        )
        test_loader = DataLoader(TensorDataset(x_test, y_test), batch_size=1024)
        context.update(
            {
                "x_train": x_train,
                "x_test": x_test,
                "y_train": y_train,
                "y_test": y_test,
                "train_loader": train_loader,
                "test_loader": test_loader,
                "n_features": cfg.loading.n_features,
            }
        )
        return context
