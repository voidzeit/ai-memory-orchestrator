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
