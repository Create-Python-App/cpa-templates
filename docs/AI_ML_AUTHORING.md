# AI/ML authoring guide

How to add AI/ML templates and extensions to `cpa-templates` without creating a
combinatorial catalog. Parent epic:
[#71](https://github.com/Create-Python-App/cpa-templates/issues/71). This
taxonomy is defined in
[#72](https://github.com/Create-Python-App/cpa-templates/issues/72).

## Decision tree: template vs extension

| Question | Template | Extension |
|----------|----------|-----------|
| New project topology / framework? | Yes (e.g. sklearn MLOps layout) | No |
| Optional capability on FastAPI? | No | Yes (`fastapi-*`) |
| GitHub Actions / CT/CD? | Never in base template | Yes (`all-mlops-github-actions`) |
| Data modality (tabular/sequence/image)? | No | Prefer modality packs |
| Distributed training? | No | Framework-specific extension |

**Do not** add a new chat template type. Chat/RAG/agents are FastAPI extensions on
`fastapi-starter` (`type: fastapi-backend`).

**Do not** clone a monolithic SaaS-AI starter (CNA M3 flagship pattern). Compose
extensions instead.

## Categories

| Slug | Use for |
|------|---------|
| `ai-ml-applications` | FastAPI AI capability extensions |
| `mlops` | MLOps framework starters and MLOps-specific extensions |
| Reuse `ci`, `observability`, `database`, `containers`, `security` | Cross-cutting packs (e.g. AI guardrails belong under `security`, not a new category) |

`ai-ml-applications` and `mlops` are not yet in `templates.json` — like the
type/category wiring below, they land via
[#76](https://github.com/Create-Python-App/cpa-templates/issues/76), once the
first template or extension using them exists.

## Template types

| Type | Canonical template dir |
|------|------------------------|
| `mlops-sklearn` | `mlops-sklearn-starter` |
| `mlops-pytorch` | `mlops-pytorch-starter` (future) |
| `mlops-tensorflow` | `mlops-tensorflow-starter` (future) |

Keep using `fastapi-backend` for AI app extensions — do not invent `chat-*` types.

These type/category names are the accepted taxonomy from this issue. Wiring them
into the registry itself — `scripts/ci/registry.py::CANONICAL_TEMPLATE_BY_TYPE`
and `scripts/ci/validate-registry.py::STACK_PREFIX_BY_TYPE` — happens in
[#76](https://github.com/Create-Python-App/cpa-templates/issues/76), once each
template type actually lands. Do not add these mappings before the template
directory they point to exists.

## Quality and CI rules

1. Default tests are **CPU-only**, fast, and use synthetic/fixture data.
2. No mandatory GPU/CUDA dependencies.
3. No network calls or real API keys in tests — placeholders in `.env.example` only.
4. GitHub Actions for MLOps live in extensions, not base templates.
5. **Bare L1** jobs for every AI/ML template even with zero extensions (#92).
6. **L2 runs pytest** in the generated project (#92).
7. L3 profiles stay small — never stack every AI extension (CNA #309 anti-pattern).

## `incompatibleWith` matrix (#91)

Declare conflicts in `templates.json` before merging conflicting pairs.

| Extension A | Extension B | Reason / resolution |
|-------------|-------------|---------------------|
| `fastapi-ai-chat` | `fastapi-langgraph-chat` | Both may own `/chat` — either set `incompatibleWith` or document non-overlapping routes before shipping LangGraph |
| Competing `all-mlops-*-data` packs that overwrite the same data paths | each other | Prefer one modality pack per profile |

Neither `fastapi-ai-chat` nor `fastapi-langgraph-chat` exists yet — this row
documents the rule to apply once the first one lands (tracked in
[#77](https://github.com/Create-Python-App/cpa-templates/issues/77)).

## Extension constraints

- Use `template/` so bank `README.md` does not overwrite the project README.
- Ship `template/docs/<TOPIC>_GUIDE.md` and `template/docs/README.md.append`.
- Partial `pyproject.toml` overlays for dependencies.
- Ship tests for generated paths the extension adds (or document mount steps + unit tests).
- Do **not** embed `.github/workflows` in FastAPI AI extensions — compose `github-setup` or `all-mlops-github-actions`.

## AI span primitive contract (#112)

Describes the standard span kinds and attribute schema AI extensions must use
when emitting LLM/tool/retrieval/guardrail spans via the primitives from
`fastapi-mlflow-tracing` (#81). The helper API (`maybe_start_span`,
`set_attribute`) is owned by #81; this section defines **what** to emit and
**how**, not the helper signatures.

### Related issues

| Issue | Role |
|-------|------|
| [#81](https://github.com/Create-Python-App/cpa-templates/issues/81) | Primitive API owner (`maybe_start_span`, `set_attribute`) |
| [#77](https://github.com/Create-Python-App/cpa-templates/issues/77) | `fastapi-ai-chat` — first consumer |
| [#78](https://github.com/Create-Python-App/cpa-templates/issues/78) | `fastapi-rag-pgvector` — retrieval consumer |
| [#79](https://github.com/Create-Python-App/cpa-templates/issues/79) | `fastapi-langgraph-chat` — agent/tool consumer |
| [#80](https://github.com/Create-Python-App/cpa-templates/issues/80) | `fastapi-mcp-client` — tool_call consumer |
| [#82](https://github.com/Create-Python-App/cpa-templates/issues/82) | `fastapi-ai-guardrails` — guardrail_check consumer |
| [#91](https://github.com/Create-Python-App/cpa-templates/issues/91) | `incompatibleWith` matrix (combination policy) |
| [#112](https://github.com/Create-Python-App/cpa-templates/issues/112) | This contract |

### Span kinds

Every AI extension MUST use one of these four span kinds — never invent new
ones. The span name should be a human-readable identifier (e.g.
`"chat-completion"` or `"vector-search"`).

| Kind | Meaning | Owner issue |
|------|---------|-------------|
| `llm_inference` | A single model completion (chat, embeddings, completion). | #77, #79 |
| `tool_call` | An MCP/agent tool invocation. | #80, #79 |
| `retrieval` | RAG fetch from a vector or knowledge store. | #78 |
| `guardrail_check` | Input/output guardrail evaluation. | #82 |

### Required attributes

#### `llm_inference`

| Attribute | Type | Semantics |
|-----------|------|-----------|
| `llm.provider` | `str` | `"openai"` \| `"anthropic"` \| `"ollama"` \| ... |
| `llm.model` | `str` | Exact model id, e.g. `"gpt-4o-mini"` |
| `llm.input_tokens` | `int` | Token count in |
| `llm.output_tokens` | `int` | Token count out |
| `llm.latency_ms` | `float` | Wall-clock from request to last chunk |
| `llm.error` | `str \| None` | Exception type if failed, `None` on success |
| `llm.stream` | `bool` | `True` if streaming response |
| `llm.temperature` | `float` | _(optional)_ sampling temperature |
| `llm.tool_name` | `str \| None` | _(optional)_ set when the LLM call resolved to a tool |

#### `tool_call`

| Attribute | Type | Semantics |
|-----------|------|-----------|
| `tool.name` | `str` | Tool / function name |
| `tool.input` | `str \| None` | Serialized input, behind `LLM_TRACE_PAYLOAD` opt-in only |
| `tool.output` | `str \| None` | Serialized output, behind `LLM_TRACE_PAYLOAD` opt-in only |
| `tool.error` | `str \| None` | Exception type if failed, `None` on success |

#### `retrieval`

| Attribute | Type | Semantics |
|-----------|------|-----------|
| `retrieval.query` | `str \| None` | Query text, behind `LLM_TRACE_PAYLOAD` opt-in only |
| `retrieval.top_k` | `int` | Number of results requested |
| `retrieval.results_count` | `int` | Number of results returned |
| `retrieval.index` | `str` | Index / store identifier |
| `retrieval.error` | `str \| None` | Exception type if failed, `None` on success |

#### `guardrail_check`

| Attribute | Type | Semantics |
|-----------|------|-----------|
| `guardrail.name` | `str` | Guardrail identifier |
| `guardrail.blocked` | `bool` | `True` if the check rejected the input/output |
| `guardrail.reason` | `str \| None` | Short reason when `blocked=True` |

### Span shape

1. Each kind opens with `maybe_start_span(kind, name="...")` from the
   `fastapi-mlflow-tracing` extension and closes with `.end()`. Latency is
   recorded automatically by the span context manager (#81).
2. **Guardrail rejections** set `llm.error = "guardrail_blocked"` and
   `guardrail.reason` on the **same** `llm_inference` span — not a separate
   span. The span tree stays linear, and the parent `llm_inference` span
   records the error.

Example (illustrative — the helper API is owned by #81):

```python
from app.core.mlflow_tracing import maybe_start_span

def chat(messages: list[dict]) -> str:
    with maybe_start_span(
        "llm_inference",
        name="chat-completion",
        **{
            "llm.provider": "openai",
            "llm.model": "gpt-4o-mini",
            "llm.stream": True,
        }
    ) as span:
        try:
            response = call_openai(messages)
            span.set_attribute("llm.input_tokens", response.usage.prompt_tokens)
            span.set_attribute("llm.output_tokens", response.usage.completion_tokens)
            span.set_attribute("llm.latency_ms", response.latency_ms)
            span.set_attribute("llm.error", None)
            return response
        except Exception as exc:
            span.set_attribute("llm.error", type(exc).__name__)
            raise
```

### Privacy

- **Default is no payload logging.** Raw prompts, completions, tool inputs,
  and tool outputs are never recorded unless an explicit opt-in env var is set.
- `LLM_TRACE_PAYLOAD=true` enables recording of `llm.input_text`,
  `llm.output_text`, `tool.input`, `tool.output`, and `retrieval.query`.
  This is **off in CI** by default and is documented in
  `docs/MLFLOW_TRACING_GUIDE.md`.
- PII redaction surface stays in `fastapi-ai-guardrails` (#82), not in the
  tracing layers or this contract.

### Acceptance criteria

- [x] The 4 span kinds above are documented with their required attributes.
- [x] The privacy rule (`LLM_TRACE_PAYLOAD=false` default, no raw
      prompt/completion logging) is documented.
- [x] The contract links #81 (primitives owner), #77, #78, #79, #80, #82
      (consumers).
- [ ] First consumer (#77 or #82) implements against this contract, not an
      ad-hoc schema.

## Extension constraints

- Use `template/` so bank `README.md` does not overwrite the project README.
- Ship `template/docs/<TOPIC>_GUIDE.md` and `template/docs/README.md.append`.
- Partial `pyproject.toml` overlays for dependencies.
- Ship tests for generated paths the extension adds (or document mount steps + unit tests).
- Do **not** embed `.github/workflows` in FastAPI AI extensions — compose `github-setup` or `all-mlops-github-actions`.

## Related docs

- [AUTHORING.md](./AUTHORING.md)
- [TEMPLATE_QUALITY_M1.md](./TEMPLATE_QUALITY_M1.md)
- [TESTING.md](./TESTING.md)
- [MLOPS_CONTRACT.md](./MLOPS_CONTRACT.md)
