# AI Memory Orchestrator

**Durable repo memory. Minimal tokens. Maximum context signal.**

AI Memory Orchestrator, or **AMO**, is a Git-native memory compiler for AI coding agents. It gives any repository a durable, validated, agent-readable memory layer.

AMO creates a canonical `.ai/` memory system, generates token-optimized context packs, builds machine indexes and project graphs, validates drift and artifact hygiene, serves a local web graph viewer, and optionally syncs to Obsidian.

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
- adapters for `AGENTS.md`, Claude Code, Cursor, Cline, Codex, OpenCode, and MCP-native tools

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

```bash
pip install ai-memory-orchestrator
```

For local development:

```bash
pip install -e .[dev]
```

## Quickstart

```bash
cd your-repo
amo init
amo scan
amo context --task "fix failing tests"
amo validate
```

## Main commands

```bash
amo init
amo scan
amo context --task "..."
amo postflight --task "..." --summary "..."
amo validate
amo graph build
amo server --host 127.0.0.1 --port 8787
amo export --target agents
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

## License

Apache-2.0
