"""Unit tests for connector framework and implementations."""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import services.connectors as connectors
from services.connectors import (
    GitHubUsersConnector,
    GoogleNewsConnector,
    MediaWikiConnector,
    RDAPConnector,
    WikidataConnector,
)


def test_mediawiki_connector(monkeypatch):
    async def fake_fetch_json(url, host):
        return {
            "query": {"search": [{"title": "Alice", "snippet": "Alice <b>Smith</b>"}]}
        }

    monkeypatch.setattr(connectors, "_fetch_json", fake_fetch_json)
    docs = asyncio.run(MediaWikiConnector().search("alice"))
    assert docs and docs[0]["source"] == "wikipedia"


def test_google_news_connector(monkeypatch):
    async def fake_fetch_text(url, host):
        return (
            "<rss><channel><item><title>News</title><link>https://example.com"
            "</link><description>Summary</description></item></channel></rss>"
        )

    monkeypatch.setattr(connectors, "_fetch_text", fake_fetch_text)
    docs = asyncio.run(GoogleNewsConnector().search("test"))
    assert docs[0]["url"] == "https://example.com"


def test_rdap_connector_domain_only(monkeypatch):
    async def fake_fetch_json(url, host):
        return {"name": "example.com"}

    monkeypatch.setattr(connectors, "_fetch_json", fake_fetch_json)
    connector = RDAPConnector()
    docs = asyncio.run(connector.search("example.com"))
    assert docs and docs[0]["source"] == "rdap"
    assert asyncio.run(connector.search("notadomain")) == []


def test_github_users_connector(monkeypatch):
    async def fake_fetch_json(url, host):
        return {
            "login": "octocat",
            "html_url": "https://github.com/octocat",
            "bio": "hi",
        }

    monkeypatch.setattr(connectors, "_fetch_json", fake_fetch_json)
    docs = asyncio.run(GitHubUsersConnector().search("octocat"))
    assert docs[0]["title"] == "octocat"


def test_stub_connectors_return_empty():
    docs = asyncio.run(WikidataConnector().search("foo"))
    assert docs == []


def test_connector_handles_error(monkeypatch, caplog):
    async def bad_fetch_json(url, host):
        raise ValueError("boom")

    caplog.set_level("ERROR")
    monkeypatch.setattr(connectors, "_fetch_json", bad_fetch_json)
    docs = asyncio.run(MediaWikiConnector().search("alice"))
    assert docs == []
    assert "connector_error" in caplog.text
