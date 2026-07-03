# Release Notes: 0.1.0-alpha

AMO 0.1.0-alpha is the first public foundation for a Git-native repository memory layer for AI coding agents.

## What is included

- `.ai/` canonical memory scaffold
- CLI lifecycle commands
- file scan and machine indexes
- task-specific context packs
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
amo graph build
amo graph export --format neo4j
amo embeddings build
amo validate --strict
amo status
```

## Release intent

This alpha is meant to establish the architecture, schema, and product direction before deeper integrations.
