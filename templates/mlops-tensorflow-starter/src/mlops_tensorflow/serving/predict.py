"""Batch score a CSV of feature columns using a registered model — never retrains."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from mlops_tensorflow.config import load_config
from mlops_tensorflow.tracking.model_registry import load_model


def load_features(path: Path) -> np.ndarray:
    return np.asarray(np.loadtxt(path, delimiter=","), dtype=np.float32)


def predict(model_uri: str, features: np.ndarray) -> np.ndarray:
    model = load_model(model_uri)
    matrix = np.asarray(features, dtype=np.float32)
    if matrix.ndim == 1:
        matrix = matrix.reshape(1, -1)
    return np.asarray(np.argmax(np.asarray(model.predict(matrix, verbose=0)), axis=1))


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch predict using a registered model")
    parser.add_argument("--config", type=Path, default=Path("configs/default.yaml"))
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--model-uri", type=str, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    model_uri = args.model_uri or config.serving.model_uri
    features = load_features(args.input)
    predictions = predict(model_uri, features)
    print(",".join(str(int(p)) for p in predictions))


if __name__ == "__main__":
    main()
