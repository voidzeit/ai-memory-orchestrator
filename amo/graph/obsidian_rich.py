from __future__ import annotations

import hashlib
import re
from pathlib import Path

from amo.graph.schema import ProjectGraph


def safe_note_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "node"
    short_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]
    return f"{slug[:80]}--{short_hash}"


def export_rich_obsidian_graph(graph: ProjectGraph, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    nodes_dir = output_dir / "Nodes"
    views_dir = output_dir / "Views"
    nodes_dir.mkdir(parents=True, exist_ok=True)
    views_dir.mkdir(parents=True, exist_ok=True)

    names = {node["id"]: safe_note_name(node["id"]) for node in graph["nodes"]}
    index = ["# AMO Graph", "", "Generated from `.ai/machine/graph.json`.", "", "## Nodes", ""]

    for node in graph["nodes"]:
        note_name = names[node["id"]]
        outbound = [edge for edge in graph["edges"] if edge["source"] == node["id"]]
        inbound = [edge for edge in graph["edges"] if edge["target"] == node["id"]]
        body = [
            "---",
            f"amo_id: \"{node['id']}\"",
            f"amo_type: {node['type']}",
            f"source_path: \"{node.get('path', '')}\"",
            "tags:",
            "  - amo/node",
            f"  - amo/node/{node['type']}",
            "aliases:",
            f"  - \"{node.get('label', node['id'])}\"",
            "---",
            "",
            f"# {node.get('label', node['id'])}",
            "",
            "## Outbound",
            "",
        ]
        body.extend([f"- `{edge['type']}` -> [[Nodes/{names[edge['target']]}]]" for edge in outbound] or ["- None"])
        body.extend(["", "## Inbound", ""])
        body.extend([f"- [[Nodes/{names[edge['source']]}]] -> `{edge['type']}`" for edge in inbound] or ["- None"])
        (nodes_dir / f"{note_name}.md").write_text("\n".join(body) + "\n", encoding="utf-8")
        index.append(f"- [[Nodes/{note_name}]]")

    (output_dir / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    (views_dir / "Groups.md").write_text(
        "# Groups\n\n- amo/node/file\n- amo/node/memory\n- amo/node/test\n- amo/node/directory\n- amo/node/context_pack\n",
        encoding="utf-8",
    )
    return output_dir
