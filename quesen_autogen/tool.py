"""
AutoGen v0.4+ tool functions for Quesen.

AutoGen's tool contract in the v0.4 series is a plain (async) Python callable
with type-annotated signatures. That is trivially compatible with the Quesen
SDK's typed methods; the wrappers below are thin async shims that:
  • read `QUESEN_BASE_URL` + `QUESEN_API_KEY` from env (or accept a shared client),
  • return the raw dict envelope so the agent can reason over it verbatim,
  • fail-closed by re-raising the SDK's typed exceptions.

Doctrine anchors:
  - §2 Determinism preserved: no prompt tuning, no randomness in the wrapper.
  - §11 Ecosystem neutrality: no autogen import forced at import-time — users
    who never touch autogen still get functional wrappers.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

try:
    from quesen_sdk import AsyncQuesenClient
    from quesen_sdk.tsc import TscContext
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-autogen requires `quesen-sdk`. Install with `pip install quesen-sdk`."
    ) from exc


_shared_client: Optional[AsyncQuesenClient] = None
_sandbox_ready: bool = False


async def _client() -> AsyncQuesenClient:
    global _shared_client, _sandbox_ready
    if _shared_client is None:
        base_url = os.environ.get("QUESEN_BASE_URL")
        if not base_url:
            raise RuntimeError(
                "quesen-autogen: set QUESEN_BASE_URL (and optionally QUESEN_API_KEY) "
                "before invoking the tools."
            )
        _shared_client = AsyncQuesenClient(
            base_url=base_url, api_key=os.environ.get("QUESEN_API_KEY"),
        )
    # If configured for the sandbox (QUESEN_SANDBOX=1) and no key is set, mint one.
    if (not _sandbox_ready and not _shared_client.api_key
            and os.environ.get("QUESEN_SANDBOX", "").lower() in ("1", "true", "yes")):
        await _shared_client.create_sandbox_key()
        _sandbox_ready = True
    return _shared_client


_EGRESS = {"send_data", "data_egress", "egress", "exfiltrate", "http_post", "upload"}
_PAYMENT = {"payment", "pay", "transfer", "send_funds", "send_money"}


async def quesen_firewall(
    action: str = "tool_call",
    agent: Optional[str] = None,
    target: Optional[str] = None,
    data_class: Optional[Any] = None,
    capability_class: Optional[str] = None,
    granted_scopes: Optional[list] = None,
    requested_scopes: Optional[list] = None,
    client_request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Agent firewall (TSC v2): deterministic PASS / REVIEW / BLOCK / SKIP + audit
    receipt for a high-risk action, BEFORE it crosses a trust boundary.

    Call this before sending data out (`action='send_data'`, `data_class='secret'`),
    invoking a tool (`action='tool_call'`), or a payment (`action='payment'`).
    Requires an engine with `QUESEN_TSC_V2_ENABLED=true`."""
    act = (action or "tool_call").lower()
    classes = None
    if data_class is not None:
        classes = [data_class] if isinstance(data_class, str) else list(data_class)
    if act in _EGRESS:
        ctx = TscContext.data_egress(
            data_classes=classes or ["unknown"], to=target or "unknown",
            provenance="adapter_derived", client_request_id=client_request_id,
        )
    elif act in _PAYMENT:
        ctx = TscContext.payment(
            granted_scopes=granted_scopes, provenance="client_asserted",
            client_request_id=client_request_id,
        )
    else:
        ctx = TscContext.tool_call(
            capability_class=capability_class or "other",
            granted_scopes=granted_scopes, requested_scopes=requested_scopes,
            provenance="adapter_derived", client_request_id=client_request_id,
        )
    d = await (await _client()).validate_tsc(ctx)
    return d.raw


async def quesen_validate(
    domain_age_days: Optional[int] = None,
    engagement_ratio: Optional[float] = None,
    scam_keyword_count: Optional[int] = None,
    client_request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Deterministic PROCEED / REVIEW / SKIP verdict.

    Call this BEFORE any high-consequence action. Returns the verdict + risk_score
    + confidence + conflict_triggers. Same input -> same output.
    """
    r = await (await _client()).validate(
        domain_age_days=domain_age_days,
        engagement_ratio=engagement_ratio,
        scam_keyword_count=scam_keyword_count,
        client_request_id=client_request_id,
    )
    return r.raw


async def quesen_simulate(
    domain_age_days: Optional[int] = None,
    engagement_ratio: Optional[float] = None,
    scam_keyword_count: Optional[int] = None,
    weights_override: Optional[Dict[str, float]] = None,
    thresholds_override: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Free counterfactual scoring. Not charged."""
    r = await (await _client()).simulate(
        domain_age_days=domain_age_days,
        engagement_ratio=engagement_ratio,
        scam_keyword_count=scam_keyword_count,
        weights_override=weights_override,
        thresholds_override=thresholds_override,
    )
    return r.raw


async def quesen_report(
    request_id: str,
    outcome: str,
    notes: Optional[str] = None,
    realized_pnl: Optional[float] = None,
    elapsed_seconds: Optional[int] = None,
    venue: Optional[str] = None,
    signal_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Post-decision outcome feedback (v1.1 schema).

    Pass the request_id returned by quesen_validate + an outcome enum
    (RUG | LOSS | OK | WIN | UNKNOWN). Optional post-trade metadata improves
    the aggregate quality signal.
    """
    r = await (await _client()).report(
        request_id=request_id,
        outcome=outcome,
        notes=notes,
        realized_pnl=realized_pnl,
        elapsed_seconds=elapsed_seconds,
        venue=venue,
        signal_hash=signal_hash,
    )
    return r.raw
