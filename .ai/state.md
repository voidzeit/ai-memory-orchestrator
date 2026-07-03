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

## Implemented in bootstrap

- CLI scaffold.
- Init, scan, context, postflight, validate, graph, server commands.
- Generic templates.
- Basic validators.
- AGENTS.md adapter.
- Obsidian adapter.
- FastAPI server scaffold.
- GitHub Actions CI.
- OpenCode workflow scaffold.

## Known gaps

- Interactive web graph UI is still minimal.
- Context ranking is heuristic.
- Graph edges are basic.
- Adapter implementations beyond AGENTS.md and Obsidian are placeholders/future work.
