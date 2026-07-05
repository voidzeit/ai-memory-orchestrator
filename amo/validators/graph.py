from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def check_graph_contract(repo: Path) -> list[str]:
    path = repo / ".ai" / "machine" / "graph.json"
    if not path.exists():
        return []
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid graph JSON: {exc}."]
    if not isinstance(graph, dict):
        return ["Invalid graph: root must be an object."]

    errors: list[str] = []
    for field in ("schema_version", "nodes", "edges"):
        if field not in graph:
            errors.append(f"Invalid graph: missing `{field}`.")
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list):
        errors.append("Invalid graph: `nodes` must be an array.")
        nodes = []
    if not isinstance(edges, list):
        errors.append("Invalid graph: `edges` must be an array.")
        edges = []

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Invalid graph node {index}: must be an object.")
            continue
        _require_fields(errors, "node", index, node, ("id", "type", "label"))
        node_id = node.get("id")
        if isinstance(node_id, str):
            if node_id in node_ids:
                errors.append(f"Invalid graph: duplicate node id `{node_id}`.")
            node_ids.add(node_id)

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"Invalid graph edge {index}: must be an object.")
            continue
        _require_fields(errors, "edge", index, edge, ("source", "target", "type"))
        for endpoint in ("source", "target"):
            value = edge.get(endpoint)
            if isinstance(value, str) and value not in node_ids:
                errors.append(f"Invalid graph edge {index}: `{endpoint}` references missing node `{value}`.")
    return errors


def _require_fields(
    errors: list[str], kind: str, index: int, value: dict[str, Any], fields: tuple[str, ...]
) -> None:
    for field in fields:
        if field not in value or not isinstance(value[field], str) or not value[field]:
            errors.append(f"Invalid graph {kind} {index}: missing or invalid `{field}`.")
