"""Golden-file tests for document normalisation and dedupe metrics."""
import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api import main as api
from services.connectors import Connector
from services.observability import reset_metrics, export_metrics


def test_normalise_doc_matches_golden():
    raw = {
        "title": "T",
        "summary": "S",
        "url": "https://example.com/foo/",
        "source": "x",
        "fetched_at": "2023-01-01T00:00:00",
        "raw": {"content": "hi"},
    }
    result = api.normalise_doc(raw)
    golden_path = Path(__file__).parent / "golden" / "normalised_doc.json"
    golden = json.loads(golden_path.read_text())
    assert result == golden


class _DupConnector(Connector):
    source = "dup"

    async def _search(self, query: str, **kwargs):
        return [
            {
                "title": "t",
                "summary": "s",
                "url": "https://example.com/a",
                "source": self.source,
                "fetched_at": "2023",
                "raw": {"content": "x"},
            },
            {
                "title": "t",
                "summary": "s",
                "url": "https://example.com/a",
                "source": self.source,
                "fetched_at": "2023",
                "raw": {"content": "x"},
            },
        ]


def test_dedupe_ratio_metric(monkeypatch):
    reset_metrics()
    monkeypatch.setattr(api, "CONNECTORS", [_DupConnector()])
    asyncio.run(api.search(q="x", type="person"))
    metrics = export_metrics()
    assert metrics["dedupe_ratio"] == 0.5
