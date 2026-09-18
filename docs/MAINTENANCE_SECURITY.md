# Maintenance: Security

> How to handle security alerts, audits, and hardening in the `create-python-app` ecosystem.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).
>
> **Last updated:** September 2026 | Covers: `cpa-templates` templates and extensions as of September 2026, including MLOps (sklearn, PyTorch, TensorFlow) and AI/LLM extensions.

---

## 1. Sources of alerts

There are three main channels:

1. **GitHub Dependabot alerts** — vulnerabilities in direct and transitive dependencies. Runs on both `create-python-app` and `cpa-templates`.
2. **OSV-Scanner CI** — runs in `create-python-app` via `.github/workflows/osv-scanner.yml`. Currently **not run on cpa-templates**; Dependabot alerts are the primary scanner for template and extension dependencies (see [Limitations](#limitations) below).
3. **CodeQL alerts** — code scanning alerts in `create-python-app` and `cpa-templates`.

Check all three when doing security work:

```bash
# Dependabot alerts
gh api repos/Create-Python-App/create-python-app/dependabot/alerts --jq '.[] | {number, severity, package: .dependency.package.name, title}' | head -n 20
gh api repos/Create-Python-App/cpa-templates/dependabot/alerts --jq '.[] | {number, severity, package: .dependency.package.name, title}' | head -n 20

# CodeQL
gh code-scanning alerts list --repo Create-Python-App/create-python-app --state open
gh code-scanning alerts list --repo Create-Python-App/cpa-templates --state open
```

---

## 2. Triage

| Severity | Action | Notes |
|---|---|---|
| Critical / High in CLI code path | P0 — fix immediately and release | — |
| High in **fastapi-starter** or **django-api** | P1 — fix within the sprint | Affects majority of users |
| High in **MLOps templates** (sklearn, PyTorch, TensorFlow) | P1 — fix within the sprint | See [Section 5.2](#52-ml-framework-dependency-profiles) for audit guidance |
| High in **AI/LLM extensions** (fastapi-ai-chat, fastapi-langgraph-chat, etc.) | P1 — fix within the sprint | High indirect user impact via LLM provider deps |
| High in other templates/extensions | P2 — fix in next maintenance cycle | Narrower user base |
| Moderate / Low | Batch with other maintenance | — |
| Informational only | Document and close if not actionable | — |

Questions to ask:

- Is the vulnerable dependency in the **CLI execution path** or only in generated projects?
- Can we bump the dependency without breaking the template/extension?
- Is the fix already available upstream on PyPI?
- Can we mitigate with `pyproject.toml` constraints while waiting for upstream?
- **For MLOps templates:** Does the vulnerability exist in the transitive tree of a heavy framework (PyTorch/TensorFlow/scikit-learn)? These may have overlapping transitive graphs and require coordinated pins.
- **For AI/LLM extensions:** Does the issue affect the LLM provider SDK (openai, anthropic, langchain) or a known-problematic transitive like urllib3?

---

## 3. Fixing in `create-python-app`

The CLI monorepo uses uv. Root-level dependency constraints can pin transitive packages across workspace members.

In the workspace root `pyproject.toml`, use `[tool.uv]` constraint overrides or bump direct dependencies, then:

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
```

Document the rationale in the PR when pinning a transitive dependency for a CVE.

---

## 4. Fixing in `cpa-templates`

Templates and extensions declare dependencies in `pyproject.toml`. The fix must be in version ranges, constraint overrides, or explicit pins—not ad hoc edits in generated projects.

### 4.1 Direct dependency bump

If the vulnerable package is a direct dependency of a template or extension, bump it in that layer's `pyproject.toml`.

### 4.2 Transitive dependency override

If the vulnerable package is transitive, add an explicit pin in the owning template or extension:

```toml
[project]
dependencies = [
  "some-safe-pkg>=1.2.3",
  # Pin transitive fix until upstream releases
  "vulnerable-transitive>=2.0.1",
]
```

When uv override syntax is available in your target template, prefer documented `[tool.uv]` override fields over duplicating unrelated deps.

### 4.3 Cannot fix quickly

If no fixed version exists or the bump is breaking, open a tracking issue and document:

- The CVE or advisory ID.
- Why it cannot be fixed yet.
- The planned remediation date.

---

## 5. Dependency profiles by template type

### 5.1 Standard templates (FastAPI, Django, CLI)

These have lightweight, API-focused dependency trees:

- **fastapi-starter**: FastAPI, uvicorn, pydantic, httpx (dev)
- **django-api**: Django, gunicorn, psycopg3 (opt)
- **cli-starter**: Typer, rich (minimal)
- **celery-worker**: Celery, redis (opt), psycopg3 (opt)

Vulnerabilities in these are usually straightforward to fix via direct dependency bumps. Audit via Dependabot or local `pip-audit`.

### 5.2 MLOps templates: sklearn, PyTorch, TensorFlow

These templates introduce **heavy transitive dependency trees** with scientific computing stacks:

**mlops-sklearn-starter:**
```toml
dependencies = [
  "fastapi>=0.115.0",
  "matplotlib>=3.9.0",
  "mlflow>=2.15.0",
  "numpy>=2.0.0",
  "pydantic>=2.9.0",
  "pyyaml>=6.0.0",
  "scikit-learn>=1.5.0",
  "uvicorn[standard]>=0.30.0",
]
```

**mlops-pytorch-starter, mlops-tensorflow-starter:** Similar, plus `torch>=2.4.0` or `tensorflow>=2.17.0`.

**Audit considerations:**

- The NumPy, SciPy, and framework stacks (PyTorch/TensorFlow) evolve rapidly; always pin lower bounds to stable point releases.
- MLflow adds transitive deps (sqlalchemy, alembic, gunicorn); review MLflow's `setup.py` when an MLflow bump is involved.
- PyTorch and TensorFlow have independent security schedules; monitor their GitHub releases and PyPI pages separately.
- **Local audit:**

  ```bash
  cd templates/mlops-sklearn-starter && uv sync --all-groups
  uv run pip-audit

  cd templates/mlops-pytorch-starter && uv sync --all-groups
  uv run pip-audit

  cd templates/mlops-tensorflow-starter && uv sync --all-groups
  uv run pip-audit
  ```

- **Coordinated fixes:** If a transitive (e.g., urllib3, requests) affects all three MLOps templates, coordinate pins across all three `pyproject.toml` files in one PR to keep the lock graphs aligned.

### 5.3 AI/LLM extensions

These extensions add LLM-provider SDKs and retrieval libraries, introducing their own vulnerability surfaces:

| Extension | Key dependencies | Audit focus |
|-----------|-------------------|------------|
| `fastapi-ai-chat` | langchain-core, pydantic | Provider abstraction layer (mock-only in MVP) |
| `fastapi-ai-guardrails` | guardrails-ai, pydantic | Guardrails library and its transitive graph |
| `fastapi-langgraph-chat` | langgraph, langchain, pydantic | Agent framework (newer, less mature) |
| `fastapi-mcp-client` | mcp (Model Context Protocol), aiohttp | Protocol client library and HTTP stack |
| `fastapi-mlflow-tracing` | mlflow, opentelemetry | MLflow integration + observability stack |
| `fastapi-rag-pgvector` | langchain, psycopg3, pgvector | Vector DB client + retrieval chain |

**Audit considerations:**

- **LLM provider SDKs** (openai, anthropic, cohere) ship under their own release cadence; check GitHub Security Advisories for these packages directly.
- **langchain and langgraph** are actively developed; newer releases may have breaking changes. Test extensions against current versions before bumping.
- **Transitive HTTP libraries** (urllib3, requests, aiohttp) appear in LLM SDK trees; prioritize fixes in these layers.
- **Local audit:**

  ```bash
  cd extensions/fastapi-ai-chat && uv sync
  uv run pip-audit

  cd extensions/fastapi-langgraph-chat && uv sync
  uv run pip-audit

  # Repeat for other AI/LLM extensions
  ```

- **Note:** AI/LLM extensions apply on top of a `fastapi-starter` or similar base; vulnerabilities in the base template propagate. Always audit the **full generated project** after adding an AI/LLM extension:

  ```bash
  cd my-app && uv sync --all-groups && uv run pip-audit
  ```

---

## 6. Running audits locally

### 6.1 In create-python-app

```bash
# In create-python-app (requires pip-audit or osv-scanner)
uv run pip-audit
osv-scanner -r .

# In a generated project
cd my-app && uv run pip-audit
osv-scanner -r .

# uv may expose audit subcommands as they stabilize; prefer project docs when available
```

---

## 7. CodeQL fixes

CodeQL alerts often relate to:

- Unsafe shell command construction from environment variables or user input.
- Injection via template strings in CLI code.
- Path traversal when resolving `file://` template URLs.

### General fix pattern

- Validate and sanitize inputs before passing them to `subprocess` or shell templates.
- Prefer structured arguments (`subprocess.run` with a list) over string shell commands.
- Avoid interpolating user-controlled values directly into commands or file paths.

If an alert is a false positive, dismiss it with a comment explaining why.

---

## 8. Validation

After any security change:

1. Run the relevant audit command until the alert is gone or mitigated.
2. Run the normal CI checks (`pytest`, `ruff`, type-check).
3. For `cpa-templates`: scaffold the affected template + extensions and validate.
4. For `create-python-app`: run the full test suite and security workflows when possible.

---

## 9. Checklist

- [ ] Alert has been triaged and prioritized.
- [ ] Fix is minimal and scoped.
- [ ] Audit no longer reports the vulnerability (or it is documented as unfixable).
- [ ] CI passes.
- [ ] Generated projects still install, lint, and test.
- [ ] A release tag is planned if the fix affects a published PyPI package.

---

## 10. Limitations

### OSV-Scanner coverage gap in cpa-templates

Currently, OSV-Scanner runs only in the `create-python-app` repository (via `.github/workflows/osv-scanner.yml`). The `cpa-templates` repository relies on **Dependabot alerts alone** for supply-chain scanning.

**Implications:**

- Vulnerabilities in template and extension dependencies are flagged by Dependabot, not OSV-Scanner.
- Dependabot coverage is comprehensive but may have different latency and sensitivity than OSV-Scanner.
- If OSV-Scanner is added to `cpa-templates` in the future, this section should be updated and any workflow conflicts resolved.

**Workaround:** Maintainers can run OSV-Scanner locally on template and extension directories as part of security audits (see [Section 6](#6-running-audits-locally)).
