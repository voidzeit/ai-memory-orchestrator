# MCP Server

`amo mcp serve` exposes AMO memory to MCP-compatible clients (Claude Code, Cursor, and
others) over newline-delimited JSON-RPC on stdio. It is dependency-free by design: the
protocol surface AMO needs (initialize, resources, tools) is small enough to implement
directly, and heavier SDKs can be adopted later without changing the contract.

## Client configuration

```json
{
  "mcpServers": {
    "amo": {
      "command": "amo",
      "args": ["mcp", "serve", "--repo", "/path/to/repo"]
    }
  }
}
```

## Resources (read-only)

| URI | Backing file |
| --- | --- |
| `amo://memory/state` | `.ai/state.md` |
| `amo://memory/tasks` | `.ai/tasks.md` |
| `amo://memory/decisions` | `.ai/decisions.md` |
| `amo://memory/tests` | `.ai/tests.md` |
| `amo://graph` | `.ai/machine/graph.json` |
| `amo://validation` | `.ai/machine/validation.json` |
| `amo://context/quick` | `.ai/packs/quick.md` |
| `amo://handoff/latest` | `.ai/packs/handoff.md` |
| `amo://benchmark/latest` | `.ai/machine/benchmark.json` |
| `amo://evolution/findings` | `.ai/evolution/findings.md` |

Reading a resource never generates it; ungenerated artifacts return a clear error.

## Tools

`amo.scan`, `amo.graph_build`, `amo.context`, `amo.validate`, `amo.benchmark`,
`amo.optimize_suggest`, `amo.handoff` write only derived or compiled artifacts.

`amo.postflight` is the single canonical-memory mutator and demands `confirm: true`
plus a non-empty `summary`; it goes through the same lock/backup/run-history path as
the CLI. `amo.search_graph` searches node ids and labels.

`amo optimize params apply-safe` is deliberately **not** exposed over MCP: parameter
promotion stays behind the CLI policy gate.

## Security model

- Resources are read-only; the server never bypasses AMO's authority order.
- Every tool call appends an `mcp_tool_invocation` entry to the evidence ledger.
- The server binds to stdio only — no network listener.
