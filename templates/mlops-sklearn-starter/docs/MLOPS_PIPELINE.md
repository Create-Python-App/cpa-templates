# MLOps pipeline

## `BaseStep` contract

```python
class BaseStep(ABC):
    name: str
    def validate(self, context: StepContext) -> None: ...
    @abstractmethod
    def run(self, context: StepContext) -> StepContext: ...
```

`StepContext` is a plain `dict[str, Any]` threaded through every step.
`run_pipeline(config_path)` (`pipeline/run.py`) builds
`context = {"config": config}`, iterates `config.steps`, looks up each name
in `STEP_REGISTRY`, calls `step.validate(context)` then `step.run(context)`.

## `STEP_REGISTRY`

`pipeline/steps_registry.py` maps config step names to `BaseStep` classes.
Step names match their config section 1:1, except `evaluate` (no
configuration needed beyond context) and `serving` (invoked separately, not
part of `steps:`).

## Adding a new step

1. Implement a `BaseStep` subclass in the appropriate stage module
   (`data/`, `models/`, etc.).
2. Register it in `pipeline/steps_registry.py`'s `STEP_REGISTRY`.
3. Add its name to `configs/default.yaml`'s `steps:` list, and add a
   matching config section if it needs configuration.

## Registration vs. promotion

`models/train.py` always registers each run's model as a new version — cheap
and automatic. **Promoting a version to the `production` alias is never
automatic.** That's a deliberate gate for the future model-quality-gate CI
job (`all-mlops-github-actions`), which compares a candidate against the
version currently aliased `production` before promoting it. See
[DEPLOYMENT.md](./DEPLOYMENT.md) for how to promote manually today.

## Dataset and preprocessing lineage

Every training run logs: the full `ExperimentConfig` as params, an
`mlflow.data.Dataset` built from the exact training split (`data/loading.py`),
and a `preprocessing_version` tag (`data/preprocessing.py`'s
`PREPROCESSING_VERSION`, bumped by hand when cleaning/feature logic changes).
Together these fully reconstruct what data, what preprocessing, and what
config produced a given model version — without a new dependency or real
dataset storage.

## Why the scaler travels with the model

`data/preprocessing.py`/`data/features.py` build **unfitted** transformers.
`models/build.py` assembles them with the classifier into one
`sklearn.Pipeline`, and `models/train.py` fits the whole pipeline in a
single `.fit()` call before logging/registering it as one MLflow model
artifact. This means the fitted scaler's parameters travel with the
registered model — serving code never needs to separately track or reload
them, and can't accidentally apply mismatched preprocessing to new input.
