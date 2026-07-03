# Obsidian Graph Export

AMO's Obsidian export should be optimized for Obsidian Graph View, not just for reading Markdown.

## Obsidian primitives AMO should use

- Markdown notes as nodes
- wikilinks as edges
- YAML properties as structured metadata
- `tags` as graph groups
- `aliases` as readable labels
- folders as graph scopes
- index notes as navigation hubs

## Recommended vault layout

```txt
.obsidian/project-memory/
├── index.md
├── State.md
├── Decisions.md
├── Tasks.md
├── Tests.md
└── Graph/
    ├── index.md
    ├── Nodes/
    ├── Edges/
    ├── Views/
    └── Queries.md
```

## Node note template

```md
---
amo_id: "file:src/app.py"
amo_type: file
source_path: "src/app.py"
tags:
  - amo/node
  - amo/node/file
aliases:
  - "src/app.py"
---

# src/app.py

## Outbound

- contains -> [[dir - src]]

## Inbound

- [[repo - my-project]] -> contains
```

## Graph View groups

Use Obsidian Graph View groups with searches such as:

```txt
tag:#amo/node/file
tag:#amo/node/memory
tag:#amo/node/test
tag:#amo/node/context_pack
tag:#amo/node/directory
```

## Local graph

Every AMO node note should have enough wikilinks for Obsidian's local graph depth slider to reveal meaningful neighborhoods.
