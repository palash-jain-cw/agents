## Agents Package

Lightweight wrappers for building AI agents across pluggable providers. Includes core agent orchestration, provider-specific clients, and shared helpers for structured responses. Bedrock (Anthropic) is the first provider; additional providers can be added behind the same interface.

## Quick Start
- Install deps with uv (recommended):
  - `uv sync`
- Configure provider credentials:
  - For Bedrock (current built-in):
    - `AWS_ACCESS_KEY_ID=...`
    - `AWS_SECRET_ACCESS_KEY=...`
    - `AWS_DEFAULT_REGION=...`
  - Future providers: add their env vars similarly.
- Run a simple agent:
  - `python -m agents.core.base` (see sample below)

## Minimal Usage
```python
from agents.core.base import Agent
from agents.core.models import StringRequest

agent = Agent(name="demo")
response, usage = agent.run(StringRequest(request="Hello!"))
print(response)
print(usage)
```

## Structure
- `agents/core`: Agent wrapper, settings, logging defaults, base Pydantic models.
- `agents/providers/bedrock`: Bedrock Anthropic client + content formatters.
- `agents/providers/<new>`: Add new providers by implementing a client with the same `query()` signature and wiring it in `Agent.resolve_provider()`.
- `agents/shared`: Utilities for parsing structured model responses.
- `notebooks`: Walkthroughs (`PJ_01_Settings`, `PJ_02_Bedrock_Provider`, `PJ_03_Base_Agent`).

## Logging
Logging config is initialized on import (`agents.core.logging_config`). Customize by adjusting level/format in `configure_logging()` if needed.

## Notes
- The Bedrock client validates AWS env vars before use and raises if missing.
- Structured output parsing assumes JSON enclosed in the first/last braces of the model response.
