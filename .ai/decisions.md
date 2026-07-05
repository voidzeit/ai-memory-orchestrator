# Decisions

## DEC-0001 — `.ai/` is source of truth

Status: accepted  
Date: 2026-07-03

Canonical project memory lives in `.ai/`.

Consequences:

- `.ai/machine/` indexes are derived.
- `.ai/packs/` context packs are derived.
- `.ai/runtime/` is disposable.
- Obsidian is optional.

## DEC-0002 — AMO Web is the primary graph interface

Status: accepted  
Date: 2026-07-03

The graph is generated as machine-readable JSON and visualized through AMO Web. Obsidian sync is an optional adapter.

## DEC-0003 — Context packs optimize utility per token

Status: accepted  
Date: 2026-07-03

The main product value is compiling the smallest sufficient context for an AI coding task.

## DEC-0004 — Public release starts as alpha

Status: accepted  
Date: 2026-07-03

The first public-ready release is `0.1.0-alpha`. It should be honest about current limitations while keeping the CLI, memory scaffold, validation, server scaffold, and adapters usable.

Consequences:

- README marks project status as alpha.
- CHANGELOG documents known limitations.
- Security and contribution docs are included before public visibility.
- At decision time, advanced graph UI and MCP were roadmap items. Both were implemented before the alpha-readiness reconciliation; this historical note no longer describes current implementation status.

## DEC-0005 — Graph JSON is canonical; Neo4j and Obsidian are exports

Status: accepted  
Date: 2026-07-03

AMO stores the portable graph contract in `.ai/machine/graph.json`.

Consequences:

- Neo4j is an optional analytics export.
- Obsidian is an optional rich human view.
- AMO Web reads the same graph JSON.
- `.ai/` remains the source of truth.

## DEC-0006 — Embeddings are optional derived intelligence

Status: accepted  
Date: 2026-07-03

Embeddings improve search and ranking, but they are derived artifacts and never replace canonical memory.

## DEC-0007 — Long chats should compact into handoff packs

Status: accepted  
Date: 2026-07-03

AMO treats chat history as volatile runtime context, not project truth. Long or degraded agent sessions should produce `.ai/packs/handoff.md` and restart from repository memory.

Consequences:

- `amo handoff` is part of the release workflow.
- Context packs include degradation signals.
- Agents should prefer handoff packs over old chat transcripts.
