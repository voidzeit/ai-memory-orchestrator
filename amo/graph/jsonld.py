from __future__ import annotations

import json
from pathlib import Path

from amo.graph.schema import ProjectGraph


def export_jsonld(graph: ProjectGraph, output: Path) -> Path:
    document = {
        "@context": {"amo": "https://github.com/voidzeit/ai-memory-orchestrator/schema#", "type": "@type", "label": "amo:label", "source": {"@id": "amo:source", "@type": "@id"}, "target": {"@id": "amo:target", "@type": "@id"}},
        "schema_version": graph["schema_version"],
        "@graph": [{"@id": node["id"], **{key: value for key, value in node.items() if key != "id"}} for node in graph["nodes"]]
        + [{"@id": f"edge:{index}", **edge} for index, edge in enumerate(graph["edges"])],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output
