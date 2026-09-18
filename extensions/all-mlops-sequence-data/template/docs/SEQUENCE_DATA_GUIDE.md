# Sequence Data Pack

Framework-agnostic sequence helpers for MLOps starters
(`data_packs/sequence.py`, NumPy only — no framework dependency).

## What it adds

- `make_series()` — deterministic sine + trend + noise series
  `(n_series, length, n_features)`.
- `sliding_windows()` — window/horizon supervised pairs per series.
- `temporal_split()` — contiguous past/future split, never shuffled
  (leakage rule: every train index precedes every test index).
- `validate_series()` — 3D/finite/non-empty schema rules.

## Usage

```python
from data_packs.sequence import (
    make_series,
    sliding_windows,
    temporal_split,
    validate_series,
)

series = make_series(n_series=8, length=64, n_features=3, seed=42)
xs, ys = sliding_windows(series, window=16, horizon=1)
train_idx, test_idx = temporal_split(xs.shape[1])
x_train, x_test = xs[:, train_idx], xs[:, test_idx]
validate_series(x_train)
```

## Configuration

Pure function arguments only — no environment variables.

## Verification

```bash
uv run pytest tests/test_sequence_data_pack.py -v
```

Covers shapes/dtypes, determinism, window counts and target alignment,
short-series rejection, and the temporal ordering guarantee.

## Troubleshooting

- `ValueError: length ... too short for window=..., horizon=...` — raise
  `length` or shrink `window`/`horizon`.
- Never `split_indices`-shuffle series: use `temporal_split`, or future
  information leaks into training.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (leakage rules).
