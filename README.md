# AI Memory Orchestrator

**Durable repo memory. Minimal tokens. Maximum context signal.**

AI Memory Orchestrator, or **AMO**, is a Git-native memory compiler for AI coding agents. It gives any repository a durable, validated, agent-readable memory layer.

AMO creates a canonical `.ai/` memory system, generates token-optimized context packs, builds machine indexes and project graphs, validates drift and artifact hygiene, serves a local web graph viewer, and optionally syncs to Obsidian.

> Status: **0.1.0 alpha**. The CLI and file-based memory layer are usable; graph intelligence and advanced adapters are still evolving.

## Why AMO?

AI coding agents read too much, forget fast, duplicate context, and often cannot tell what is actually true inside a repository.

AMO fixes that with:

- canonical repo memory in `.ai/`
- compact machine indexes in `.ai/machine/`
- task-specific context packs in `.ai/packs/`
- preflight/postflight lifecycle
- drift and artifact hygiene validation
- local web graph viewer
- optional Obsidian sync
- adapters for `AGENTS.md`, Claude Code, Cursor, Cline, Codex, and OpenCode

## Core idea

```txt
.ai/          = source of truth
.ai/machine/  = derived indexes
.ai/packs/    = compiled context for agents
.ai/runtime/  = disposable session/cache state
AMO Web       = primary graph UI
Obsidian      = optional human graph adapter
```

## Install

From source:

```bash
git clone https://github.com/voidzeit/ai-memory-orchestrator.git
cd ai-memory-orchestrator
pip install -e '.[dev]'
```

Future package install:

```bash
pip install ai-memory-orchestrator
```

## Quickstart

```bash
cd your-repo
amo init
amo scan
amo preflight --task "fix failing tests"
amo validate
```

Serve the local graph viewer:

```bash
amo graph build
amo server --host 127.0.0.1 --port 8787
```

LAN access requires a token:

```bash
export AMO_SERVER_TOKEN="change-me"
amo server --host 0.0.0.0 --port 8787 --token
```

## Main commands

```bash
amo init
amo scan
amo context --task "..."
amo preflight --task "..."
amo postflight --task "..." --summary "..."
amo validate
amo status
amo graph build
amo server --host 127.0.0.1 --port 8787
amo export --target agents
amo export --target claude
amo export --target cursor
amo export --target cline
amo export --target opencode
amo obsidian sync
```

## Context compiler

AMO does not feed the whole repo to an agent. It compiles the smallest sufficient context for the task:

```txt
repo + .ai memory + task
        ↓
context units
        ↓
ranking utility/token
        ↓
compression
        ↓
expansion map
        ↓
context pack
```

## Release readiness

Before publishing a release:

```bash
ruff check .
pytest
amo scan
amo graph build
amo validate --strict
amo status
```

## License

Apache-2.0
