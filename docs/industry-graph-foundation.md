# Industry Graph Foundation

See [Graph interoperability](graph-interoperability.md) for JSON-LD, GraphML, and GEXF export guidance.

AMO must scale as a repository memory graph, not as a loose set of markdown summaries.

The industrial target is a graph contract that is hierarchical, portable, queryable, explainable, and safe for teams.

## Core rule

```txt
.ai/ canonical memory -> graph.json -> validated exports -> agent packs
```

`.ai/` remains the source of truth. `.ai/machine/graph.json` is the canonical machine graph. All other graph outputs are derived.

## Hierarchy

AMO uses a layered graph hierarchy:

```txt
Repository
  Directory
    File
      Module
        Symbol
          Behavior

Repository
  Memory
    Decision
    Task
    Test
    Risk
    Context Pack

Repository
  Workflow
    Validator
    Artifact
    Adapter
    Export
```

This allows AMO to answer questions at different levels of detail without loading the whole repository.

## Required graph properties

Every graph node should eventually support:

```txt
id              stable unique identifier
type            controlled node type
label           human-readable name
path            source path when available
source          source system or derivation step
authority       confidence/source authority score
metadata        tool-specific attributes
```

Every graph edge should eventually support:

```txt
source          source node id
target          target node id
type            controlled relationship type
label           optional human-readable relationship
metadata        evidence and derivation details
```

## Industrial graph capabilities

AMO should support:

- hierarchical navigation from repository to symbol
- memory-to-code traceability
- decision-to-file traceability
- test coverage mapping
- risk and validator findings
- context pack derivation paths
- export adapters for graph ecosystems
- deterministic node ids
- schema validation in CI
- incremental graph builds
- stable graph exports

## Standard export targets

AMO should keep one native graph contract and export to established ecosystems:

| Target | Purpose |
|---|---|
| AMO JSON | canonical internal machine graph |
| JSON-LD / RDF | semantic web and linked-data interoperability |
| GraphML | generic graph exchange and graph tooling |
| GEXF | Gephi and visual network analysis |
| Neo4j Cypher | property graph analytics |
| Obsidian Markdown | human graph navigation |
| MCP resources | live agent access |

## Scaling model

The graph must scale in layers:

```txt
Level 0: repository, files, directories
Level 1: memory files, context packs, tests
Level 2: symbols, modules, imports, dependencies
Level 3: decisions, risks, validators, artifacts
Level 4: semantic concepts and domain ontology
Level 5: temporal evolution and benchmark evidence
```

Each level must be independently buildable and testable.

## Query goals

A useful AMO graph should answer:

- What files are relevant to this task?
- Which decisions govern this module?
- What tests validate this behavior?
- What context pack was derived from which evidence?
- Which memory is stale or contradicted by code?
- Which parts of the repo changed since the last handoff?
- Which nodes are high authority vs derived or runtime-only?

## Release rule

No graph feature is complete unless it has:

- schema definition
- builder or exporter implementation
- test fixture
- validation path
- docs
- example command
