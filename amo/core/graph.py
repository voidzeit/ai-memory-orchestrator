import json
from pathlib import Path

from amo.graph.exporters import export_graph_cypher, export_graph_json, export_obsidian_graph_notes
from amo.graph.code_structure import extract_python_structure
from amo.graph.gexf import export_gexf
from amo.graph.graphml import export_graphml
from amo.graph.jsonld import export_jsonld
from amo.graph.schema import ProjectGraph
from amo.io import write_json, write_text
from amo.paths import ai_path

SCHEMA_VERSION = "0.2"


def build_graph(repo: Path) -> Path:
    repo = repo.resolve()
    graph = build_project_graph(repo)
    output = ai_path(repo, "machine", "graph.json")
    write_json(output, graph)
    write_text(ai_path(repo, "graph.md"), render_graph_markdown(graph))
    return output


def build_project_graph(repo: Path) -> ProjectGraph:
    files_path = ai_path(repo, "machine", "files.json")
    files = []
    if files_path.exists():
        files = json.loads(files_path.read_text(encoding="utf-8")).get("files", [])

    nodes = [
        {
            "id": f"repo:{repo.name}",
            "type": "repository",
            "label": repo.name,
            "path": ".",
            "source": "git",
            "authority": 1.0,
            "level": "L0",
        }
    ]
    edges = []

    memory_files = [
        ("memory:manifest", ".ai/manifest.yaml"),
        ("memory:state", ".ai/state.md"),
        ("memory:decisions", ".ai/decisions.md"),
        ("memory:tasks", ".ai/tasks.md"),
        ("memory:tests", ".ai/tests.md"),
        ("memory:graph", ".ai/graph.md"),
    ]
    for node_id, path in memory_files:
        nodes.append(
            {
                "id": node_id,
                "type": "memory",
                "label": path,
                "path": path,
                "source": ".ai",
                "authority": 0.95,
                "level": "L1",
            }
        )
        edges.append({"source": f"repo:{repo.name}", "target": node_id, "type": "contains"})

    seen_dirs = set()
    for item in files:
        file_path = str(item["path"])
        file_node = {
            "id": f"file:{file_path}",
            "type": "file",
            "label": file_path,
            "path": file_path,
            "source": "scan",
            "authority": 0.8,
            "level": "L0",
            "metadata": {"lines": item.get("lines"), "size": item.get("size"), "suffix": item.get("suffix")},
        }
        nodes.append(file_node)
        edges.append({"source": f"repo:{repo.name}", "target": file_node["id"], "type": "contains"})

        parts = Path(file_path).parts[:-1]
        current = ""
        parent_id = f"repo:{repo.name}"
        for part in parts:
            current = f"{current}/{part}" if current else part
            dir_id = f"dir:{current}"
            if dir_id not in seen_dirs:
                seen_dirs.add(dir_id)
                nodes.append(
                    {
                        "id": dir_id,
                        "type": "directory",
                        "label": current,
                        "path": current,
                        "source": "scan",
                        "authority": 0.8,
                        "level": "L0",
                    }
                )
                edges.append({"source": parent_id, "target": dir_id, "type": "contains"})
            parent_id = dir_id
        if parts:
            edges.append({"source": parent_id, "target": file_node["id"], "type": "contains"})

        if file_path.startswith("tests/") or "/test_" in file_path or file_path.endswith("_test.py"):
            test_id = f"test:{file_path}"
            nodes.append(
                {
                    "id": test_id,
                    "type": "test",
                    "label": file_path,
                    "path": file_path,
                    "source": "scan",
                    "authority": 0.85,
                    "level": "L3",
                }
            )
            edges.append({"source": test_id, "target": file_node["id"], "type": "documents"})
            edges.append({"source": file_node["id"], "target": test_id, "type": "tested_by"})

        if file_path.startswith(".ai/packs/"):
            pack_id = f"pack:{file_path}"
            nodes.append(
                {
                    "id": pack_id,
                    "type": "context_pack",
                    "label": file_path,
                    "path": file_path,
                    "source": ".ai/packs",
                    "authority": 0.75,
                    "level": "L1",
                }
            )
            edges.append({"source": pack_id, "target": file_node["id"], "type": "derived_from"})

    for item in files:
        file_path = str(item["path"])
        if file_path.endswith(".py"):
            code_nodes, code_edges = extract_python_structure(repo, file_path)
            nodes.extend(code_nodes)
            edges.extend(code_edges)

    unique_nodes = {node["id"]: node for node in nodes}
    nodes = list(unique_nodes.values())

    for node in nodes:
        if node["type"] == "file":
            edges.append({"source": "memory:state", "target": node["id"], "type": "documents"})

    return {"schema_version": SCHEMA_VERSION, "nodes": nodes, "edges": edges}


def export_graph(repo: Path, export_format: str, output: Path | None = None) -> Path:
    repo = repo.resolve()
    graph_path = ai_path(repo, "machine", "graph.json")
    if not graph_path.exists():
        graph_path = build_graph(repo)
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    if export_format == "json":
        return export_graph_json(graph, output or ai_path(repo, "machine", "graph.export.json"))
    if export_format == "neo4j":
        return export_graph_cypher(graph, output or ai_path(repo, "machine", "graph.cypher"))
    if export_format == "jsonld":
        return export_jsonld(graph, output or ai_path(repo, "machine", "graph.jsonld"))
    if export_format == "graphml":
        return export_graphml(graph, output or ai_path(repo, "machine", "graph.graphml"))
    if export_format == "gexf":
        return export_gexf(graph, output or ai_path(repo, "machine", "graph.gexf"))
    if export_format == "obsidian":
        return export_obsidian_graph_notes(graph, output or repo / ".obsidian" / "project-memory" / "Graph")
    raise ValueError(f"Unsupported graph export format: {export_format}")


def render_graph_markdown(graph: ProjectGraph) -> str:
    lines = ["# Graph", "", f"Schema version: `{graph['schema_version']}`", "", "## Nodes", ""]
    for node in graph["nodes"]:
        lines.append(f"- `{node['type']}` — {node['label']} (`{node['id']}`)")
    lines.extend(["", "## Edges", ""])
    for edge in graph["edges"][:250]:
        lines.append(f"- `{edge['source']}` -[{edge['type']}]-> `{edge['target']}`")
    if len(graph["edges"]) > 250:
        lines.append(f"- ... {len(graph['edges']) - 250} more edges")
    return "\n".join(lines) + "\n"
