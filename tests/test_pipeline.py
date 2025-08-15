"""Tests for deterministic search/profile pipeline using dummy connector."""
import asyncio
from datetime import datetime
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api import main as api
from services.connectors import Connector


class DummyConnector(Connector):
    source = "dummy"

    async def _search(self, query: str, **kwargs):  # pragma: no cover - simple stub
        content = f"Contact alice@example.com for more on {query}."
        doc = {
            "title": "Example Title",
            "summary": "Example Summary",
            "url": "https://example.com/article",
            "source": self.source,
            "fetched_at": datetime.utcnow().isoformat(),
            "raw": {"content": content},
        }
        return [doc, doc.copy()]


@pytest.fixture(autouse=True)
def patch_connectors():
    original = api.CONNECTORS[:]
    api.CONNECTORS[:] = [DummyConnector()]
    yield
    api.CONNECTORS[:] = original


def test_search_deduplicates_and_hashes():
    data = asyncio.run(api.search(q="alice", type="person"))
    assert data["count"] == 1
"""Tests for deterministic search/profile pipeline."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api.main import profile, search  # noqa: E402


def test_search_deduplicates_and_hashes():
    data = asyncio.run(search(q="alice", type="person"))
    assert data["count"] == 1  # duplicate URLs collapsed
    doc = data["docs"][0]
    assert doc["url"] == "https://example.com/article"
    assert len(doc["hash"]) == 64


def test_profile_extracts_signals():
    result = asyncio.run(api.profile(q="alice", type="person"))
    assert "alice@example.com" in result["signals"]["emails"]
    assert result["confidence"] <= 1
    assert result["query"] == "alice"


def test_profile_includes_advanced_facts(monkeypatch):
    monkeypatch.setenv("ADVANCED_FACTS", "true")
    result = asyncio.run(api.profile(q="alice", type="person"))
    assert set(result["facts"].keys()) == {"tech", "geo", "legal", "media"}
    result = asyncio.run(profile(q="alice", type="person"))
    assert "alice@example.com" in result["signals"]["emails"]
    assert result["confidence"] <= 1
    assert result["query"] == "alice"
