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
    result = asyncio.run(profile(q="alice", type="person"))
    assert "alice@example.com" in result["signals"]["emails"]
    assert result["confidence"] <= 1
    assert result["query"] == "alice"
