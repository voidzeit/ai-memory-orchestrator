# Changelog

## 0.1.0-alpha

Initial public alpha preparation.

### Added

- Git-native `.ai/` canonical memory layer.
- `amo` CLI entrypoint.
- Commands for init, scan, context, preflight, postflight, validate, status, graph, server, export, and Obsidian sync.
- Machine indexes for files, artifacts, context units, graph, and validation.
- Token-oriented context pack generation.
- Local FastAPI graph viewer scaffold.
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

- The web graph viewer is still a minimal JSON view.
- Graph edges are basic.
- Context ranking is heuristic.
- MCP integration is documented but not implemented.
