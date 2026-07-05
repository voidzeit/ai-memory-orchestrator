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
## Postflight — 2026-07-04T04:54:53.734060+00:00

Task: make AMO the repo-native memory and graph operating layer

Summary: Stabilized runtime validation and config, integrated foundation branches, added graph contract validation and levels, Python structure extraction, standard exports, collision-safe Obsidian notes, full agent profiles, deterministic benchmark, and safe evolve.
## Postflight — 2026-07-05T05:05:38.264353+00:00

Task: implement staged deterministic optimizable parameters

Summary: Added typed parameter search spaces, deterministic seeded sweeps, normalized evidence-aware objectives, evolutionary trial reports, safe-only promotion, and parameter-driven context ranking.
## Postflight — 2026-07-05T08:13:51.889057+00:00

Task: test postflight

Summary: validated run history

Outcome: completed
Changed files: amo/core/postflight.py
