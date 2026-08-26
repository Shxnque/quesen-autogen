# Quesen — AutoGen Tool

> Deterministic **Agent Firewall** + A2A risk validation exposed as AutoGen (v0.4+) function tools.

**Status:** v0.3.0 · tracks Quesen engine v1.10.0 (TSC v2 firewall) · requires `quesen-sdk>=0.4.1`.
**Developer portal:** https://senueren.co.za/quesen · **Source:** https://github.com/Shxnque/quesen

---

## Agent Firewall (no signup)

```python
import os, asyncio
os.environ["QUESEN_BASE_URL"] = "https://web-production-aa5ba.up.railway.app"
os.environ["QUESEN_SANDBOX"] = "1"          # self-serve a free key

from quesen_autogen import quesen_firewall   # register on any AutoGen agent's tools

async def main():
    v = await quesen_firewall(action="send_data",
                              target="https://paste.evil.example", data_class="secret")
    print(v["decision"])                      # 'BLOCK'
asyncio.run(main())
```


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

## Receipt provenance (v1.10)

`quesen_validate(...)` returns the raw response dict from `AsyncQuesenClient`.
Against a v1.10.0+ engine the dict includes:

- `input_snapshot_hash` — SHA-256 over canonical request JSON.
- `commit_sha` — git SHA of the engine ruleset live at decision time (or `"unknown"`).

See the [public API reference](https://github.com/Shxnque/quesen/blob/main/docs/api-reference.md#receipt-provenance-v110).

## Tools shipped

- `quesen_validate(...)` — wraps `/validate` (carries v1.10 provenance)
- `quesen_simulate(...)` — wraps `/simulate`
- `quesen_report(...)` — wraps `/report` (v1.1 schema)

Each is a plain async Python function with type-annotated arguments — AutoGen consumes those signatures directly.

MIT license. See [`senueren.co.za/quesen`](https://senueren.co.za/quesen) for canonical documentation.
