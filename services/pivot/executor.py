"""Simple pivot graph executor.

The executor traverses a YAML-defined graph of lawful OSINT pivots and
records the path taken for each discovered entity. It purposely keeps the
implementation lightweight and deterministic for testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple, Any

# --- YAML loading ---------------------------------------------------------

def _convert(value: str) -> Any:
    """Best-effort conversion of YAML scalar *value* to Python types."""
    if value.startswith(('"', "'")) and value.endswith(('"', "'")):
        value = value[1:-1]
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value

def load_graph(path: Path | None = None) -> List[Dict[str, Any]]:
    """Load pivot edges from *path*.

    This parser understands a small YAML subset sufficient for the graph
    structure used in tests. Each edge is a mapping containing the keys
    ``from_type``, ``to_type``, ``pattern``, ``tos_notes``, ``risk_score``
    and ``enabled``.
    """
    path = path or Path(__file__).with_name("pivot_graph.yaml")
    edges: List[Dict[str, Any]] = []
    current: Dict[str, Any] | None = None
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- "):
                if current:
                    edges.append(current)
                current = {}
                line = line[2:]
                if line:
                    key, val = line.split(":", 1)
                    current[key.strip()] = _convert(val.strip())
            elif current and ":" in line:
                key, val = line.split(":", 1)
                current[key.strip()] = _convert(val.strip())
        if current:
            edges.append(current)
    return edges

# --- Pivot execution ------------------------------------------------------

# Deterministic stub transforms for tests
Transform = Callable[[str], Iterable[str]]

TRANSFORMS: Dict[str, Transform] = {
    "ct_subdomains": lambda value: [f"sub.{value}"],
    "dns_asn": lambda value: ["AS64500"],
    "hosted_domains": lambda value: ["example.net"],
}


def execute(start_type: str, value: str, *, max_depth: int = 3,
            graph: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    """Execute pivots starting from ``(start_type, value)``.

    Parameters
    ----------
    start_type:
        Entity type of the starting value.
    value:
        Starting value to pivot from.
    max_depth:
        Maximum pivot depth.
    graph:
        Optional pre-loaded edge list.

    Returns
    -------
    list of dict
        Each result contains ``type``, ``value`` and ``path`` describing the
        edges traversed to reach it.
    """
    edges = graph or load_graph()
    index: Dict[str, List[Dict[str, Any]]] = {}
    for edge in edges:
        if edge.get("enabled"):
            index.setdefault(edge["from_type"], []).append(edge)

    results: List[Dict[str, Any]] = []
    queue: List[Tuple[str, str, List[Dict[str, Any]]]] = [(start_type, value, [])]
    while queue:
        etype, val, path = queue.pop(0)
        for edge in index.get(etype, []):
            func = TRANSFORMS.get(edge["pattern"])
            if not func:
                continue
            for out in func(val):
                new_path = path + [edge]
                result = {"type": edge["to_type"], "value": out, "path": new_path}
                results.append(result)
                if len(new_path) < max_depth:
                    queue.append((edge["to_type"], out, new_path))
    return results
