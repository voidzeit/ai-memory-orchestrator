import json
from pathlib import Path

from amo.io import write_json, write_text
from amo.paths import ai_path


def build_graph(repo: Path) -> Path:
    repo = repo.resolve()
    files_path = ai_path(repo, "machine", "files.json")
    files = []
    if files_path.exists():
        files = json.loads(files_path.read_text(encoding="utf-8")).get("files", [])
    nodes = [{"id": f"file:{item['path']}", "type": "file", "label": item["path"]} for item in files]
    nodes.extend([
        {"id": "memory:state", "type": "memory", "label": ".ai/state.md"},
        {"id": "memory:decisions", "type": "memory", "label": ".ai/decisions.md"},
        {"id": "memory:tasks", "type": "memory", "label": ".ai/tasks.md"},
    ])
    edges = [{"from": "memory:state", "to": node["id"], "type": "documents"} for node in nodes if node["type"] == "file"]
    graph = {"nodes": nodes, "edges": edges}
    output = ai_path(repo, "machine", "graph.json")
    write_json(output, graph)
    graph_md = "# Graph\n\n" + "\n".join(f"- {node['type']}: {node['label']}" for node in nodes) + "\n"
    write_text(ai_path(repo, "graph.md"), graph_md)
    return output
