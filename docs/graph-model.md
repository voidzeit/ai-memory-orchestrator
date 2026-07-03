# AMO Graph Model

AMO graph data is richer than an Obsidian backlink graph and lighter than a mandatory graph database.

The canonical graph is stored as JSON:

```txt
.ai/machine/graph.json
```

This file is the portable graph contract. Other views can be generated from it.

## Node types

- repository
- directory
- file
- memory
- decision
- task
- test
- workflow
- artifact
- context_pack
- adapter
- validator
- risk

## Edge types

- contains
- documents
- references
- depends_on
- generates
- validates
- tested_by
- derived_from
- exports_to
- belongs_to
- supersedes
- conflicts_with

## Why JSON first?

JSON keeps AMO portable:

- works in Git
- works without services
- works in CI
- works offline
- can be served by AMO Web
- can be exported to Neo4j
- can be exported to Obsidian notes

## Neo4j compatibility

AMO can export the graph to Cypher:

```bash
amo graph export --format neo4j
```

Default output:

```txt
.ai/machine/graph.cypher
```

Neo4j is best when you want advanced graph queries, central analytics, or multi-repo knowledge graphs.

## Obsidian compatibility

AMO can export graph nodes as Markdown notes:

```bash
amo graph export --format obsidian
```

Obsidian is best for human navigation, writing, review, and visual exploration.

## AMO Web

AMO Web is the primary built-in graph viewer. It reads the same canonical graph data and does not require Obsidian or Neo4j.
