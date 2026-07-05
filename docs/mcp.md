# MCP Adapter

AMO includes a dependency-free MCP stdio server:

```bash
amo mcp serve
```

It exposes canonical memory, graph, validation, and context-pack resources plus tools for scan, graph build, context, validation, benchmark, optimizer suggestions, handoff, postflight, and graph search. Resources are read-only. `amo.postflight` is the canonical-memory write tool and rejects calls unless the host sends `confirm=true` with a non-empty summary.

The server does not change AMO's authority model: `.ai/` canonical files remain the source of truth; machine indexes, packs, evolution output, and runtime state remain lower-authority derived data.

See [MCP Server](mcp-server.md) for protocol examples, resource URIs, tool names, and client configuration.
