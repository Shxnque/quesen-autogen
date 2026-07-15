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
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-autogen requires `quesen-sdk`. Install with `pip install quesen-sdk`."
    ) from exc


_shared_client: Optional[AsyncQuesenClient] = None


def _client() -> AsyncQuesenClient:
    global _shared_client
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
    return _shared_client


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
    r = await _client().validate(
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
    r = await _client().simulate(
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
    r = await _client().report(
        request_id=request_id,
        outcome=outcome,
        notes=notes,
        realized_pnl=realized_pnl,
        elapsed_seconds=elapsed_seconds,
        venue=venue,
        signal_hash=signal_hash,
    )
    return r.raw
