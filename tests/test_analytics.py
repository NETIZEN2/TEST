"""Benchmarks for analytics components."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.ner.ner import extract_entities
from services.analytics.events import extract_events
from services.analytics.confidence import compute_confidence
from services.analytics.graph import build_graph, centrality, components, shortest_path


def test_ner_precision_recall():
    text = "Barack Obama visited Paris and met Microsoft executives."
    gold = {
        ("Barack Obama", "PERSON", "Q76"),
        ("Paris", "GPE", "Q90"),
        ("Microsoft", "ORG", "Q2283"),
    }
    preds = {
        (e["text"], e["label"], e["wikidata_id"])
        for e in extract_entities(text)
    }
    tp = len(preds & gold)
    precision = tp / len(preds) if preds else 0
    recall = tp / len(gold)
    assert precision >= 0.8
    assert recall >= 0.8


def test_event_extraction_precision_recall():
    text = "On 1 Jan 2020, Alice founded Acme in Sydney."
    source = "http://example.com"
    events = extract_events(text, source)
    assert events, "no events"
    event = events[0]
    gold = {"who": "Alice", "what": "founded", "when": "2020-01-01", "where": "Sydney", "source": source}
    pred_items = {(k, event[k]) for k in gold}
    gold_items = set(gold.items())
    tp = len(pred_items & gold_items)
    precision = tp / len(pred_items)
    recall = tp / len(gold_items)
    assert precision >= 0.8
    assert recall >= 0.8


def test_confidence_model():
    score = compute_confidence(0.8, 2, 10, 0.9)
    expected = round(0.4 * 0.8 + 0.3 * (2 / 5) + 0.2 * (1 - 10 / 365) + 0.1 * 0.9, 3)
    assert score == expected


def test_graph_analytics():
    edges = [
        ("alice", "alice@example.com"),
        ("alice@example.com", "example.com"),
        ("example.com", "bob@example.com"),
        ("bob@example.com", "bob"),
    ]
    g = build_graph(edges)
    cent = centrality(g)
    assert cent["example.com"] > cent["alice"]
    comps = components(g)
    assert len(comps) == 1
    path = shortest_path(g, "alice", "bob")
    assert path == ["alice", "alice@example.com", "example.com", "bob@example.com", "bob"]
