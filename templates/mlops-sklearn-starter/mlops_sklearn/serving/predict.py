"""Batch score a CSV of feature columns (no header labels required beyond f0..)."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

from mlops_sklearn.config import load_config
from mlops_sklearn.steps.load_synthetic import LoadSyntheticStep
from mlops_sklearn.steps.train_classifier import TrainClassifierStep


def load_features(path: Path) -> np.ndarray:
    return np.loadtxt(path, delimiter=",")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch predict with a freshly trained model")
    parser.add_argument("--config", type=Path, default=Path("configs/default.yaml"))
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    context: dict = {"config": config}
    context = LoadSyntheticStep().run(context)
    context = TrainClassifierStep().run(context)
    model: LogisticRegression = context["model"]
    features = load_features(args.input)
    if features.ndim == 1:
        features = features.reshape(1, -1)
    preds = model.predict(features)
    print(",".join(str(int(p)) for p in preds))


if __name__ == "__main__":
    main()
