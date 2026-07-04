from __future__ import annotations

import ast
from pathlib import Path

from amo.graph.schema import GraphEdge, GraphNode


def extract_python_structure(repo: Path, relative_path: str) -> tuple[list[GraphNode], list[GraphEdge]]:
    path = repo / relative_path
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative_path)
    except (OSError, SyntaxError, UnicodeError):
        return [], []

    module_name = _module_name(relative_path)
    module_id = f"module:{module_name}"
    nodes: list[GraphNode] = [
        {"id": module_id, "type": "module", "label": module_name, "path": relative_path, "source": "ast", "authority": 0.9, "level": "L2"}
    ]
    edges: list[GraphEdge] = [{"source": f"file:{relative_path}", "target": module_id, "type": "contains"}]

    for item in tree.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbol_id = f"symbol:{module_name}:{item.name}"
            nodes.append({"id": symbol_id, "type": "symbol", "label": item.name, "path": relative_path, "source": "ast", "authority": 0.9, "level": "L2", "metadata": {"kind": "class" if isinstance(item, ast.ClassDef) else "function", "line": item.lineno}})
            edges.append({"source": module_id, "target": symbol_id, "type": "contains"})
        if isinstance(item, (ast.Import, ast.ImportFrom)):
            names = [alias.name for alias in item.names] if isinstance(item, ast.Import) else ([item.module] if item.module else [])
            for name in names:
                dependency_id = f"module:{name}"
                nodes.append({"id": dependency_id, "type": "module", "label": name, "source": "ast-import", "authority": 0.5, "level": "L2"})
                edges.append({"source": module_id, "target": dependency_id, "type": "depends_on"})
                edges.append({"source": f"file:{relative_path}", "target": dependency_id, "type": "references"})
    return nodes, edges


def _module_name(relative_path: str) -> str:
    path = Path(relative_path)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts) or path.stem
