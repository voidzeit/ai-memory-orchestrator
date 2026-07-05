from __future__ import annotations

import json
from collections import deque
from pathlib import Path

DEFAULT_SEED_TOP_K = 10
DEFAULT_MAX_HOPS = 2
DEFAULT_DISTANCE_DECAY = 0.75


def task_terms(task: str) -> set[str]:
    return {term.lower() for term in task.replace("-", " ").split() if len(term) > 2}


def lexical_seed_paths(units: list[dict[str, object]], task: str, top_k: int) -> list[str]:
    """Rank unit paths by lexical task relevance and return the top seeds."""
    terms = task_terms(task)
    scored = []
    for unit in units:
        haystack = " ".join(
            [str(unit.get("title", "")), str(unit.get("summary", "")), " ".join(unit.get("tags", []))]
        ).lower()
        relevance = sum(1 for term in terms if term in haystack)
        if relevance > 0:
            scored.append((relevance, str(unit.get("expand") or unit.get("title") or "")))
    scored.sort(key=lambda item: (-item[0], item[1]))
    seeds = []
    for _, path in scored:
        if path and path not in seeds:
            seeds.append(path)
        if len(seeds) >= top_k:
            break
    return seeds


def load_graph(repo: Path) -> dict[str, object] | None:
    path = repo / ".ai" / "machine" / "graph.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def graph_proximity(
    graph: dict[str, object],
    seed_paths: list[str],
    max_hops: int = DEFAULT_MAX_HOPS,
    distance_decay: float = DEFAULT_DISTANCE_DECAY,
) -> dict[str, float]:
    """Expand seed file nodes through the graph; return path -> decayed proximity.

    Seeds score 1.0; each hop multiplies by distance_decay. Only file nodes
    contribute paths, but traversal may pass through any node type (directories,
    symbols, tests) so structural relationships still connect files.
    """
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    path_by_node = {
        str(node.get("id")): str(node.get("path"))
        for node in nodes
        if node.get("type") == "file" and node.get("path")
    }
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        source, target = str(edge.get("source")), str(edge.get("target"))
        adjacency.setdefault(source, set()).add(target)
        adjacency.setdefault(target, set()).add(source)

    seed_nodes = [f"file:{path}" for path in seed_paths if f"file:{path}" in path_by_node]
    proximity: dict[str, float] = {}
    visited: dict[str, int] = {}
    queue: deque[tuple[str, int]] = deque((node, 0) for node in seed_nodes)
    for node in seed_nodes:
        visited[node] = 0
    while queue:
        node, hops = queue.popleft()
        if node in path_by_node:
            score = distance_decay**hops
            path = path_by_node[node]
            proximity[path] = max(proximity.get(path, 0.0), score)
        if hops >= max_hops:
            continue
        for neighbor in adjacency.get(node, ()):
            if neighbor not in visited or visited[neighbor] > hops + 1:
                visited[neighbor] = hops + 1
                queue.append((neighbor, hops + 1))
    return proximity


def compute_neighborhood(
    repo: Path,
    units: list[dict[str, object]],
    task: str,
    seed_top_k: int = DEFAULT_SEED_TOP_K,
    max_hops: int = DEFAULT_MAX_HOPS,
    distance_decay: float = DEFAULT_DISTANCE_DECAY,
) -> tuple[dict[str, float], list[str]]:
    """Return (path -> proximity, seed paths). Empty when no graph exists."""
    graph = load_graph(repo)
    if graph is None:
        return {}, []
    seeds = lexical_seed_paths(units, task, seed_top_k)
    if not seeds:
        return {}, []
    return graph_proximity(graph, seeds, max_hops=max_hops, distance_decay=distance_decay), seeds
