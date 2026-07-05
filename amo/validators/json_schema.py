from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


def check_graph_schema(repo: Path) -> list[str]:
    """Validate the generated graph against the checked-in JSON Schema artifact."""
    graph_path = repo / ".ai" / "machine" / "graph.json"
    if not graph_path.exists():
        return []
    schema_path = _schema_path(repo)
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        return [f"Graph schema validation could not run: {exc}."]

    return [
        f"Graph schema violation at {_error_path(error.absolute_path)}: {error.message}."
        for error in sorted(validator.iter_errors(graph), key=lambda item: list(item.absolute_path))
    ]


def _schema_path(repo: Path) -> Path:
    project_schema = repo / "schemas" / "amo-graph.schema.json"
    if project_schema.is_file():
        return project_schema
    return Path(__file__).resolve().parents[2] / "schemas" / "amo-graph.schema.json"


def _error_path(parts: Any) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path
