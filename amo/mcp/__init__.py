"""MCP-compatible server exposing AMO memory as resources and tools."""

from amo.mcp.resources import list_resources, read_resource
from amo.mcp.server import handle_message, serve_stdio
from amo.mcp.tools import call_tool, list_tools

__all__ = [
    "call_tool",
    "handle_message",
    "list_resources",
    "list_tools",
    "read_resource",
    "serve_stdio",
]
