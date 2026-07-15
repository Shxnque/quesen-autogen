"""AutoGen wrapper smoke tests — import + signature sanity."""

import inspect

import pytest

quesen_sdk = pytest.importorskip("quesen_sdk")

from quesen_autogen import quesen_report, quesen_simulate, quesen_validate


def test_validate_signature_annotations():
    sig = inspect.signature(quesen_validate)
    assert set(sig.parameters) == {
        "domain_age_days", "engagement_ratio", "scam_keyword_count", "client_request_id"
    }


def test_report_requires_request_id_and_outcome():
    sig = inspect.signature(quesen_report)
    positional = [
        p for p in sig.parameters.values()
        if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD,)
        and p.default is inspect.Parameter.empty
    ]
    names = {p.name for p in positional}
    assert {"request_id", "outcome"} <= names


def test_tools_are_coroutines():
    for fn in (quesen_validate, quesen_simulate, quesen_report):
        assert inspect.iscoroutinefunction(fn)
