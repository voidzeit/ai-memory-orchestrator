from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, TextIO

from amo.mcp.resources import list_resources, read_resource
from amo.mcp.tools import ToolError, call_tool, list_tools

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "amo", "version": "0.1.0a1"}

PARSE_ERROR = -32700
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def handle_message(repo: Path, message: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one JSON-RPC message. Returns None for notifications."""
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None  # notifications (e.g. notifications/initialized) need no reply
    params = message.get("params") or {}
    try:
        result = _dispatch(repo, str(method), params)
    except ToolError as exc:
        return _error(request_id, INVALID_PARAMS, str(exc))
    except (KeyError, FileNotFoundError) as exc:
        return _error(request_id, INVALID_PARAMS, str(exc))
    except Exception as exc:  # noqa: BLE001 - protocol boundary must not crash
        return _error(request_id, INTERNAL_ERROR, str(exc))
    if result is None:
        return _error(request_id, METHOD_NOT_FOUND, f"Unknown method: {method}")
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _dispatch(repo: Path, method: str, params: dict[str, Any]) -> dict[str, Any] | None:
    if method == "initialize":
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"resources": {}, "tools": {}},
            "serverInfo": SERVER_INFO,
        }
    if method == "ping":
        return {}
    if method == "resources/list":
        return {"resources": list_resources()}
    if method == "resources/read":
        uri = str(params.get("uri", ""))
        return {"contents": [read_resource(repo, uri)]}
    if method == "tools/list":
        return {"tools": list_tools()}
    if method == "tools/call":
        name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        result = call_tool(repo, name, arguments)
        return {
            "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
            "isError": False,
        }
    return None


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def serve_stdio(repo: Path, stdin: TextIO | None = None, stdout: TextIO | None = None) -> None:
    """Serve MCP over newline-delimited JSON-RPC on stdio."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            response: dict[str, Any] | None = _error(None, PARSE_ERROR, f"Invalid JSON: {exc}")
        else:
            response = handle_message(repo, message)
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            stdout.flush()
