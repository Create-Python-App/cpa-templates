# MLOps template contract

Shared contract for `mlops-sklearn-starter` ([#84](https://github.com/Create-Python-App/cpa-templates/issues/84)),
`mlops-pytorch-starter`, and `mlops-tensorflow-starter` (future), so the three
frameworks don't drift into unrelated designs. Parent epic:
[#71](https://github.com/Create-Python-App/cpa-templates/issues/71). This
contract is defined in
[#83](https://github.com/Create-Python-App/cpa-templates/issues/83) and
complements [AI_ML_AUTHORING.md](./AI_ML_AUTHORING.md)'s taxonomy.

## Project layout

MLOps templates use `src/<package>/` layout — an intentional deviation from
the rest of the catalog (`fastapi-starter`, `cli-starter` use a flat
`<package>/`), decided explicitly for this framework family.

```
templates/mlops-<framework>-starter/
├── src/<package>/
│   ├── config.py                  # typed ExperimentConfig (pydantic v2)
│   ├── pipeline/                   # orchestration glue only — no ML logic
│   │   ├── base.py                  # BaseStep ABC, StepContext
│   │   ├── steps_registry.py         # STEP_REGISTRY: dict[str, type[BaseStep]]
│   │   └── run.py                     # run_pipeline(config_path), CLI entrypoint
│   ├── data/                        # Data Processing stage
│   │   ├── loading.py                 # load/generate raw data AND train/test split
│   │   ├── preprocessing.py            # cleaning; fit-on-train, transform-both
│   │   └── features.py                  # feature engineering
│   ├── models/                       # Training & Evaluation stage
│   │   ├── build.py                    # build_model(cfg) — architecture/estimator
│   │   ├── train.py                     # fit step; registers new MLflow model version
│   │   ├── evaluate.py                   # thin orchestrator: metrics + plots + report
│   │   └── metrics.py                     # compute_metrics(y_true, y_pred) -> dict
│   ├── visualization/                 # plotting functions (used by data/ and models/)
│   │   └── plots.py
│   ├── tracking/                      # MLflow-specific concerns only
│   │   ├── client.py                    # tracking URI/experiment/run/dataset wrappers
│   │   └── model_registry.py             # load/register/promote-check helpers
│   └── serving/                       # Deploying stage
│       ├── predict.py                   # loads model by URI, never retrains
│       └── app.py (optional)              # FastAPI endpoint, framework-dependent
├── configs/default.yaml
├── reports/                          # gitignored output: metrics.json, plots
├── tests/                            # Testing stage
├── docs/                             # 7 required docs, see below
├── pyproject.toml, cpa.config.json, AGENTS.md, README.md, .env.example, .gitignore
```

**Naming and boundary notes:**

- `models/build.py`, not `architecture.py` — "architecture" fits defining
  PyTorch/TensorFlow layers but reads oddly for "pick a `LogisticRegression`
  and its hyperparams." One name must work across all three frameworks.
- `pipeline/steps_registry.py`, not `pipeline/registry.py` — disambiguates
  from `tracking/model_registry.py` (the MLflow Model Registry). Both are
  "registries" of completely different things.
- `visualization/` is top-level, not nested under `models/` — reusable by
  both `data/` (e.g. input distributions) and `models/` (confusion matrix,
  ROC curve).
- `reports/` is a root-level, **gitignored output** directory, not a `src/`
  code package. Under the CPU-first/offline policy, CI runs get a throwaway
  local MLflow store with no persistent server, so `reports/metrics.json`
  (+ optional plots), uploaded as a plain GitHub Actions artifact by the
  future `all-mlops-github-actions` extension
  ([#87](https://github.com/Create-Python-App/cpa-templates/issues/87)), is
  the only durable output a PR reviewer can inspect after a CI run ends.
- **No root-level `models/` artifact folder.** MLflow's own tracking store is
  the single source of truth for trained artifacts — a second, differently
  scoped `models/` (root-level files vs. `src/<package>/models/` code) would
  create confusing naming overlap.
- **No `metrics/` top-level package** — `models/metrics.py` (its own file,
  not its own package) gets the same testability without an unjustified
  package boundary.
- **No generic `utils/`** — a catch-all with no single responsibility. A
  genuine cross-cutting helper gets a name describing what it does instead.
- **No `notebooks/` or `references/`** — no real datasets under the
  synthetic/fixture-only data policy, and notebooks invite untested
  exploratory code into a template meant to demonstrate clean, typed, tested
  practice.

## `BaseStep` interface

CPA templates are scaffolded into independent generated projects with no
runtime dependency on `cpa-templates` itself. "Shared `BaseStep` interface"
means the **same interface pattern, reimplemented identically** in each
framework template — never a shared installed package.

```python
# src/<package>/pipeline/base.py
from abc import ABC, abstractmethod
from typing import Any

StepContext = dict[str, Any]

class BaseStep(ABC):
    name: str

    def validate(self, context: StepContext) -> None:
        return None

    @abstractmethod
    def run(self, context: StepContext) -> StepContext:
        raise NotImplementedError
```

`pipeline/run.py`'s `run_pipeline(config_path)` builds
`context = {"config": config}`, iterates `config.steps`, looks up each step
class in `STEP_REGISTRY`, calls `step.validate(context)` then
`step.run(context)`, and threads the context through.

## Config model

One YAML file (`configs/default.yaml`), not one file per concern. Additional
files (`configs/ci.yaml`, etc.) are supported via `--config`, each a full
alternate `ExperimentConfig` — never a partial merged override.

Every top-level YAML key maps to exactly one code module, backed by one
pydantic `BaseModel` each, composed into `ExperimentConfig`:

```yaml
# configs/default.yaml
experiment_name: mlops-sklearn-local
random_seed: 42
steps: [loading, preprocessing, features, model, training, evaluate]

loading:            # -> data/loading.py (includes the train/test split)
  n_samples: 200
  n_features: 8
  test_size: 0.25

preprocessing:       # -> data/preprocessing.py
  scale: true

features:            # -> data/features.py
  polynomial_degree: 1

model:                # -> models/build.py (architecture/hyperparams)
  type: logistic_regression
  max_iter: 200

training:              # -> models/train.py (fit-loop settings)
  cv_folds: 1

serving:                 # -> serving/predict.py or app.py
  model_uri: "models:/<name>@production"
```

**Step names match their config section 1:1** — `STEP_REGISTRY` key equals
the YAML key it's configured by (`loading`, `preprocessing`, `features`,
`model`, `training`). Two exceptions, both intentional: `evaluate` needs no
configuration beyond what's already in `context` (the trained model and test
split), so it has no section; `serving` is invoked separately via
`serving/predict.py`/`app.py`, never part of the `steps:` list `run_pipeline`
executes, so it has no step.

**Split lives in `loading`, not a separate stage/section.** To avoid data
leakage, splitting must happen before any preprocessing/feature fitting
(scalers/encoders fit on the train split only, then applied to both). For
synthetic data, generation and splitting are inseparable, so
`data/loading.py` owns both; `LoadingConfig` carries `test_size`/`stratify`.

`ExperimentConfig` base fields every framework must include:
`experiment_name: str`, `random_seed: int`, `steps: list[str]`. The six
per-stage nested configs (`loading`, `preprocessing`, `features`, `model`,
`training`, `serving`) are mandatory sections (may be near-empty for a given
framework), keeping the config's shape self-documenting against the code
layout.

## MLflow policy

- **Local/offline by default.** `tracking/client.py` resolves
  `MLFLOW_TRACKING_URI` from env, defaulting to `sqlite:///./mlflow.db` —
  never a hardcoded remote URI. Remote servers only via env override,
  documented as a blank placeholder in `.env.example`.
- **Registration vs. promotion.** `models/train.py` always registers each
  run's model as a new version via `tracking/model_registry.py` (cheap,
  automatic). Promotion uses MLflow's **alias-based** Model Registry
  (`MlflowClient.set_registered_model_alias(name, "production", version)`) —
  the older stage-based transitions (`Staging`/`Production`/`Archived`) are
  deprecated as of MLflow 2.9 and must not be used. **Setting the
  `production` alias is never automatic in the base template** — that's the
  model-quality-gate CI job's responsibility (`all-mlops-github-actions`,
  [#87](https://github.com/Create-Python-App/cpa-templates/issues/87)),
  which compares the candidate against the version currently aliased
  `production`.
- **Dataset lineage.** `data/loading.py` builds an `mlflow.data.Dataset`
  (e.g. `mlflow.data.from_numpy(x, targets=y, source="synthetic:make_classification")`)
  and puts it on the context; `models/train.py` logs it via a
  `tracking/client.py` wrapper, `log_dataset(dataset, context)`, inside the
  active run — using MLflow's built-in dataset-as-run-input tracking
  (`mlflow.log_input`). `data/preprocessing.py` exposes a plain
  `PREPROCESSING_VERSION` constant, bumped by hand when cleaning/feature
  logic changes, logged as an MLflow tag. Combined with the dataset digest
  and the logged `ExperimentConfig` params, a run's lineage (what data, what
  preprocessing, what config) is fully reconstructable without a new
  dependency or real dataset storage.
- **General app logging is out of scope for `tracking/`.** `tracking/` is
  specifically for MLflow experiment tracking, not Python log lines —
  `logging.basicConfig(...)` inline in `pipeline/run.py`'s CLI entrypoint is
  sufficient.

## Serving policy

Framework/template chooses batch scoring (`serving/predict.py`) or a FastAPI
endpoint (`serving/app.py`), documented in `docs/DEPLOYMENT.md`. Either way,
serving loads a model **by URI** via `tracking/model_registry.py` — defaulting
to the version aliased `production` (`models:/<name>@production`),
overridable via `--model-uri` to test an unaliased version — and **never
retrains on serve**.

## Test policy

1. **Config/schema test** — `configs/default.yaml` loads and validates
   against `ExperimentConfig`.
2. **Shape/forward-pass test** — tiny synthetic tensors through
   `models/build.py` + `models/train.py`; collapses into the training smoke
   test for sklearn, matters more for PyTorch/TensorFlow.
3. **Pipeline smoke test** — `run_pipeline()` end-to-end on synthetic/fixture
   data with a `tmp_path`-backed MLflow store, asserting on
   `context["metrics"]`. No network access, no real API keys, no GPU
   requirement.
4. **Unit tests for extracted plain functions** — `models/metrics.py`,
   `visualization/plots.py`, and `tracking/client.py` are directly
   unit-testable without constructing a `StepContext`, since they're plain
   functions rather than `BaseStep` subclasses.

## Dependency policy

CPU-first defaults (plain `torch`/`tensorflow` CPU wheels, no CUDA-only
extras required for `uv sync` or tests to pass). GPU support may be
documented as an optional path in `docs/DEPLOYMENT.md`, never required.

## Required docs (every MLOps template)

| Doc | Content |
|---|---|
| `docs/README.md` | Standard CPA template overview |
| `docs/PROJECT_STRUCTURE.md` | The layout above, folder-by-folder |
| `docs/CONFIGURATION.md` | `configs/default.yaml` fields, `.env.example` vars |
| `docs/TESTING_GUIDE.md` | The 4 test categories above |
| `docs/DEPLOYMENT.md` | Which serving mode this template uses and why; CI/CD is the `all-mlops-github-actions` extension, not this doc |
| `docs/TYPING.md` | pydantic v2 + mypy/pyright, matching CPA's typed-Python default |
| `docs/MLOPS_PIPELINE.md` | **Non-negotiable**: the `BaseStep` contract, `STEP_REGISTRY`, how to add a step, the registration-vs-promotion split, and dataset/preprocessing lineage |

## CI/CD boundary

This contract governs the template's runtime code and tests only. GitHub
Actions workflows never live in the base template — they come from
`all-mlops-github-actions`
([#87](https://github.com/Create-Python-App/cpa-templates/issues/87)).

## Related docs

- [AI_ML_AUTHORING.md](./AI_ML_AUTHORING.md)
- [AUTHORING.md](./AUTHORING.md)
- `mlops-sklearn-starter` ([#84](https://github.com/Create-Python-App/cpa-templates/issues/84))
  is the first template required to implement this contract.
