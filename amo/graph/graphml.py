from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from amo.graph.schema import ProjectGraph


def export_graphml(graph: ProjectGraph, output: Path) -> Path:
    root = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    for key in ("type", "label", "level", "path"):
        ET.SubElement(root, "key", id=key, **{"for": "node", "attr.name": key, "attr.type": "string"})
    ET.SubElement(root, "key", id="edge_type", **{"for": "edge", "attr.name": "type", "attr.type": "string"})
    body = ET.SubElement(root, "graph", id="amo", edgedefault="directed")
    for node in graph["nodes"]:
        element = ET.SubElement(body, "node", id=node["id"])
        for key in ("type", "label", "level", "path"):
            if key in node:
                ET.SubElement(element, "data", key=key).text = str(node[key])
    for index, edge in enumerate(graph["edges"]):
        element = ET.SubElement(body, "edge", id=f"e{index}", source=edge["source"], target=edge["target"])
        ET.SubElement(element, "data", key="edge_type").text = edge["type"]
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    return output
