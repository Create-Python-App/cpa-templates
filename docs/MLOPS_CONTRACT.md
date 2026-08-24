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



## CI profile compatibility

Every registered MLOps template and extension must participate in CPA's layered CI model. MLOps CI stays CPU-first, offline-capable, and free of required external credentials.

| Layer              | MLOps requirement                                                                                                                                                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **L1 — template**  | Every MLOps template must have a bare scaffold job, even when no compatible extensions exist yet. The generated project must scaffold successfully with its default CPU-safe configuration.                                                        |
| **L2 — extension** | Every MLOps extension must be tested against its canonical template type. After scaffolding, CI must run the generated project's test command (`pytest` unless the template defines another command), not only dependency installation or linting. |
| **L3 — profile**   | Maintain a small set of curated, representative MLOps stacks under `ci/profiles/`. Profiles validate realistic extension composition; they must not attempt every compatible extension combination.                                                |

Additional CI requirements:

* Generated-project validation must use synthetic or fixture data and must not require network access.
* Environment validation must remain enabled in CI. Required values must come from safe defaults, `.env.example`, or test fixtures rather than skipping schema validation.
* Default CI must not require cloud credentials, API keys, remote experiment trackers, GPUs, CUDA, or distributed-training infrastructure.
* GPU, cloud, and distributed paths must be mocked, reduced to a CPU fallback, or kept outside the default L1/L2/L3 profiles.
* Every new MLOps template or extension must identify the CI layer/profile that validates it.


## Shared environment variables

MLOps templates and extensions should use a small, consistent set of environment variables for configuration shared across generated projects.

### Common variables

| Variable              | Purpose                                                            | Default / CI expectation                                                                          |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `MODEL_NAME`          | Logical name of the model being trained, evaluated, or registered. | Templates should provide a deterministic local default such as the project or starter model name. |
| `MLFLOW_TRACKING_URI` | MLflow experiment-tracking and model-registry backend.             | Must default to a local/offline-safe backend such as `sqlite:///./mlflow.db`.                     |

Rules:

* Shared variables must have deterministic, CPU-safe, offline-capable defaults where possible.
* Templates must not require users to configure cloud services merely to scaffold, import, or test the generated project.
* `.env.example` should document variables exposed to generated-project users.
* Environment-variable names must be stable across MLOps templates when they represent the same concept.
* Extensions should reuse an existing shared variable instead of introducing a template-specific alias for the same setting.
* Extension-specific configuration may introduce additional variables only when the setting is not already covered by the common contract.
* Secrets such as API keys, cloud credentials, tokens, and passwords must never have committed real values or insecure production defaults.
* CI tests must provide safe fixture values for required secrets or mock the integration that consumes them.
* Configuration validation should remain active in CI rather than being bypassed because credentials or remote services are unavailable.

### Tracker configuration

`MLFLOW_TRACKING_URI` is the canonical experiment-tracker URI for templates using the shared MLflow tracking module. Do not introduce a second generic variable such as `EXPERIMENT_TRACKER_URI` for the same setting.

An extension using a different tracking system may define provider-specific variables when required, but those variables belong to that extension and must not change the meaning of the shared MLflow configuration.





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


## Extension composition rules

MLOps extensions must compose without changing the core module boundaries, test guarantees, or CPU-first/offline behavior defined by this contract.

### Compatibility

An MLOps extension is compatible with a template only when:

* the template's `type` is included in the extension's declared `type`;
* the extension does not overwrite files or feature modules owned by another selected extension;
* applying the extension does not make the generated project's default install or tests require a GPU, cloud service, network access, or real credentials;
* shared configuration follows the environment-variable contract above rather than introducing aliases for existing settings.

Extensions should add capability around the common MLOps structure instead of replacing it. For example, an experiment-tracking, serving, data-validation, or CI extension may add implementation around the relevant module boundary, but should not move model training, data loading, or pipeline orchestration into a different project layout.

### Ownership and conflicts

Each extension must have a clear ownership boundary for the files, routes, configuration, and runtime behavior it adds.

Use `incompatibleWith` when two extensions cannot safely coexist, including when they:

* overwrite the same generated file or feature directory;
* claim the same route or provider slot with mutually exclusive implementations;
* configure competing runtimes or backends that cannot operate together;
* make contradictory assumptions about ownership of the same MLOps concern.

`incompatibleWith` declarations must be symmetric. If extension `a` declares extension `b` incompatible, extension `b` must also declare extension `a`.

Do not use `incompatibleWith` for differences that can coexist through namespacing, merged configuration, optional dependencies, or provider-specific environment variables.

