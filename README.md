# Quesen — AutoGen Tool

> Deterministic A2A risk validation exposed as AutoGen (v0.4+) function tools.

**Parent repo:** https://github.com/Shxnque/Quesen-sib

---

## Install

```bash
pip install quesen-autogen
# or:
pip install git+https://github.com/Shxnque/quesen-autogen.git
```

## 30-second usage (AutoGen v0.4+)

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from quesen_autogen import quesen_validate, quesen_simulate, quesen_report

model = OpenAIChatCompletionClient(model="gpt-4o-mini")
agent = AssistantAgent(
    name="defensive_trader",
    model_client=model,
    tools=[quesen_validate, quesen_simulate, quesen_report],
    system_message=(
        "Before any high-stakes action, call quesen_validate. "
        "Do not proceed unless the decision is PROCEED."
    ),
)
```

## Tools shipped

- `quesen_validate(...)` — wraps `/validate`
- `quesen_simulate(...)` — wraps `/simulate`
- `quesen_report(...)` — wraps `/report` (v1.1 schema)

Each is a plain async Python function with type-annotated arguments — AutoGen consumes those signatures directly.

MIT license. Extracted from `Shxnque/Quesen-sib` `sdks/autogen/`.
