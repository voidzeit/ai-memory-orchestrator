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
- Obsidian is an optional rich human graph view.
- Neo4j is an optional graph analytics export.
- Embeddings are optional derived intelligence.

## Implemented

- CLI lifecycle commands.
- Graph schema and JSON graph contract.
- Neo4j/Cypher graph export.
- Obsidian graph note export.
- Local deterministic embedding index.
- Generic templates with Python/Node overlays.
- Basic validators and agent adapter exports.
- FastAPI server scaffold and CI.

## Known gaps

- Interactive web graph UI is still minimal.
- Context ranking is heuristic.
- MCP integration is documented but not implemented.
- Repository visibility must still be changed in GitHub settings if public release is desired.
