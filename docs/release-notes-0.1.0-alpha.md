# Release Notes: 0.1.0-alpha

AMO 0.1.0-alpha is the first public foundation for a Git-native repository memory layer for AI coding agents.

## What is included

- `.ai/` canonical memory scaffold
- CLI lifecycle commands
- file scan and machine indexes
- task-specific context packs
- session handoff packs for long or degraded agent sessions
- validation reports
- graph schema and graph build
- graph-aware context selection and hierarchical L0-L3 graph metadata
- Python module, symbol, import, and dependency extraction
- JSON, JSON-LD, GraphML, GEXF, Neo4j/Cypher, and Obsidian exports
- optional local embeddings
- AGENTS/Codex, Claude, Cursor, Cline, and OpenCode adapter exports
- interactive local organism dashboard
- executable truth-aware benchmark fixture flow
- evidence ledger
- propose-only optimizer and deterministic parameter sweeps with confirmed safe apply
- MCP stdio resources and tools
- robust postflight locking, backups, run history, outcomes, validation, changed files, and decisions
- manifesto and context rot positioning

## What is not stable yet

- PyPI distribution; this alpha is source-install only
- external embedding providers
- broader language extraction beyond the initial Python pass
- federation runtime (design only)

## Recommended validation

```bash
ruff check .
pytest
amo scan
amo preflight --task "release readiness" --profile quick
amo handoff --task "release readiness" --summary "release validation"
amo graph build
amo graph export --format json
amo graph export --format jsonld
amo graph export --format graphml
amo graph export --format gexf
amo graph export --format neo4j
amo embeddings build
amo benchmark examples/agent-debug-session --task "fix failing tests"
amo benchmark . --task "release readiness"
amo optimize suggest
amo optimize check
amo optimize plan
amo optimize params suggest
amo optimize params sweep --trials 10 --seed 42
amo optimize params best
amo validate --strict
amo status
```

## Installation and distribution

Install this alpha from source. PyPI publishing is explicitly deferred until a trusted
publisher is configured and verified; no local artifact will be uploaded manually.

## Safety model

Canonical memory is reviewed Git content. Machine indexes, packs, evolution output, and
runtime state have lower authority. The optimizer is propose-only; safe parameter apply
requires explicit confirmation and cannot edit source code. MCP canonical-memory writes
require confirmation and a non-empty summary.

## Feedback

Report bugs and documentation gaps through the repository's GitHub Issues page.

## Release intent

This alpha establishes a repo-native context discipline: agents start from compiled context, restart from handoff packs when sessions degrade, and write durable knowledge back into reviewed `.ai/` memory.
