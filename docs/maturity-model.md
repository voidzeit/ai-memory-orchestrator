# AMO Maturity Model

This model helps a repository move from ad-hoc AI usage to governed AI coding workflows.

## Level 0: No memory

The assistant starts from raw repository files and conversation context.

## Level 1: Static instructions

The repository has a manual instruction file such as `AGENTS.md`.

## Level 2: Canonical memory

The repository has reviewed `.ai/` memory files.

## Level 3: Compiled context

The repository uses task-specific context packs from `.ai/packs/`.

## Level 4: Validated memory

The repository runs AMO validators and tracks memory drift.

## Level 5: Graph-aware memory

The repository builds `graph.json` and uses graph exports for navigation or analytics.

## Level 6: Search-aware memory

The repository uses optional embeddings or search indexes to improve context selection.

## Level 7: Organization memory

Multiple repositories share compatible AMO schemas and can be analyzed together.
