"""Minimal graph analytics without external dependencies."""
from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Set, Tuple

Graph = Dict[str, Set[str]]

def build_graph(edges: Iterable[Tuple[str, str]]) -> Graph:
    graph: Graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
    return graph

def centrality(graph: Graph) -> Dict[str, float]:
    n = len(graph)
    return {node: (len(neigh) / (n - 1) if n > 1 else 0.0) for node, neigh in graph.items()}

def components(graph: Graph) -> List[Set[str]]:
    seen: Set[str] = set()
    comps: List[Set[str]] = []
    for node in graph:
        if node in seen:
            continue
        queue = [node]
        comp: Set[str] = set()
        while queue:
            v = queue.pop()
            if v in seen:
                continue
            seen.add(v)
            comp.add(v)
            queue.extend(graph[v] - seen)
        comps.append(comp)
    return comps

def shortest_path(graph: Graph, start: str, end: str) -> List[str]:
    if start == end:
        return [start]
    q = deque([(start, [start])])
    seen = {start}
    while q:
        node, path = q.popleft()
        for neigh in graph[node]:
            if neigh == end:
                return path + [neigh]
            if neigh not in seen:
                seen.add(neigh)
                q.append((neigh, path + [neigh]))
    raise ValueError("no path")
