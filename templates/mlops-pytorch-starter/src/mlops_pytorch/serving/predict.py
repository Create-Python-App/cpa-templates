"""Batch score a CSV of feature columns using a registered model — never retrains."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch

from mlops_pytorch.config import load_config
from mlops_pytorch.tracking.model_registry import load_model


def load_features(path: Path) -> torch.Tensor:
    return torch.as_tensor(np.loadtxt(path, delimiter=","), dtype=torch.float32)


@torch.no_grad()
def predict(model_uri: str, features: np.ndarray | torch.Tensor) -> np.ndarray:
    model = load_model(model_uri)
    model.eval()
    tensor = (
        features
        if isinstance(features, torch.Tensor)
        else torch.as_tensor(np.asarray(features), dtype=torch.float32)
    )
    if tensor.ndim == 1:
        tensor = tensor.reshape(1, -1)
    return np.asarray(model(tensor).argmax(dim=1).cpu())


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
