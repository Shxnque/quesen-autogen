"""Quesen AutoGen integration — async function tools for AutoGen v0.4+.

Includes the Agent Firewall tool (TSC v2), the legacy A2A risk tools, and
(v0.4.0) the async fail-closed enforcement decorator `quesen_guard`.
"""

from .tool import (
    quesen_firewall,
    quesen_guard,
    quesen_report,
    quesen_simulate,
    quesen_validate,
)

__version__ = "0.5.0"

__all__ = [
    "__version__",
    "quesen_firewall",
    "quesen_guard",
    "quesen_validate",
    "quesen_simulate",
    "quesen_report",
]
