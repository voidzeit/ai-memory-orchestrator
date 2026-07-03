# AMO Schema Contract

AMO is useful to teams only if its files are predictable.

This document defines the stable file contracts that tools, agents, CI jobs, and future integrations can depend on.

## Canonical memory

```txt
.ai/manifest.yaml
.ai/state.md
.ai/decisions.md
.ai/tasks.md
.ai/tests.md
.ai/graph.md
```

These files are human-readable and versioned in Git.

## Derived machine data

```txt
.ai/machine/files.json
.ai/machine/context_units.json
.ai/machine/artifacts.json
.ai/machine/graph.json
.ai/machine/validation.json
.ai/machine/embedding_index.json
.ai/machine/embeddings.jsonl
```

These files are derived. They can be regenerated.

## Context packs

```txt
.ai/packs/quick.md
.ai/packs/debug.md
.ai/packs/architecture.md
.ai/packs/full.md
```

Context packs are compiled task surfaces for AI coding agents.

## Runtime

```txt
.ai/runtime/
```

Runtime files are disposable and should be ignored by Git.

## Stability policy

- Canonical memory file names should remain stable.
- Machine JSON schema changes should increment `schema_version`.
- New fields should be additive when possible.
- Breaking changes should be documented in the changelog.
