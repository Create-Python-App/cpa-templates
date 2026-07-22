"""CLI entry: run configured pipeline steps."""

from __future__ import annotations

import argparse
from pathlib import Path

from mlops_sklearn.config import load_config
from mlops_sklearn.steps import STEP_REGISTRY


def run_pipeline(config_path: Path) -> dict:
    config = load_config(config_path)
    context: dict = {"config": config}
    for step_name in config.steps:
        step_cls = STEP_REGISTRY.get(step_name)
        if step_cls is None:
            raise KeyError(f"unknown step: {step_name}")
        context = step_cls().run(context)
    return context


def main() -> None:
    parser = argparse.ArgumentParser(description="Train sklearn MLOps pipeline")
    parser.add_argument("--config", type=Path, default=Path("configs/default.yaml"))
    args = parser.parse_args()
    result = run_pipeline(args.config)
    metrics = result.get("metrics", {})
    print(f"training complete metrics={metrics}")


if __name__ == "__main__":
    main()
