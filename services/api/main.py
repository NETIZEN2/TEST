"""FastAPI service implementing deterministic OSINT pipeline."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse, urlunparse

from dataclasses import dataclass, field
from fastapi import FastAPI, HTTPException

from .audit_log import AuditLog

app = FastAPI()
audit_log = AuditLog()
# simple in-memory persistence stub
ENTITIES: Dict[str, dict] = {}


@dataclass
class DocModel:
    """Normalised document record."""

    id: str
    title: str
    summary: str
    url: str
    source: str
    fetched_at: str
    raw: dict
    hash: str
    classification: str = "OFFICIAL"
    provenance: dict = field(default_factory=dict)


@dataclass
class SearchResponse:
    query: str
    type: Optional[str]
    count: int
    docs: List[DocModel]


@dataclass
class EntityProfileModel:
    query: str
    type: str
    canonical_name: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    confidence: float = 0.0
    description: Optional[str] = None
    signals: dict = field(default_factory=dict)
    facts: dict = field(default_factory=dict)
    sources: List[DocModel] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def canonical_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme, parsed.netloc.lower(), path, "", "", ""))


def extract_signals(text: str) -> Dict[str, List[str]]:
    emails = re.findall(r"[\w.\-]+@[\w.\-]+\.[a-zA-Z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s-]{7,}\d", text)
    handles = re.findall(r"@\w+", text)
    domains = re.findall(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", text)
    return {
        "emails": emails,
        "domains": domains,
        "usernames": handles,
        "phones": phones,
        "locations": [],  # TODO: NER for locations
    }


def normalise_doc(raw_doc: dict) -> dict:
    url = canonical_url(raw_doc["url"])
    content = raw_doc.get("raw", {}).get("content", "")
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    doc_id = content_hash[:8]
    return {
        "id": doc_id,
        "title": raw_doc.get("title", ""),
        "summary": raw_doc.get("summary", ""),
        "url": url,
        "source": raw_doc.get("source", ""),
        "fetched_at": raw_doc.get("fetched_at", datetime.utcnow().isoformat()),
        "raw": raw_doc.get("raw", {}),
        "hash": content_hash,
        "classification": "OFFICIAL",
        "provenance": {
            "url": url,
            "fetched_at": raw_doc.get("fetched_at", ""),
            "content_hash": content_hash,
            "connector": raw_doc.get("source", ""),
        },
    }


async def connector_example(query: str) -> List[dict]:
    """Dummy connector returning deterministic data."""

    await asyncio.sleep(0)  # simulate IO
    content = f"Contact alice@example.com for more on {query}."
    doc = {
        "title": "Example Title",
        "summary": "Example Summary",
        "url": "https://example.com/article",
        "source": "example",
        "fetched_at": datetime.utcnow().isoformat(),
        "raw": {"content": content},
    }
    # return duplicate to exercise dedupe logic
    return [doc, doc.copy()]


async def run_connectors(query: str) -> List[dict]:
    """Run all connectors concurrently for *query*."""

    results = await asyncio.gather(connector_example(query))
    # flatten
    return [doc for docs in results for doc in docs]


def audit(action: str, target: str, metadata: dict) -> None:
    audit_log.append(
        {
            "ts": datetime.utcnow().isoformat(),
            "actor": "system",
            "action": action,
            "target": target,
            "metadata": metadata,
        }
    )


async def pipeline_search(query: str) -> List[dict]:
    raw_docs = await run_connectors(query)
    seen = set()
    docs: List[dict] = []
    for raw in raw_docs:
        doc = normalise_doc(raw)
        if doc["url"] in seen:
            continue
        seen.add(doc["url"])
        docs.append(doc)
    return docs


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
"""FastAPI service entry point."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""

    return {"status": "ok"}


@app.get("/search", response_model=SearchResponse)
async def search(q: str, type: Optional[str] = None):
    start = time.time()
    audit("search_start", q, {})
    docs = await pipeline_search(q)
    audit("search_end", q, {"count": len(docs), "latency_ms": int((time.time() - start) * 1000)})
    return {"query": q, "type": type, "count": len(docs), "docs": docs}


@app.get("/profile", response_model=EntityProfileModel)
async def profile(q: str, type: str):
    start = time.time()
    audit("profile_start", q, {"type": type})
    docs = await pipeline_search(q)
    signals: Dict[str, List[str]] = {"emails": [], "domains": [], "usernames": [], "phones": [], "locations": []}
    title_counts: Dict[str, int] = {}
    description = None
    for d in docs:
        content = d["raw"].get("content", "")
        sig = extract_signals(content)
        for k, v in sig.items():
            signals[k].extend(v)
        title_counts[d["title"]] = title_counts.get(d["title"], 0) + 1
        if d["source"].lower() in {"wikipedia", "wikidata"} and not description:
            description = d["summary"]
    canonical_name = max(title_counts, key=title_counts.get) if title_counts else q
    aliases = [t for t in title_counts if t != canonical_name]
    confidence = min(1.0, len(docs) / 5)
    profile = {
        "query": q,
        "type": type,
        "canonical_name": canonical_name,
        "aliases": aliases,
        "confidence": confidence,
        "description": description,
        "signals": {k: sorted(set(v)) for k, v in signals.items()},
        "facts": {},
        "sources": docs,
    }
    audit("profile_end", q, {"count": len(docs), "latency_ms": int((time.time() - start) * 1000)})
    if os.getenv("PERSIST_STUB") == "true":
        key = hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest()[:8]
        ENTITIES[key] = profile
        profile["id"] = key
    return profile


@app.post("/entities")
async def create_entity(profile: EntityProfileModel):
    data = profile.dict()
    key = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:8]
    ENTITIES[key] = data
    return {"id": key}


@app.get("/entities/{entity_id}")
async def get_entity(entity_id: str):
    if entity_id not in ENTITIES:
        raise HTTPException(404, "entity not found")
    return ENTITIES[entity_id]


@app.post("/export")
async def export(profile: EntityProfileModel, format: str = "json"):
    if format not in {"json", "pdf"}:
        raise HTTPException(400, "unsupported format")
    # stub: just return the profile
    return profile
    return {"status": "ok"}
