from __future__ import annotations

import json
from pathlib import Path

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
    output_dir.mkdir(parents=True, exist_ok=True)
    index_lines = ["# AMO Graph", "", "Generated from `.ai/machine/graph.json`.", ""]
    for node in graph["nodes"]:
        safe_name = node["id"].replace(":", "-").replace("/", "-")
        note = output_dir / f"{safe_name}.md"
        backlinks = [edge for edge in graph["edges"] if edge["source"] == node["id"] or edge["target"] == node["id"]]
        body = [
            "---",
            f"amo_id: {node['id']}",
            f"amo_type: {node['type']}",
            "---",
            "",
            f"# {node.get('label', node['id'])}",
            "",
            f"Type: `{node['type']}`",
            f"Path: `{node.get('path', '')}`",
            "",
            "## Relationships",
            "",
        ]
        for edge in backlinks:
            body.append(f"- `{edge['source']}` -[{edge['type']}]-> `{edge['target']}`")
        note.write_text("\n".join(body) + "\n", encoding="utf-8")
        index_lines.append(f"- [[{safe_name}]]")
    (output_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return output_dir
