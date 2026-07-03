# Neo4j Export

AMO does not require Neo4j, but the graph model is compatible with Neo4j.

The default AMO graph lives in Git as JSON:

```txt
.ai/machine/graph.json
```

For Neo4j, export Cypher:

```bash
amo scan
amo graph build
amo graph export --format neo4j
```

This creates:

```txt
.ai/machine/graph.cypher
```

## Why use Neo4j?

Neo4j is useful when AMO needs:

- multi-repository graph analytics
- advanced dependency queries
- organization-level memory maps
- historical graph analysis
- graph algorithms

## Why not require it?

AMO is Git-native first. A repository should remain agent-ready without any external database.

Neo4j is an optional power-user export, not the source of truth.

## Source of truth order

```txt
source code > git history > .ai/ memory > .ai/machine/graph.json > Neo4j export
```

If Neo4j disagrees with `.ai/`, `.ai/` wins.
