# FastAPI AI Guardrails Guide

## Introduction

This guide provides comprehensive documentation for the FastAPI AI Guardrails extension, including setup, configuration, and best practices for implementing input/output validation in your AI applications.

## Overview

The FastAPI AI Guardrails extension ensures that AI-generated and user-provided data meets safety and quality standards through configurable validation rules.

## Installation

Add the extension to your project:

```bash
pip install fastapi-ai-guardrails
```

Or add to your `extension-addons` in `cpa.config.json`:

```json
{
  "extension-addons": ["fastapi-ai-guardrails"]
}
```

## Quick Start

### 1. Create Extension Directory

```bash
mkdir -p extensions/fastapi-ai-guardrails/template/app/core
mkdir -p extensions/fastapi-ai-guardrails/template/tests
```

### 2. Set Up Core Module

Add `guardrails.py` to `template/app/core/`:

```python
"""FastAPI AI guardrails extension."""

from typing import Any, List, Optional

class GuardrailError(Exception):
    """Raised when input or output violates guardrail rules."""

def apply_input_guardrails(input_data: Any, **kwargs) -> Any:
    """Validate input data against guardrail rules."""
    # Your validation logic here
    return input_data

def apply_output_guardrails(output_data: Any, **kwargs) -> Any:
    """Validate output data against guardrail rules."""
    # Your validation logic here
    return output_data
```

### 3. Add Tests

Create comprehensive tests for all guardrail scenarios.

## Core Features

### Input Validation

The extension provides several input validation mechanisms:

#### 1. Required Fields

Ensure critical fields are present in input data:

```python
apply_input_guardrails(
    user_data,
    required_fields=["user_id", "email", "preferences"]
)
```

#### 2. Maximum Length

Limit string lengths to prevent excessive processing:

```python
apply_input_guardrails(
    long_text,
    max_length=1000
)
```

#### 3. Blocked Patterns

Prevent dangerous or inappropriate content:

```python
apply_input_guardrails(
    user_input,
    blocked_patterns=["password", "secret", "admin"]
)
```

### Output Validation

Similarly, validate AI-generated outputs:

```python
apply_output_guardrails(
    model_response,
    required_fields=["answer", "confidence"],
    max_length=500,
    blocked_patterns=["@", "mailto:"]
)
```

## Configuration

### Environment Variables

Set guardrail configuration via environment variables:

```bash
export GUARDRAILS_MAX_LENGTH=1000
export GUARDRAILS_BLOCKED_PATTERNS="ignore,bypass,override"
export GUARDRAILS_REQUIRED_FIELDS="user_id,session_id"
```

### Config File

Create `config/guardrails.yaml`:

```yaml
input:
  max_length: 1000
  blocked_patterns:
    - "ignore previous instructions"
    - "delete everything"
    - "bypass security"
  required_fields:
    - "user_id"
    - "session_id"
    - "timestamp"

output:
  max_length: 500
  blocked_patterns:
    - "@"
    - "mailto:"
    - "tel:"
    - "password"
  required_fields:
    - "answer"
    - "confidence"
    - "source"
```

## Best Practices

### 1. Defense in Depth

Implement multiple layers of validation:

```python
# Layer 1: Basic validation
validated = apply_input_guardrails(user_input)

# Layer 2: Additional business rules
validated = business_logic.validate(validated)

# Layer 3: AI-specific checks
validated = ai_safety.check(validated)
```

### 2. Error Handling

Handle guardrail errors gracefully:

```python
from fastapi_ai_guardrails import GuardrailError

try:
    validated = apply_input_guardrails(user_input)
except GuardrailError as e:
    # Log the error
    logger.warning(f"Guardrail error: {e}")
    # Return user-friendly error message
    return {"error": "Invalid input format", "details": str(e)}, 400
```

### 3. Performance Considerations

- Cache blocked patterns compilation
- Use efficient string matching algorithms
- Consider parallel validation for multiple fields
- Implement input truncation instead of rejection when appropriate

## Common Use Cases

### 1. Chat Application Guardrails

```python
# Input guardrails for chat messages
chat_guardrails = {
    "max_length": 1000,
    "blocked_patterns": [
        "ignore previous instructions",
        "system prompt",
        "bypass",
        "override"
    ],
    "required_fields": ["user_id", "message"]
}

# Output guardrails for AI responses
response_guardrails = {
    "max_length": 500,
    "blocked_patterns": ["@", "mailto:", "password"],
    "required_fields": ["text", "confidence"]
}
```

### 2. Data Processing Pipeline

```python
# Validate incoming data
processed = apply_input_guardrails(data, **input_config)

# Process with AI model
result = ai_model.process(processed)

# Validate output
final_output = apply_output_guardrails(result, **output_config)
```

## Testing Your Guardrails

### Unit Tests

```python
def test_input_guardrails():
    # Test valid input
    assert apply_input_guardrails("hello") == "hello"
    
    # Test blocked pattern
    with pytest.raises(GuardrailError):
        apply_input_guardrails("delete everything")
    
    # Test length limit
    with pytest.raises(GuardrailError):
        apply_input_guardrails("x" * 1001)
```

### Integration Tests

Test guardrails within your actual application flow.

## Troubleshooting

### Common Issues

**Issue**: Guardrails rejecting valid input

**Solution**: Check your blocked patterns and required fields configuration. Ensure patterns are appropriate for your use case.

**Issue**: Performance degradation with many guardrails

**Solution**: Profile your guardrail implementation and optimize matching algorithms.

**Issue**: Guardrails not being applied

**Solution**: Verify extension is properly installed and added to `extension-addons`.

### Debug Mode

Set `DEBUG_GUARDRAILS=1` to enable detailed error messages and validation logging.

## Future Enhancements

Consider implementing:

1. **AI-Generated Guardrails**: Use ML models to detect novel attack patterns
2. **Contextual Validation**: Understand conversation context for better validation
3. **Compliance Checks**: Validate against industry-specific regulations
4. **Real-time Monitoring**: Track guardrail effectiveness and false positives

## Related Extensions

This extension works well with:

- `fastapi-ai-chat`: For chat applications
- `fastapi-ai-langgraph`: For complex workflow orchestration
- `fastapi-ai-rag`: For retrieval-augmented generation

## License

MIT