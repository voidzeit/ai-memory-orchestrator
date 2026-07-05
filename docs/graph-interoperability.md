# Graph Interoperability

AMO produces graph data that can be used by multiple systems while keeping one internal contract.

## Canonical graph

The portable contract is:

```txt
.ai/machine/graph.json
```

This file is AMO's internal graph contract. Stable node IDs, node types, edge types, and metadata originate here.

## Standard exports

Supported export targets:

```txt
json       lossless AMO native graph JSON
jsonld     linked data and future semantic integrations
graphml    general graph tooling such as NetworkX, yEd, and Gephi
gexf       network exploration and visualization, especially Gephi
neo4j      Cypher import for property-graph analytics
obsidian   Markdown notes with wikilinks and properties
```

Run `amo graph export --format <format>`.

## Design rule

AMO does not make a database or note app the source of truth.

```txt
.ai/ memory -> graph.json -> exports
```

## Obsidian graph view strategy

Obsidian builds its graph from notes and internal links. AMO's Obsidian export creates:

- one deterministic, collision-safe Markdown note per AMO node
- YAML properties for machine-readable metadata
- `tags` for graph groups
- `aliases` for readable node labels
- wikilinks for real graph edges
- index notes for navigation

## Portable graph strategy

AMO supports both major graph families:

- semantic graph and linked data through JSON-LD
- property graph analytics through Neo4j/Cypher, GraphML, and GEXF

The native AMO graph remains a simple node-edge contract that can be converted to both.
