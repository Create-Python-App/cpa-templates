"""CLI entry: run configured pipeline steps."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from mlops_sklearn.config import load_config
from mlops_sklearn.pipeline.base import StepContext
from mlops_sklearn.pipeline.steps_registry import STEP_REGISTRY


def run_pipeline(config_path: Path) -> StepContext:
    config = load_config(config_path)
    context: StepContext = {"config": config}
    for step_name in config.steps:
        step_cls = STEP_REGISTRY.get(step_name)
        if step_cls is None:
            raise KeyError(f"unknown step: {step_name}")
        step = step_cls()
        step.validate(context)
        context = step.run(context)
    return context


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Run the sklearn MLOps pipeline")
    parser.add_argument("--config", type=Path, default=Path("configs/default.yaml"))
    args = parser.parse_args()
    result = run_pipeline(args.config)
    metrics = result.get("metrics", {})
    print(f"pipeline complete metrics={metrics}")


if __name__ == "__main__":
    main()
