# Adapters

Adapters export AMO memory into external tool formats.

Supported agent targets and generated files:

| Target | Generated file |
|---|---|
| `agents` | `AGENTS.md` |
| `codex` | `AGENTS.md` (Codex-compatible repository instructions) |
| `claude` | `CLAUDE.md` |
| `cursor` | `.cursor/rules/amo.mdc` |
| `cline` | `memory-bank/activeContext.md` |
| `opencode` | `OPENCODE.md` |

Obsidian notes are generated separately by `amo obsidian sync` or `amo graph export --format obsidian`.

Adapters are not the source of truth. `.ai/` is the source of truth.

Every coding-agent profile includes the repository authority order, preflight and expansion policy, degradation-triggered handoff, postflight, validation commands, and the disposable runtime policy. MCP is a separate stdio integration documented in [MCP Server](mcp-server.md); adapters remain generated instruction files rather than protocol servers.
