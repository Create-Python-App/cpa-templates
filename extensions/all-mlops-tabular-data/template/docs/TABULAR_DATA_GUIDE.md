# Tabular Data Pack

Framework-agnostic tabular helpers for MLOps starters (`data_packs/tabular.py`,
NumPy only — no sklearn/PyTorch/TensorFlow dependency).

## What it adds

- `make_tabular_classification()` — deterministic two-blob synthetic dataset.
- `split_indices()` — disjoint shuffled train/test indices (no leakage by
  construction).
- `fit_standardizer()` / `apply_standardizer()` — fit mean/std on the train
  split only, apply anywhere.
- `validate_tabular()` — 2D/finite/row-match/two-class schema rules.

## Usage

```python
from data_packs.tabular import (
    apply_standardizer,
    fit_standardizer,
    make_tabular_classification,
    split_indices,
    validate_tabular,
)

x, y = make_tabular_classification(n_samples=200, n_features=8, seed=42)
train_idx, test_idx = split_indices(len(x), test_size=0.25, seed=42)
stats = fit_standardizer(x[train_idx])  # train split only
x_test = apply_standardizer(x[test_idx], stats)
validate_tabular(x_test, y[test_idx])
```

## Configuration

Pure function arguments only — no environment variables. Defaults
(`n_samples=200`, `test_size=0.25`, `seed=42`) match the MLOps starter
convention.

## Verification

```bash
uv run pytest tests/test_tabular_data_pack.py -v
```

Covers shapes/dtypes, seed determinism, index disjointness + full coverage,
train-only stats (leakage rule), and every validation rejection.

## Troubleshooting

- `ValueError: test_size must be in (0, 1)` — pass a fraction, not a count.
- `ValueError: labels must contain at least two classes` — check your label
  column before validating.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (split lives in loading).
- Starter data guide: `data/` module docstrings.
