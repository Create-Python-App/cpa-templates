# fastapi-ai-guardrails

A FastAPI extension providing typed guardrail hooks for input and output validation in AI applications.

## Overview

This extension adds guardrail mechanisms to ensure that AI-generated or user-provided inputs and outputs meet certain quality and safety standards. It provides:

- **Input validation**: Checks for required fields, maximum length limits, and blocked patterns.
- **Output validation**: Ensures generated responses adhere to safety and formatting rules.
- **Extensible design**: Easy to customize guardrail rules for specific use cases.

## Installation

```bash
pip install fastapi-ai-guardrails
```

## Usage

Add the extension to your FastAPI application:

```python
from fastapi import FastAPI
from fastapi_ai_guardrails import apply_input_guardrails, apply_output_guardrails

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(
    user_message: str,
    model_response: dict,
):
    # Validate input
    validated_input = apply_input_guardrails(user_message)
    
    # Process the model
    processed = model.process(validated_input)
    
    # Validate output
    validated_output = apply_output_guardrails(processed)
    
    return {"response": validated_output}
```

## Guardrail Rules

### Input Validation

- **Required fields**: Ensure critical fields are present
- **Max length**: Limit string lengths to prevent excessive processing
- **Blocked patterns**: Prevent dangerous or inappropriate content

### Output Validation

- **Max length**: Cap response size
- **Blocked patterns**: Sanitize output for safety
- **Structured response checks**: Enforce expected schema

## Configuration

The extension accepts configurable parameters for each guardrail:

- `max_length`: Maximum allowed length for strings
- `blocked_patterns`: List of substrings to reject
- `required_fields`: Fields that must be present

## Testing

Run the test suite:

```bash
pytest extensions/fastapi-ai-guardrails/tests/test_guardrails.py -v
```

## License

MIT