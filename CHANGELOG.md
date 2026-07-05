# Changelog

## 0.1.0-alpha

Initial public alpha preparation.

### Added

- Git-native `.ai/` canonical memory layer.
- `amo` CLI entrypoint.
- Commands for init, scan, context, preflight, postflight, validate, status, graph, server, export, and Obsidian sync.
- Executable benchmark fixtures with optional truth annotations and explicitly unscored metrics when truth is absent.
- Evidence ledger integration across lifecycle, graph, benchmark, optimizer, MCP, and adapter operations.
- Propose-only optimizer commands and deterministic, seeded parameter sweeps with safe-only confirmed apply.
- JSON, JSON-LD, GraphML, GEXF, Neo4j/Cypher, and Obsidian graph exports.
- Python module, symbol, and import/dependency extraction in the hierarchical graph.
- MCP stdio resources and tools with explicit confirmation for canonical-memory writes.
- Interactive local organism dashboard with graph inspection, search, filters, node details, and warnings.
- Machine indexes for files, artifacts, context units, graph, and validation.
- Token-oriented context pack generation.
- Local FastAPI organism dashboard and API.
- Agent exports for AGENTS.md, Claude, Cursor, Cline, and OpenCode.
- Generic, Python, and Node template scaffolds.
- Basic validators for canonical files, runtime pollution, and unsafe instructions.
- GitHub Actions CI.

### Fixed

- Template inheritance now overlays specialized templates on top of the generic scaffold.
- Scanner no longer excludes every folder named `runtime`; it excludes `.ai/runtime` specifically.
- LAN server mode requires an explicit token flag.
- Stale `.ai/tasks.md` bootstrap entry refreshed.

### Known limitations

- Repository visibility, branch protection, and required checks remain GitHub settings.
- CodeQL and OpenSSF Scorecard need a successful run after public visibility and permissions are configured.
- External embedding providers are not included.
- Federation remains design-only.
- PyPI publication requires trusted-publisher configuration and an explicit release decision.
