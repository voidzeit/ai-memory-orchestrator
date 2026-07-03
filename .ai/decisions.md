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
- Advanced graph UI and MCP remain roadmap items.
