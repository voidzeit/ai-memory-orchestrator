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
- Neo4j export
- Obsidian export
- optional local embeddings
- agent adapter exports
- local server scaffold
- benchmark plan
- manifesto and context rot positioning

## What is not stable yet

- interactive graph UI
- MCP server implementation
- advanced adapter profiles
- automated benchmark command
- external embedding providers

## Recommended validation

```bash
ruff check .
pytest
amo scan
amo preflight --task "release readiness" --profile quick
amo handoff --task "release readiness" --summary "release validation"
amo graph build
amo graph export --format neo4j
amo embeddings build
amo validate --strict
amo status
```

## Release intent

This alpha establishes a repo-native context discipline: agents start from compiled context, restart from handoff packs when sessions degrade, and write durable knowledge back into reviewed `.ai/` memory.
