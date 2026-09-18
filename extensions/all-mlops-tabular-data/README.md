# all-mlops-tabular-data

Framework-agnostic tabular data pack for MLOps starters. Layers synthetic
tabular generation, disjoint index splitting, train-only standardization,
and schema validation onto any `mlops-*` template — no sklearn, PyTorch, or
TensorFlow dependency.

## Generated layout

- `data_packs/tabular.py` — generators, splitters, standardizer, validator.
- `tests/test_tabular_data_pack.py` — shape/determinism/leakage/validation tests.
- `template/pyproject.toml` — partial: `force-include`s `data_packs` into the wheel.
- `docs/TABULAR_DATA_GUIDE.md` — long-form guide, linked from the project docs.

## Usage (generated project)

```python
from data_packs.tabular import make_tabular_classification, split_indices

x, y = make_tabular_classification(n_samples=200, n_features=8, seed=42)
train_idx, test_idx = split_indices(len(x), test_size=0.25, seed=42)
```
