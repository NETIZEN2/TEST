"""Chaos tests ensuring connector outages do not break the pipeline."""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api import main as api
from services.connectors import Connector


class DummyConnector(Connector):
    source = "dummy"

    async def _search(self, query: str, **kwargs):
        content = f"News on {query} at {datetime.utcnow().isoformat()}"
        return [
            {
                "title": "Example",
                "summary": content,
                "url": "https://example.com/1",
                "source": self.source,
                "fetched_at": datetime.utcnow().isoformat(),
                "raw": {"content": content},
            }
        ]


class FailingConnector(Connector):
    source = "fail"

    async def _search(self, query: str, **kwargs):
        raise ValueError("boom")


@pytest.fixture(autouse=True)
def patch_connectors():
    original = api.CONNECTORS[:]
    api.CONNECTORS[:] = [FailingConnector(), DummyConnector()]
    yield
    api.CONNECTORS[:] = original


def test_pipeline_survives_outage():
    result = asyncio.run(api.search(q="alice", type="person"))
    assert result["count"] == 1