Known and future AI/ML conflicts belong in the compatibility matrix defined by `AI_ML_AUTHORING.md` and must be reflected in `templates.json` before the conflicting extensions are considered supported together.

### Composition testing

Compatibility in registry metadata is a promise that representative combinations can generate and test successfully.

* L2 validates an extension against its canonical compatible template.
* L3 validates selected multi-extension MLOps stacks that represent realistic usage.
* A new interaction between extensions that changes runtime behavior should be covered by an appropriate L3 profile.
* L3 profiles remain curated; the catalog does not need CI coverage for the Cartesian product of every nominally compatible extension.

When composition exposes a true structural or runtime conflict, prefer declaring the incompatibility explicitly instead of weakening tests or adding order-dependent behavior merely to make the combination pass.



## Observability policy (span cohabitation: MLflow vs OpenTelemetry)

MLOps templates reach observability through two surfaces that **must not
double-instrument the same request**: MLflow (training-run tracking, owned
by `tracking/` per the policy above) and OpenTelemetry (HTTP/request tracing,
owned by the `fastapi-opentelemetry` extension). This section keeps both
composable when a serving FastAPI endpoint (`serving/app.py`) coexists with
the tracing extension stack.

### Ownership split

| Concern | Owner | Enabled by |
|---|---|---|
| Training run, params, metrics, datasets, model registry | `tracking/` (this contract) | `MLFLOW_TRACKING_URI` (local/offline default) |
| HTTP request spans + framework instrumentation | `fastapi-opentelemetry` extension | `OTEL_ENABLED` |
| LLM inference / tool / retrieval / guardrail spans | FastAPI AI extensions under #73, using #81's primitives | `MLFLOW_ENABLED` + the span-kind API from #112 |

### Coexistence rule (non-negotiable)

1. **MLflow autolog for FastAPI is OFF by default** in `fastapi-mlflow-tracing`
   (#81). The extension instruments only the spans it explicitly starts via
   `_maybe_start_span(kind, name)` — it never globally patches FastAPI, uvicorn,
   or `requests` like `otelsdk` does.
2. **OpenTelemetry wins on HTTP.** When both `fastapi-opentelemetry` and
   `fastapi-mlflow-tracing` are applied to the same `fastapi-backend` project:
   - HTTP request spans (kind `SERVER`, route, status, latency) belong to OTel.
   - MLflow emits only its **child spans** (`llm_inference`, `tool_call`,
     `retrieval`, `guardrail_check` per #112) — explicitly opened by the AI
     extension code, never auto-spanned from the request middleware.
   - This avoids span trees with duplicate `SERVER` entries and avoids
     double-recording request latency.
3. **No silent no-op cascade.** If both `OTEL_ENABLED` and `MLFLOW_ENABLED` are
   unset, both layers become no-op. The generated `app/main.py` wire-up (one
   line per extension, per `AUTHORING.md` parity) must not assume an order:
   `init_sentry()` → `configure_telemetry(app)` → `configure_mlflow_tracing(app)`
   is the documented order, but each helper must tolerate being called alone
   or after a no-op sibling.
4. **Attribute namespace.** OTel uses OpenTelemetry semconv attributes
   (`http.request.method`, `http.response.status_code`, ...). MLflow-traced AI
   spans use the `llm.*` / `tool.*` / `retrieval.*` namespace defined by #112.
   No extension writes attributes outside its namespace.
5. **`incompatibleWith` declaration.** Any future extension that would patch
   FastAPI globally (e.g. an alternate MLflow autolog) must declare
   `incompatibleWith: ["fastapi-opentelemetry"]` in `templates.json`. The
   current `fastapi-mlflow-tracing` design (#81) does **not** patch globally,
   so it stays compatible by default — but #91 owns the matrix that enforces
   this for every new entry.

### Privacy (applies to both layers)

- Default is **no payload logging**. Raw HTTP bodies, raw prompts, raw
  completions, credentials, and sensitive headers are never recorded unless
  an explicit opt-in env var is set (`LLM_TRACE_PAYLOAD=true` for AI spans,
  `OTEL_EXPORTER_OTLP_HEADERS` for OTel — both off in CI by default).
- PII redaction surface stays in `fastapi-ai-guardrails` (#82), not in the
  tracing layers.

### Cross-references

- #81 — primitive API owner (`_maybe_start_span`, `set_attribute`).
- #91 — `incompatibleWith` matrix owner.
- #112 — AI span primitive contract (attribute schema for `llm_inference`,
  `tool_call`, `retrieval`, `guardrail_check`).

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
