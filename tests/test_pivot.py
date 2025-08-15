"""Tests for pivot graph and executor."""

from pathlib import Path

from services.pivot import execute, load_graph


def test_graph_has_domain_edge():
    edges = load_graph()
    assert any(e["from_type"] == "domain" and e["to_type"] == "subdomain" for e in edges)


def test_executor_records_path():
    results = execute("domain", "example.com", max_depth=3)
    final = next(r for r in results if r["type"] == "domain" and r["value"] == "example.net")
    patterns = [step["pattern"] for step in final["path"]]
    assert patterns == ["ct_subdomains", "dns_asn", "hosted_domains"]
