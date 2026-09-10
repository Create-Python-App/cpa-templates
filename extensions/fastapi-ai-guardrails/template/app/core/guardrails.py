"""
FastAPI AI guardrails extension.
Provides typed guardrail hooks for input and output validation.
"""

import re
from typing import Any


class GuardrailError(Exception):
    """Raised when input or output violates guardrail rules."""


#: Case-insensitive prompt-injection markers blocked from inputs by default.
DEFAULT_INPUT_BLOCKED_PATTERNS: list[str] = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "disregard all previous instructions",
]

#: Email addresses are blocked from outputs by default (PII guard).
DEFAULT_OUTPUT_BLOCKED_PATTERNS: list[str] = [
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
]


def apply_input_guardrails(
    input_data: Any,
    *,
    max_length: int = 1000,
    blocked_patterns: list[str] | None = None,
    required_fields: list[str] | None = None,
) -> Any:
    """
    Validate input data against guardrail rules.

    Args:
        input_data: The input data to validate.
        max_length: Maximum allowed length for string fields.
        blocked_patterns: List of regex-like patterns that should not appear.
        required_fields: List of field names that must be present.

    Returns:
        The validated input data (possibly modified).

    Raises:
        GuardrailError: If input violates any guardrail rule.
    """
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in input_data:
                raise GuardrailError(f"Missing required field: {field}")

    # Check max length for strings
    if isinstance(input_data, str):
        if len(input_data) > max_length:
            raise GuardrailError(
                f"Input string exceeds maximum length of {max_length}: {len(input_data)}"
            )

    # Check blocked patterns (regex, case-insensitive; secure defaults apply)
    for pattern in (
        blocked_patterns if blocked_patterns is not None else DEFAULT_INPUT_BLOCKED_PATTERNS
    ):
        if re.search(pattern, str(input_data), re.IGNORECASE):
            raise GuardrailError(f"Input contains blocked pattern: {pattern}")

    return input_data


def apply_output_guardrails(
    output_data: Any,
    *,
    max_length: int = 1000,
    blocked_patterns: list[str] | None = None,
    required_fields: list[str] | None = None,
) -> Any:
    """
    Validate output data against guardrail rules.

    Args:
        output_data: The output data to validate.
        max_length: Maximum allowed length for string fields.
        blocked_patterns: List of regex-like patterns that should not appear.
        required_fields: List of field names that must be present.

    Returns:
        The validated output data (possibly modified).

    Raises:
        GuardrailError: If output violates any guardrail rule.
    """
    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in output_data:
                raise GuardrailError(f"Missing required field: {field}")

    # Check max length for strings
    if isinstance(output_data, str):
        if len(output_data) > max_length:
            raise GuardrailError(
                f"Output string exceeds maximum length of {max_length}: {len(output_data)}"
            )

    # Check blocked patterns (regex, case-insensitive; secure defaults apply)
    for pattern in (
        blocked_patterns
        if blocked_patterns is not None
        else DEFAULT_OUTPUT_BLOCKED_PATTERNS
    ):
        if re.search(pattern, str(output_data), re.IGNORECASE):
            raise GuardrailError(f"Output contains blocked pattern: {pattern}")

    return output_data
