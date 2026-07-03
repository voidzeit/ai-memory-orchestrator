# AMO Graph Ontology

This document defines the semantic contract for AMO graph nodes and edges.

## Design goals

The ontology must be:

- stable enough for external tools
- simple enough for alpha adoption
- hierarchical enough for large repositories
- compatible with property graphs and RDF-style exports
- useful for coding agents, not just graph databases

## Node classes

### Structural nodes

| Type | Meaning |
|---|---|
| `repository` | root project container |
| `directory` | filesystem grouping |
| `file` | source, documentation, config, or artifact file |
| `module` | language-level or package-level unit |
| `symbol` | function, class, method, type, component |

### Memory nodes

| Type | Meaning |
|---|---|
| `memory` | canonical AMO memory file or memory section |
| `decision` | accepted or proposed project decision |
| `task` | open, done, or deferred work item |
| `test` | test file, suite, case, or validation command |
| `risk` | known risk, blocker, drift, or uncertainty |
| `context_pack` | generated task-specific agent context |

### Operations nodes

| Type | Meaning |
|---|---|
| `workflow` | CI, release, validation, or agent workflow |
| `validator` | rule or process that checks project quality |
| `artifact` | generated output, index, report, or export |
| `adapter` | integration target such as Claude, Cursor, Cline, OpenCode, Obsidian, Neo4j, MCP |

## Edge classes

### Structure

| Type | Meaning |
|---|---|
| `contains` | parent contains child |
| `belongs_to` | child belongs to logical parent |
| `references` | node refers to another node |
| `depends_on` | source requires target |

### Memory and evidence

| Type | Meaning |
|---|---|
| `documents` | memory or docs describe target |
| `derived_from` | node/artifact was generated from evidence |
| `supersedes` | newer memory replaces older memory |
| `conflicts_with` | two nodes disagree or are inconsistent |

### Quality and delivery

| Type | Meaning |
|---|---|
| `tested_by` | target is tested by source |
| `validates` | validator checks target |
| `generates` | workflow or builder generates artifact |
| `exports_to` | graph or memory exports to adapter target |

## Authority model

Authority scores should be interpreted as relative trust, not absolute truth.

Suggested authority defaults:

```txt
source code             1.00
git history             0.95
.ai canonical memory    0.90
machine indexes         0.80
context packs           0.70
adapter exports         0.60
runtime notes           0.40
chat summaries          0.25
```

Conflicts should resolve toward the higher-authority source unless a human updates canonical memory.

## Stable identifiers

Node ids should be deterministic.

Recommended format:

```txt
repo:{repo_name}
dir:{path}
file:{path}
module:{path_or_module_name}
symbol:{path}::{qualified_name}
memory:{name}
decision:{id}
task:{id}
test:{path_or_test_id}
pack:{path}
workflow:{name}
validator:{name}
artifact:{path}
adapter:{target}
risk:{id}
```

## Compatibility

AMO graph JSON should map cleanly to:

- property graph nodes and relationships
- RDF subjects, predicates, and objects
- Obsidian notes and wikilinks
- GraphML nodes and edges
- GEXF nodes and edges

AMO should not invent a new graph exchange universe. It should maintain one internal contract and export to existing standards.
