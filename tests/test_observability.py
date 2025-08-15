"""Tests for logging redaction, correlation IDs and signal extraction metrics."""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api import main as api
from services.connectors import Connector
from services.observability import (
    configure_logging,
    correlation_id,
    export_metrics,
    reset_metrics,
)


def test_logging_redacts_pii_and_adds_cid(capfd):
    configure_logging()
    correlation_id.set("cid123")
    logging.getLogger("test").info("contact alice@example.com on +61 1234 5678")
    out = capfd.readouterr().err.strip().splitlines()[-1]
    record = json.loads(out)
    assert record["cid"] == "cid123"
    assert "[REDACTED]" in record["msg"]


def test_signal_extraction_precision_recall():
    dataset = [
        (
            "Email alice@example.com or bob@example.net and call +61 1234 5678",
            {
                "emails": {"alice@example.com", "bob@example.net"},
                "domains": {"example.com", "example.net"},
                "phones": {"+61 1234 5678"},
                "usernames": set(),
                "locations": set(),
            },
        ),
        (
            "Visit https://example.org and follow @alice",
            {
                "emails": set(),
                "domains": {"example.org"},
                "phones": set(),
                "usernames": {"@alice"},
                "locations": set(),
            },
        ),
    ]
    tp = fp = fn = 0
    for text, labels in dataset:
        found = api.extract_signals(text)
        for key, expected in labels.items():
            fset = set(found[key])
            tp += len(fset & expected)
            fp += len(fset - expected)
            fn += len(expected - fset)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    assert precision >= 0.8 and recall >= 0.8


class _FastConnector(Connector):
    source = "fast"

    async def _search(self, query: str, **kwargs):
        await asyncio.sleep(0.01)
        return []


def test_basic_load(monkeypatch):
    monkeypatch.setattr(api, "CONNECTORS", [_FastConnector()])
    tasks = [api.search(q=str(i), type="person") for i in range(5)]

    async def run_all():
        await asyncio.gather(*tasks)

    start = time.time()
    asyncio.run(run_all())
    assert time.time() - start < 2  # completes quickly


class _MetricsConnector(Connector):
    source = "metric"

    async def _search(self, query: str, **kwargs):
        doc = {
            "title": "t",
            "summary": "s",
            "url": "https://example.com",
            "source": self.source,
            "fetched_at": "2024-01-01T00:00:00Z",
            "raw": {"content": "s", "lang": "en", "region": "AU"},
        }
        return [doc, doc.copy()]


class _FailConnector(Connector):
    source = "fail"

    async def _search(self, query: str, **kwargs):
        class Boom(Exception):
            code = 429

        raise Boom()


def test_metrics_recording(monkeypatch):
    reset_metrics()
    monkeypatch.setattr(api, "CONNECTORS", [_MetricsConnector()])
    asyncio.run(api.search(q="x", type="person"))
    metrics = asyncio.run(api.metrics())
    assert metrics["connector_calls"]["metric"] == 1
    assert metrics["connector_success"]["metric"] == 1
    assert metrics["dedupe_ratio"] == 0.5
    assert metrics["source_mix"]["en-AU"] == 2


def test_metrics_error(monkeypatch):
    reset_metrics()
    monkeypatch.setattr(api, "CONNECTORS", [_FailConnector()])
    asyncio.run(api.search(q="x", type="person"))
    metrics = asyncio.run(api.metrics())
    assert metrics["connector_calls"]["fail"] == 1
    assert metrics["connector_status"]["fail"][429] == 1
