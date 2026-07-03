# AI Memory Orchestrator

**The cure for context rot in AI coding agents.**

AMO is a Git-native memory layer for AI coding agents. It gives a repository canonical memory, machine indexes, a project graph, validators, task-specific context packs, optional embeddings, and exports for agent tools.

Every coding agent starts by guessing repository context. AMO lets the agent start with verified project memory instead.

> Status: **0.1.0 alpha**. The CLI and file-based memory layer are usable. Graph intelligence, benchmarks, Neo4j export, Obsidian export, and optional embeddings are evolving in public.

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
.ai/machine/  = derived indexes, graph, validation, optional embeddings
.ai/packs/    = compiled context for agents
.ai/runtime/  = disposable session/cache state
AMO Web       = primary graph UI
Neo4j         = optional graph analytics export
Obsidian      = optional rich human graph view
```

## Graph architecture

AMO's graph is portable JSON first:

```txt
.ai/machine/graph.json
```

The graph is validated by:

```txt
schemas/amo-graph.schema.json
```

From that graph, AMO can export:

```bash
amo graph export --format json
amo graph export --format neo4j
amo graph export --format obsidian
```

Neo4j is useful for advanced graph analytics. Obsidian is useful for human navigation through notes, properties, tags, aliases, and wikilinks. Neither replaces `.ai/` as source of truth.

## Try it in 60 seconds

```bash
amo init
amo scan
amo preflight --task "fix failing tests"
amo graph build
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
.ai/machine/graph.json
.ai/packs/quick.md
AGENTS.md
```

## Optional embeddings

AMO can build a local deterministic embedding index without external APIs:

```bash
amo embeddings build
amo embeddings search "auth tests"
```

Embeddings are derived artifacts. They improve search and ranking but never replace canonical memory.

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
amo graph export --format neo4j
amo embeddings build
amo embeddings search "..."
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
- [Adoption guide](docs/adoption.md)
- [Maturity model](docs/maturity-model.md)
- [Schema contract](docs/schema-contract.md)
- [Architecture](docs/architecture.md)
- [Graph model](docs/graph-model.md)
- [Graph interoperability](docs/graph-interoperability.md)
- [Obsidian graph export](docs/obsidian-graph-export.md)
- [Neo4j export](docs/neo4j.md)
- [AMO and Obsidian](docs/obsidian-vs-amo.md)
- [Embeddings strategy](docs/embeddings.md)
- [Context engine](docs/context-engine.md)
- [Benchmark plan](docs/benchmark.md)
- [Comparison](docs/comparison.md)
- [Release notes](docs/release-notes-0.1.0-alpha.md)
- [Roadmap](docs/roadmap.md)

## Release readiness

```bash
ruff check .
pytest
amo scan
amo graph build
amo graph export --format neo4j
amo embeddings build
amo validate --strict
amo status
```

## License

Apache-2.0
