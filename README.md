# AI Memory Orchestrator

**The cure for context rot in AI coding agents.**

AMO is a Git-native memory layer for AI coding agents. It gives a repository canonical memory, machine indexes, a project graph, validators, and task-specific context packs.

Every coding agent starts by guessing repository context. AMO lets the agent start with verified project memory instead.

> Status: **0.1.0 alpha**. The CLI and file-based memory layer are usable. Graph intelligence, benchmarks, and advanced adapters are evolving in public.

## Context rot

**Context rot** is stale, duplicated, incomplete, or contradictory repository knowledge that causes AI coding agents to choose the wrong files, miss decisions, waste tokens, or repeat past mistakes.

AMO exists because bigger context windows are not enough.

```txt
More context is not intelligence.
Verified context is intelligence.
```

## What AMO creates

```txt
.ai/          = source of truth
.ai/machine/  = derived indexes
.ai/packs/    = compiled context for agents
.ai/runtime/  = disposable session/cache state
AMO Web       = primary graph UI
Obsidian      = optional human graph adapter
```

## Try it in 60 seconds

```bash
amo init
amo scan
amo preflight --task "fix failing tests"
amo validate
```

AMO creates a repository memory scaffold and a task-focused context pack:

```txt
.ai/manifest.yaml
.ai/state.md
.ai/decisions.md
.ai/tasks.md
.ai/tests.md
.ai/graph.md
.ai/machine/context_units.json
.ai/packs/quick.md
AGENTS.md
```

## Install from source

```bash
git clone https://github.com/voidzeit/ai-memory-orchestrator.git
cd ai-memory-orchestrator
pip install -e '.[dev]'
```

Future package install:

```bash
pip install ai-memory-orchestrator
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

## Why this matters

Before AMO:

```txt
Agent opens repo
  -> scans random files
  -> misses decisions
  -> reads stale docs
  -> burns tokens
  -> edits the wrong module
```

After AMO:

```txt
Agent opens repo
  -> reads .ai/packs/quick.md
  -> sees current truth
  -> sees relevant files
  -> sees risks and tests
  -> expands only when needed
```

## Docs

- [Manifesto](docs/manifesto.md)
- [Problem: context rot](docs/problem.md)
- [Architecture](docs/architecture.md)
- [Context engine](docs/context-engine.md)
- [Benchmark plan](docs/benchmark.md)
- [Comparison](docs/comparison.md)
- [Roadmap](docs/roadmap.md)

## Release readiness

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
