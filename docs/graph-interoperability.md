# Graph Interoperability

AMO should produce graph data that can be used by multiple systems.

## Canonical graph

The portable contract is:

```txt
.ai/machine/graph.json
```

This file is AMO's internal graph contract.

## Standard exports

Planned and supported export targets:

```txt
json       AMO native graph JSON
jsonld     linked data / semantic web systems
graphml    graph tooling and exchange
gexf       network visualization tools
neo4j      Cypher import for Neo4j
obsidian   Markdown notes with wikilinks and properties
```

## Design rule

AMO should not make a database or note app the source of truth.

```txt
.ai/ memory -> graph.json -> exports
```

## Obsidian graph view strategy

Obsidian builds its graph from notes and internal links. Therefore AMO's Obsidian export should create:

- one Markdown note per AMO node
- YAML properties for machine-readable metadata
- `tags` for graph groups
- `aliases` for readable node labels
- wikilinks for real graph edges
- index notes for navigation

## Portable graph strategy

AMO should support both major graph families:

- semantic graph / linked data through JSON-LD
- property graph analytics through Neo4j/Cypher

The native AMO graph remains a simple node-edge contract that can be converted to both.
