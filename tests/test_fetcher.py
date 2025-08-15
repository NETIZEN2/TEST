"""Unit tests for the SSRF-safe fetcher."""

import sys
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.fetcher.fetcher import FetchResult, fetch


class DummyResponse:
    def __init__(self, content: bytes, content_type: str = "text/plain"):
        self.headers = {"Content-Type": content_type}
        self._content = content

    def read(self, n: int):  # pragma: no cover - simple read
        return self._content


@mock.patch("services.fetcher.fetcher.urlopen")
@mock.patch("services.fetcher.fetcher.socket.getaddrinfo")
def test_fetch_allowlisted(mock_addr, mock_open):
    mock_addr.return_value = [(None, None, None, None, ("93.184.216.34", 0))]
    mock_open.return_value.__enter__.return_value = DummyResponse(b"ok")
    res = fetch("https://example.com", allowed_hosts={"example.com"})
    assert isinstance(res, FetchResult)
    assert res.content == b"ok"


@mock.patch("services.fetcher.fetcher.socket.getaddrinfo")
def test_fetch_blocks_private(mock_addr):
    mock_addr.return_value = [(None, None, None, None, ("127.0.0.1", 0))]
    with pytest.raises(ValueError):
        fetch("http://localhost", allowed_hosts={"localhost"})


def test_fetch_blocks_unlisted_host():
    with pytest.raises(ValueError):
        fetch("https://example.org", allowed_hosts={"example.com"})
