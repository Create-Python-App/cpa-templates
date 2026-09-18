# Distributed Training (TensorFlow)

Config-driven `tf.distribute` strategies for TensorFlow starters
(`mlops_tensorflow_distributed/`, no new dependencies).

## What it adds

- `get_strategy(kind)` — `single` (default, `OneDeviceStrategy` on CPU:0)
  or `mirrored` (`MirroredStrategy`; one replica on single-CPU CI).
- `num_replicas(kind)` — replica count for logging/gating.

## Usage

```python
from mlops_tensorflow_distributed.strategy import get_strategy

strategy = get_strategy("single")  # or "mirrored" via config
with strategy.scope():
    model = build_model(cfg, n_features)
```

## Local execution

`single` pins to CPU and always works. `mirrored` on one CPU resolves to
one replica — the distribution code path executes for real while CI stays
deterministic.

## Cluster / GPU runner notes

- On multi-GPU hosts the same `mirrored` call spans all GPUs; scale the
  learning rate with the global batch size.
- Multi-worker (`MultiWorkerMirroredStrategy`) needs `TF_CONFIG` on every
  node — out of scope for the default pipeline; add it when the cluster
  is real.
- Missing GPUs: TF falls back to CPU with a oneDNN/CUDA warning, not an
  error — slowness is the symptom.

## Troubleshooting

- `ValueError: unknown strategy` — use `single` or `mirrored`.
- Strategy/replica mismatch at `model.fit` — build AND compile the model
  inside `strategy.scope()`.
- Metric aggregation across replicas is automatic (mean reduction); log
  MLflow metrics once outside the scope.

## Resources

- MLOps contract: `docs/MLOPS_PIPELINE.md` (GPU/distributed outside default CI).
- `tf.distribute` strategy guide.
