"""Connector framework with concrete implementations."""
import asyncio
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from services.fetcher.fetcher import fetch
from services.observability import record_connector_metric

logger = logging.getLogger(__name__)


class Connector(ABC):
    """Base connector providing rate limiting and error logging."""

    source: str = ""
    _semaphore = asyncio.Semaphore(1)

    async def search(
        self,
        query: str,
        type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
        timeout_ms: int = 10000,
    ) -> List[Dict[str, Any]]:
        start = time.time()
        status = 200
        try:
            async with self._semaphore:
                docs = await self._search(
                    query, type=type, context=context, limit=limit, timeout_ms=timeout_ms
                )
            return docs
        except Exception as exc:  # never raise
            status = getattr(exc, "code", 0)
            logger.error(
                "connector_error", extra={"connector": self.source, "error": str(exc)}
            )
            return []
        finally:
            latency = int((time.time() - start) * 1000)
            record_connector_metric(self.source, status, latency)

    @abstractmethod
    async def _search(
        self,
        query: str,
        type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
        timeout_ms: int = 10000,
    ) -> List[Dict[str, Any]]:
        ...


async def _fetch_json(url: str, allowed_host: str) -> Dict[str, Any]:
    for attempt in range(3):
        try:
            res = await asyncio.to_thread(fetch, url, allowed_hosts={allowed_host})
            return json.loads(res.content.decode())
        except Exception:
            if attempt == 2:
                raise
            await asyncio.sleep(0.5 * (2**attempt))
    return {}


async def _fetch_text(url: str, allowed_host: str) -> str:
    for attempt in range(3):
        try:
            res = await asyncio.to_thread(fetch, url, allowed_hosts={allowed_host})
            return res.content.decode()
        except Exception:
            if attempt == 2:
                raise
            await asyncio.sleep(0.5 * (2**attempt))
    return ""


def _is_domain(query: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}", query))


class MediaWikiConnector(Connector):
    source = "wikipedia"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        limit = kwargs.get("limit", 5)
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srsearch": query,
            "srlimit": limit,
        }
        url = f"https://en.wikipedia.org/w/api.php?{urlencode(params)}"
        data = await _fetch_json(url, "en.wikipedia.org")
        docs: List[Dict[str, Any]] = []
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            snippet = re.sub(r"<.*?>", "", item.get("snippet", ""))
            page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            docs.append(
                {
                    "title": title,
                    "summary": snippet,
                    "url": page_url,
                    "source": self.source,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "raw": {"content": snippet, "item": item},
                }
            )
        return docs


class GoogleNewsConnector(Connector):
    source = "google_news"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        limit = kwargs.get("limit", 5)
        params = {"q": query, "hl": "en-AU", "gl": "AU", "ceid": "AU:en"}
        url = f"https://news.google.com/rss/search?{urlencode(params)}"
        text = await _fetch_text(url, "news.google.com")
        root = ET.fromstring(text or "<rss/>")
        docs: List[Dict[str, Any]] = []
        for item in root.findall("channel/item")[:limit]:
            title = item.findtext("title", default="")
            link = item.findtext("link", default="")
            summary = item.findtext("description", default="")
            docs.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "source": self.source,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "raw": {"content": summary},
                }
            )
        return docs


class RDAPConnector(Connector):
    source = "rdap"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        if not _is_domain(query):
            return []
        url = f"https://rdap.org/domain/{query}"
        data = await _fetch_json(url, "rdap.org")
        return [
            {
                "title": f"RDAP data for {query}",
                "summary": data.get("name", ""),
                "url": url,
                "source": self.source,
                "fetched_at": datetime.utcnow().isoformat(),
                "raw": data,
            }
        ]


class GitHubUsersConnector(Connector):
    source = "github_users"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/users/{query}"
        data = await _fetch_json(url, "api.github.com")
        if not data:
            return []
        return [
            {
                "title": data.get("login", ""),
                "summary": data.get("bio", "") or "",
                "url": data.get("html_url", ""),
                "source": self.source,
                "fetched_at": datetime.utcnow().isoformat(),
                "raw": data,
            }
        ]


# Phase-1 stub connectors ---------------------------------------------------


class WikidataConnector(Connector):
    source = "wikidata"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class OpenAlexConnector(Connector):
    source = "openalex"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class AbnLookupConnector(Connector):
    source = "abn_lookup"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class SecEdgarConnector(Connector):
    source = "sec_edgar"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class CompaniesHouseConnector(Connector):
    source = "companies_house"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class OpenCorporatesConnector(Connector):
    source = "open_corporates"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class GdeltConnector(Connector):
    source = "gdelt"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class CrtShConnector(Connector):
    source = "crt_sh"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []


class WaybackConnector(Connector):
    source = "wayback"

    async def _search(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        return []
