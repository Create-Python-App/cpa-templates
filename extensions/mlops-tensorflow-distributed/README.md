# mlops-tensorflow-distributed

`tf.distribute` strategy helpers for TensorFlow starters (no new
dependencies). CPU-single fallback is the default.

## Generated layout

- `mlops_tensorflow_distributed/strategy.py` — `get_strategy()`,
  `num_replicas()`.
- `template/pyproject.toml` — partial: `force-include`s the helpers into
  the wheel.
- `tests/test_tensorflow_distributed.py` — fallback strategy tests.
- `docs/DISTRIBUTED_TRAINING_GUIDE.md` — local execution, cluster/GPU notes.

## Usage (generated project)

```python
from mlops_tensorflow_distributed.strategy import get_strategy

with get_strategy("single").scope():
    model = build_model(cfg, n_features)
```
