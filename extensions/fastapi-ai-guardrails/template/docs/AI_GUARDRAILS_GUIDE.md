# AI Guardrails guide

Import helpers from `app.features.guardrails.checks`:

- `apply_input_guardrails(text)` — length + blocked patterns
- `apply_output_guardrails(text)` — email redaction

Wire these into chat/RAG services before calling providers. No external moderation APIs.
