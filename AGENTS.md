# Agent Instructions

This repository uses AI Memory Orchestrator conventions.

## Source of truth

Canonical project memory lives in `.ai/` when present.

Read these first if they exist:

```txt
.ai/manifest.yaml
.ai/state.md
.ai/tasks.md
.ai/decisions.md
.ai/tests.md
.ai/packs/quick.md
```

## Runtime is not memory

Do not treat `.ai/runtime/` as canonical. It is disposable session/cache state.

## Before work

Prefer compact context packs before reading full files.

```bash
amo context --task "<task>"
```

## After work

When a task changes project state, update memory through postflight:

```bash
amo postflight --task "<task>" --summary "<what changed>"
amo validate
```

## Safety rules

- Do not push directly to `main` unless explicitly asked.
- Work through branches and pull requests.
- Make the smallest safe change.
- Do not expose secrets or API keys.
- Do not delete files unless explicitly requested.
- Update tests or docs when behavior changes.
