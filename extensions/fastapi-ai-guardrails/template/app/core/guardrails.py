"""
FastAPI AI guardrails extension.
Provides typed guardrail hooks for input and output validation.
"""

from typing import Any, Callable, List, Optional, Union


class GuardrailError(Exception):
    """Raised when input or output violates guardrail rules."""


def apply_input_guardrails(
    input_data: Any,
    *,
    max_length: int = 1000,
    blocked_patterns: Optional[List[str]] = None,
    required_fields: Optional[List[str]] = None,
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

    # Check blocked patterns
    if blocked_patterns:
        for pattern in blocked_patterns:
            if pattern in str(input_data):
                raise GuardrailError(
                    f"Input contains blocked pattern: {pattern}"
                )

    return input_data


def apply_output_guardrails(
    output_data: Any,
    *,
    max_length: int = 1000,
    blocked_patterns: Optional[List[str]] = None,
    required_fields: Optional[List[str]] = None,
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

    # Check blocked patterns
    if blocked_patterns:
        for pattern in blocked_patterns:
            if pattern in str(output_data):
                raise GuardrailError(
                    f"Output contains blocked pattern: {pattern}"
                )

    return output_data
