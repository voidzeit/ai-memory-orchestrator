from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from amo.core.benchmark import run_benchmark
from amo.core.context import build_context_pack
from amo.core.graph import build_graph
from amo.core.handoff import build_handoff
from amo.core.optimize import optimize_suggest
from amo.core.postflight import apply_postflight
from amo.core.scan import scan_repo
from amo.core.validate import validate_repo
from amo.evidence.ledger import record_evidence


class ToolError(ValueError):
    """Tool rejected the invocation (bad arguments or missing confirmation)."""


def _string(args: dict[str, Any], key: str, required: bool = False, default: str = "") -> str:
    value = args.get(key, default)
    if not isinstance(value, str):
        raise ToolError(f"'{key}' must be a string")
    if required and not value.strip():
        raise ToolError(f"'{key}' is required")
    return value


def _tool_scan(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    return dict(scan_repo(repo))


def _tool_graph_build(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    output = build_graph(repo)
    return {"graph": str(output.relative_to(repo).as_posix())}


def _tool_context(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    task = _string(args, "task", required=True)
    profile = _string(args, "profile", default="quick")
    pack = build_context_pack(repo, task=task, profile=profile)
    return {"pack": str(pack.relative_to(repo).as_posix())}


def _tool_validate(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    strict = bool(args.get("strict", True))
    return dict(validate_repo(repo, strict=strict))


def _tool_benchmark(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    task = _string(args, "task", required=True)
    output = run_benchmark(repo, task=task)
    return json.loads(output.read_text(encoding="utf-8"))


def _tool_optimize_suggest(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    output = optimize_suggest(repo)
    return json.loads(output.read_text(encoding="utf-8"))


def _tool_handoff(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    task = _string(args, "task", required=True)
    summary = _string(args, "summary")
    pack = build_handoff(repo, task=task, summary=summary)
    return {"handoff": str(pack.relative_to(repo).as_posix())}


def _tool_postflight(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    if args.get("confirm") is not True:
        raise ToolError("amo.postflight mutates canonical memory; pass confirm=true explicitly")
    task = _string(args, "task", required=True)
    summary = _string(args, "summary", required=True)
    apply_postflight(
        repo,
        task=task,
        summary=summary,
        outcome=_string(args, "outcome", default="completed"),
        validation=_string(args, "validation"),
        changed_files=[item for item in args.get("changed_files", []) if isinstance(item, str)],
        decision=_string(args, "decision"),
    )
    return {"status": "applied"}


def _tool_search_graph(repo: Path, args: dict[str, Any]) -> dict[str, Any]:
    query = _string(args, "query", required=True).lower()
    limit = int(args.get("limit", 20))
    graph_path = repo / ".ai" / "machine" / "graph.json"
    if not graph_path.exists():
        raise ToolError("Graph not built yet; call amo.graph_build first")
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    matches = [
        {key: node.get(key) for key in ("id", "type", "label", "path", "level", "authority")}
        for node in graph.get("nodes", [])
        if query in str(node.get("id", "")).lower() or query in str(node.get("label", "")).lower()
    ]
    return {"query": query, "matches": matches[:limit], "total": len(matches)}


_HANDLERS: dict[str, Callable[[Path, dict[str, Any]], dict[str, Any]]] = {
    "amo.scan": _tool_scan,
    "amo.graph_build": _tool_graph_build,
    "amo.context": _tool_context,
    "amo.validate": _tool_validate,
    "amo.benchmark": _tool_benchmark,
    "amo.optimize_suggest": _tool_optimize_suggest,
    "amo.handoff": _tool_handoff,
    "amo.postflight": _tool_postflight,
    "amo.search_graph": _tool_search_graph,
}

TOOLS: list[dict[str, Any]] = [
    {
        "name": "amo.scan",
        "description": "Index repository files and context units (writes derived indexes only).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "amo.graph_build",
        "description": "Build the project knowledge graph (writes derived indexes only).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "amo.context",
        "description": "Compile a token-bounded context pack for a task.",
        "inputSchema": {
            "type": "object",
            "properties": {"task": {"type": "string"}, "profile": {"type": "string"}},
            "required": ["task"],
        },
    },
    {
        "name": "amo.validate",
        "description": "Validate memory, indexes, and graph contract.",
        "inputSchema": {"type": "object", "properties": {"strict": {"type": "boolean"}}},
    },
    {
        "name": "amo.benchmark",
        "description": "Run the deterministic context benchmark on this repository.",
        "inputSchema": {
            "type": "object",
            "properties": {"task": {"type": "string"}},
            "required": ["task"],
        },
    },
    {
        "name": "amo.optimize_suggest",
        "description": "Collect deterministic findings; propose-only, writes evolution artifacts.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "amo.handoff",
        "description": "Compile a session-restart handoff pack.",
        "inputSchema": {
            "type": "object",
            "properties": {"task": {"type": "string"}, "summary": {"type": "string"}},
            "required": ["task"],
        },
    },
    {
        "name": "amo.postflight",
        "description": "Mutate canonical memory after a session. Requires confirm=true and a summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "summary": {"type": "string"},
                "outcome": {"type": "string"},
                "validation": {"type": "string"},
                "changed_files": {"type": "array", "items": {"type": "string"}},
                "decision": {"type": "string"},
                "confirm": {"type": "boolean"},
            },
            "required": ["task", "summary", "confirm"],
        },
    },
    {
        "name": "amo.search_graph",
        "description": "Search graph nodes by id or label substring.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
            "required": ["query"],
        },
    },
]


def list_tools() -> list[dict[str, Any]]:
    return TOOLS


def call_tool(repo: Path, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handler = _HANDLERS.get(name)
    if handler is None:
        raise ToolError(f"Unknown tool: {name}")
    repo = repo.resolve()
    result = handler(repo, arguments or {})
    record_evidence(
        repo,
        kind="mcp_tool_invocation",
        source=f"mcp:{name}",
        result="ok",
        authority=0.6,
        limitations=("invoked by an MCP client; authority order still applies",),
    )
    return result
