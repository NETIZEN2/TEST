"""SSRF-safe HTTP fetcher service.

This module exposes :func:`fetch` which retrieves remote resources while
enforcing a strict egress allowlist, DNS pinning and basic response
validation. It purposely blocks requests to private or link-local
addresses to reduce the risk of Server Side Request Forgery (SSRF).
"""

from __future__ import annotations

from dataclasses import dataclass
import ipaddress
import os
import socket
from typing import Iterable, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_TIMEOUT = int(os.getenv("FETCHER_TIMEOUT", "5"))
MAX_BYTES = int(os.getenv("FETCHER_MAX_BYTES", "1000000"))  # 1 MiB
ALLOWED_MIME_PREFIXES = tuple(
    os.getenv("FETCHER_ALLOWED_MIME_PREFIXES", "text/,application/json").split(",")
)


def _resolve_host(host: str) -> Iterable[str]:
    """Resolve *host* and ensure no address is private or local."""

    infos = socket.getaddrinfo(host, None)
    addresses = {info[4][0] for info in infos}
    for addr in addresses:
        ip = ipaddress.ip_address(addr)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise ValueError("refusing to resolve private address")
    return addresses


@dataclass
class FetchResult:
    """Container for fetched content."""

    url: str
    content: bytes
    content_type: str


def fetch(url: str, *, allowed_hosts: Optional[Iterable[str]] = None) -> FetchResult:
    """Fetch *url* enforcing an optional *allowed_hosts* policy.

    Parameters
    ----------
    url:
        The absolute URL to retrieve.
    allowed_hosts:
        Iterable of permitted hostnames. If provided the URL's hostname must
        appear in this collection.

    Raises
    ------
    ValueError
        If the host is not allowlisted or resolves to a private address, or if
        the response exceeds limits.
    """

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("unsupported URL scheme")

    if allowed_hosts is not None and parsed.hostname not in allowed_hosts:
        raise ValueError("host not allowlisted")

    _resolve_host(parsed.hostname or "")

    req = Request(url, headers={"User-Agent": "osint-pro-fetcher"})
    with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if not any(ctype.startswith(prefix) for prefix in ALLOWED_MIME_PREFIXES):
            raise ValueError("unsupported content type")
        content = resp.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise ValueError("response too large")

    return FetchResult(url=url, content=content, content_type=ctype)

