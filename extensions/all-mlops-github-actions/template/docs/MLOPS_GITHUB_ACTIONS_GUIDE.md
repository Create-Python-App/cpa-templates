# MLOps GitHub Actions Guide

## Overview

The **all-mlops-github-actions** extension adds MLOps continuous integration
to MLOps starter templates: lint, unit tests, and an end-to-end pipeline
smoke run (`mlops-train --config configs/default.yaml`) on every push and
pull request. Repository automation (linters, PR reviews, releases) stays in
`all-github-setup`; this extension only adds the MLOps training smoke.

## Compatibility

Currently compatible with `mlops-sklearn`. PyTorch/TensorFlow starters adopt
the same `mlops-train --config <path>` entrypoint contract when they land, at
which point this extension gains those types with no workflow changes.

## What it adds

| Path | Purpose |
|------|---------|
| `.github/workflows/mlops-ci.yml` | Lint + pytest + pipeline smoke on push/PR |
