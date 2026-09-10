# all-mlops-sequence-data

Framework-agnostic sequence data pack for MLOps starters. Layers synthetic
series generation, sliding-window supervision pairs, temporal (never
shuffled) splitting, and schema validation onto any `mlops-*` template —
NumPy only.

## Generated layout

- `data_packs/sequence.py` — series, windowing, temporal split, validator.
- `tests/test_sequence_data_pack.py` — shape/determinism/ordering tests.
- `template/pyproject.toml` — partial: `force-include`s `data_packs` into the wheel.
- `docs/SEQUENCE_DATA_GUIDE.md` — long-form guide, linked from the project docs.

## Usage (generated project)

```python
from data_packs.sequence import make_series, sliding_windows, temporal_split

series = make_series(n_series=8, length=64, n_features=3, seed=42)
xs, ys = sliding_windows(series, window=16, horizon=1)
```
