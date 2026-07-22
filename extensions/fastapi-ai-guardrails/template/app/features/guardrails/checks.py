"""Reusable input/output guardrail checks (no external moderation APIs)."""

from __future__ import annotations

import re

_EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_BLOCKED = re.compile(r"(?i)\b(ignore previous instructions|exfiltrate secrets)\b")


class GuardrailError(ValueError):
    """Raised when a guardrail fails."""


def check_input_length(text: str, max_chars: int = 4000) -> None:
    if len(text) > max_chars:
        raise GuardrailError(f"input length {len(text)} exceeds {max_chars}")


def check_blocked_patterns(text: str) -> None:
    if _BLOCKED.search(text):
        raise GuardrailError("blocked pattern detected in input")


def redact_emails(text: str) -> str:
    return _EMAIL.sub("[redacted-email]", text)


def apply_input_guardrails(text: str, max_chars: int = 4000) -> str:
    check_input_length(text, max_chars=max_chars)
    check_blocked_patterns(text)
    return text


def apply_output_guardrails(text: str) -> str:
    return redact_emails(text)
