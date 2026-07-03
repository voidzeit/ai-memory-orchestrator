# State

## Project Identity

AI Memory Orchestrator is a Git-native memory compiler for AI coding agents.

## Current Truth

- The product core is a Python CLI named `amo`.
- Canonical project memory lives in `.ai/`.
- Machine indexes live in `.ai/machine/`.
- Token-optimized context packs live in `.ai/packs/`.
- Runtime/cache lives in `.ai/runtime/` and is gitignored.
- AMO Web is the primary graph viewer.
- Obsidian is an optional adapter.
- The repository is being hardened for public `0.1.0-alpha` release.

## Implemented

- CLI scaffold.
- Init, scan, context, preflight, postflight, validate, status, graph, server, export, and Obsidian sync commands.
- Generic templates with specialized Python/Node overlays.
- Basic validators.
- AGENTS.md, Claude, Cursor, Cline, and OpenCode adapter exports.
- Obsidian export adapter.
- FastAPI server scaffold.
- GitHub Actions CI.
- OpenCode workflow scaffold.
- Release docs: README, changelog, contributing guide, security policy, and roadmap.

## Known gaps

- Interactive web graph UI is still minimal.
- Context ranking is heuristic.
- Graph edges are basic.
- MCP integration is documented but not implemented.
- Repository visibility must still be changed in GitHub settings if public release is desired.
