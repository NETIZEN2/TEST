"""Lightweight observability helpers for metrics, logging and tracing.

This module intentionally keeps implementations minimal so the rest of the
codebase can depend on a single place for instrumentation without pulling in
heavy third‑party dependencies.  Metrics are stored in process and intended
for testing/demo purposes.
"""

from __future__ import annotations

import json
import logging
import re
import time
from collections import defaultdict
from contextvars import ContextVar
from typing import Dict, Iterable

# ---------------------------------------------------------------------------
# Correlation IDs and logging
# ---------------------------------------------------------------------------

# Correlation ID available to any code running within a request context.
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")

# Regexes for basic PII redaction in logs.
EMAIL_RE = re.compile(r"[\w.\-]+@[\w.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{7,}\d")


class RedactingJSONFormatter(logging.Formatter):
    """Format log records as JSON while redacting obvious PII."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - trivial
        msg = record.getMessage()
        msg = EMAIL_RE.sub("[REDACTED]", msg)
        msg = PHONE_RE.sub("[REDACTED]", msg)
        data = {
            "level": record.levelname,
            "msg": msg,
            "cid": correlation_id.get(),
        }
        for key, value in record.__dict__.get("extra", {}).items():
            data[key] = value
        return json.dumps(data)


def configure_logging() -> None:
    """Configure root logger for JSON output with redaction."""

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingJSONFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Metrics helpers
# ---------------------------------------------------------------------------

_connector_calls: Dict[str, int] = defaultdict(int)
_connector_success: Dict[str, int] = defaultdict(int)
_connector_status: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
_connector_latency: Dict[str, list] = defaultdict(list)
_source_mix: Dict[str, int] = defaultdict(int)
_dedupe_ratio: float = 0.0


def record_connector_metric(connector: str, status: int, latency_ms: int) -> None:
    """Record outcome of a connector invocation."""

    _connector_calls[connector] += 1
    if status == 200:
        _connector_success[connector] += 1
    elif status:
        if status == 429:
            _connector_status[connector][429] += 1
        elif status >= 500:
            _connector_status[connector][status] += 1
    _connector_latency[connector].append(latency_ms)


def record_source(language: str, region: str = "unknown") -> None:
    """Record language and region for source mix statistics."""

    key = f"{language or 'unknown'}-{region or 'unknown'}"
    _source_mix[key] += 1


def set_dedupe_ratio(total: int, unique: int) -> None:
    """Record deduplication ratio for last pipeline run."""

    global _dedupe_ratio
    _dedupe_ratio = unique / total if total else 0.0


def export_metrics() -> Dict[str, Dict]:
    """Return a snapshot of current metrics."""

    avg_latency = {
        k: (sum(v) / len(v) if v else 0.0) for k, v in _connector_latency.items()
    }
    return {
        "connector_calls": dict(_connector_calls),
        "connector_success": dict(_connector_success),
        "connector_status": {k: dict(v) for k, v in _connector_status.items()},
        "latency_ms": avg_latency,
        "dedupe_ratio": _dedupe_ratio,
        "source_mix": dict(_source_mix),
    }


def reset_metrics() -> None:
    """Reset all metric counters (useful for tests)."""

    _connector_calls.clear()
    _connector_success.clear()
    _connector_status.clear()
    _connector_latency.clear()
    _source_mix.clear()
    global _dedupe_ratio
    _dedupe_ratio = 0.0


# ---------------------------------------------------------------------------
# Tracing (OpenTelemetry with graceful fallback)
# ---------------------------------------------------------------------------

try:  # pragma: no cover - exercised in runtime only
    from opentelemetry import trace  # type: ignore
except Exception:  # pragma: no cover - fallback

    class _NoopTracer:  # minimal stub
        def start_as_current_span(self, name: str):
            return _NullContext()

    class _NullContext:
        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    class _Trace:
        def get_tracer(self, name: str):
            return _NoopTracer()

    trace = _Trace()  # type: ignore


tracer = trace.get_tracer("osint-pro")
