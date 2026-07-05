import io
import json

import pytest

from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.mcp.resources import list_resources, read_resource
from amo.mcp.server import handle_message, serve_stdio
from amo.mcp.tools import ToolError, call_tool, list_tools


def _repo(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    return tmp_path


def test_resources_list_covers_contract():
    uris = {item["uri"] for item in list_resources()}
    assert {
        "amo://memory/state",
        "amo://memory/tasks",
        "amo://memory/decisions",
        "amo://memory/tests",
        "amo://graph",
        "amo://validation",
        "amo://context/quick",
        "amo://handoff/latest",
        "amo://benchmark/latest",
        "amo://evolution/findings",
    } <= uris


def test_read_resource_returns_canonical_memory(tmp_path):
    repo = _repo(tmp_path)
    content = read_resource(repo, "amo://memory/state")
    assert content["mimeType"] == "text/markdown"
    assert content["text"]


def test_read_unknown_resource_raises(tmp_path):
    with pytest.raises(KeyError):
        read_resource(_repo(tmp_path), "amo://nope")


def test_tools_list_covers_contract():
    names = {tool["name"] for tool in list_tools()}
    assert {
        "amo.scan",
        "amo.graph_build",
        "amo.context",
        "amo.validate",
        "amo.benchmark",
        "amo.optimize_suggest",
        "amo.handoff",
        "amo.postflight",
        "amo.search_graph",
    } == names


def test_postflight_tool_requires_confirm(tmp_path):
    repo = _repo(tmp_path)
    with pytest.raises(ToolError, match="confirm"):
        call_tool(repo, "amo.postflight", {"task": "t", "summary": "s"})


def test_postflight_tool_requires_summary(tmp_path):
    repo = _repo(tmp_path)
    with pytest.raises(ToolError, match="summary"):
        call_tool(repo, "amo.postflight", {"task": "t", "summary": " ", "confirm": True})


def test_confirmed_postflight_applies(tmp_path):
    repo = _repo(tmp_path)
    result = call_tool(repo, "amo.postflight", {"task": "t", "summary": "done", "confirm": True})
    assert result == {"status": "applied"}
    assert "done" in (repo / ".ai" / "state.md").read_text(encoding="utf-8")


def test_search_graph_finds_nodes(tmp_path):
    repo = _repo(tmp_path)
    result = call_tool(repo, "amo.search_graph", {"query": "state"})
    assert result["total"] >= 1


def test_tool_invocations_recorded_in_ledger(tmp_path):
    repo = _repo(tmp_path)
    call_tool(repo, "amo.validate", {})
    ledger = (repo / ".ai" / "evidence" / "ledger.jsonl").read_text(encoding="utf-8")
    assert "mcp_tool_invocation" in ledger


def test_initialize_handshake(tmp_path):
    response = handle_message(_repo(tmp_path), {"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    assert response["result"]["protocolVersion"] == "2024-11-05"
    assert response["result"]["serverInfo"]["name"] == "amo"


def test_notifications_get_no_reply(tmp_path):
    assert handle_message(_repo(tmp_path), {"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_unknown_method_returns_error(tmp_path):
    response = handle_message(_repo(tmp_path), {"jsonrpc": "2.0", "id": 2, "method": "bogus"})
    assert response["error"]["code"] == -32601


def test_stdio_roundtrip(tmp_path):
    repo = _repo(tmp_path)
    stdin = io.StringIO(
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        + "\n"
        + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": "amo://memory/state"}})
        + "\n"
    )
    stdout = io.StringIO()
    serve_stdio(repo, stdin=stdin, stdout=stdout)
    lines = [json.loads(line) for line in stdout.getvalue().splitlines()]
    assert lines[0]["result"]["protocolVersion"]
    assert lines[1]["result"]["contents"][0]["uri"] == "amo://memory/state"
