from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from amo.graph.schema import ProjectGraph


def export_gexf(graph: ProjectGraph, output: Path) -> Path:
    root = ET.Element("gexf", xmlns="http://gexf.net/1.3", version="1.3")
    body = ET.SubElement(root, "graph", mode="static", defaultedgetype="directed")
    nodes = ET.SubElement(body, "nodes")
    for node in graph["nodes"]:
        ET.SubElement(nodes, "node", id=node["id"], label=node.get("label", node["id"]), type=node["type"])
    edges = ET.SubElement(body, "edges")
    for index, edge in enumerate(graph["edges"]):
        ET.SubElement(edges, "edge", id=str(index), source=edge["source"], target=edge["target"], label=edge["type"], type="directed")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    return output
