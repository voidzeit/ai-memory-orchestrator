# Adoption Guide

AMO is designed to be adopted gradually.

## Phase 1: Memory scaffold

- Run `amo init`.
- Review `.ai/` files.
- Commit canonical memory.

## Phase 2: Context packs

- Run `amo scan`.
- Run `amo preflight --task "your task"`.
- Review `.ai/packs/quick.md`.

## Phase 3: Validation

- Run `amo validate`.
- Keep `.ai/runtime/` out of Git.
- Update memory through pull requests when project truth changes.

## Phase 4: Tool adapters

- Run `amo export --target agents`.
- Add other exports only when needed.
- Keep `.ai/` as source of truth.

## Phase 5: Graph and search

- Run `amo graph build`.
- Export to Neo4j for graph analytics.
- Export to Obsidian for human navigation.
- Build embeddings when semantic search is useful.

## Principle

AMO should reduce context overhead, not add process overhead.
