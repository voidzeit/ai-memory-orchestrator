from __future__ import annotations

import json
from pathlib import Path

from amo.graph.obsidian_rich import export_rich_obsidian_graph
from amo.graph.schema import ProjectGraph, normalize_for_cypher
from amo.io import write_text


def export_graph_json(graph: ProjectGraph, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


def export_graph_cypher(graph: ProjectGraph, output: Path) -> Path:
    lines = [
        "// AMO Neo4j import",
        "// Generated from .ai/machine/graph.json",
        "CREATE CONSTRAINT amo_node_id IF NOT EXISTS FOR (n:AMONode) REQUIRE n.id IS UNIQUE;",
        "",
    ]
    for node in graph["nodes"]:
        node_id = normalize_for_cypher(node["id"])
        label = normalize_for_cypher(node.get("label", node["id"]))
        node_type = normalize_for_cypher(node["type"])
        path = normalize_for_cypher(node.get("path", ""))
        lines.append(
            "MERGE (n:AMONode {id: '" + node_id + "'}) "
            "SET n.label = '" + label + "', n.type = '" + node_type + "', n.path = '" + path + "';"
        )
    lines.append("")
    for edge in graph["edges"]:
        source = normalize_for_cypher(edge["source"])
        target = normalize_for_cypher(edge["target"])
        edge_type = normalize_for_cypher(edge["type"])
        lines.append(
            "MATCH (a:AMONode {id: '" + source + "'}), (b:AMONode {id: '" + target + "'}) "
            "MERGE (a)-[r:AMO_EDGE {type: '" + edge_type + "'}]->(b);"
        )
    write_text(output, "\n".join(lines) + "\n")
    return output


def export_obsidian_graph_notes(graph: ProjectGraph, output_dir: Path) -> Path:
    return export_rich_obsidian_graph(graph, output_dir)
