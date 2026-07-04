from __future__ import annotations

from typing import Literal, TypedDict

NodeType = Literal[
    "repository",
    "file",
    "directory",
    "module",
    "symbol",
    "decision",
    "task",
    "test",
    "workflow",
    "artifact",
    "context_pack",
    "adapter",
    "validator",
    "risk",
    "memory",
]

EdgeType = Literal[
    "contains",
    "documents",
    "references",
    "depends_on",
    "generates",
    "validates",
    "tested_by",
    "derived_from",
    "exports_to",
    "belongs_to",
    "supersedes",
    "conflicts_with",
]


class GraphNode(TypedDict, total=False):
    id: str
    type: NodeType
    label: str
    path: str
    source: str
    authority: float
    level: str
    metadata: dict[str, object]


class GraphEdge(TypedDict, total=False):
    source: str
    target: str
    type: EdgeType
    label: str
    metadata: dict[str, object]


class ProjectGraph(TypedDict):
    schema_version: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]


def normalize_for_cypher(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
