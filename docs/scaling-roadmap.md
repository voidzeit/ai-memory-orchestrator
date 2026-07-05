# AMO Scaling Roadmap

AMO scales by layers.

## Repository scale

```txt
small       files, memory, context packs
medium      modules, tests, decisions
large       symbols, dependencies, validators
enterprise  multi-repo graph, policies, benchmarks
```

## Graph scale

```txt
L0 filesystem
L1 canonical memory
L2 modules and symbols
L3 tests, validators, risks
L4 workflows, adapters, artifacts
L5 embeddings, benchmarks, evolution
```

## Agent scale

```txt
preflight   compile focused context
handoff     restart degraded sessions
postflight  write durable memory
evolve      detect memory quality issues
benchmark   measure context quality
```

## Near-term phases

1. Validate graph JSON against schema.
2. Add graph fixtures and CLI smoke tests.
3. Add collision-safe Obsidian export.
4. Implement JSON-LD, GraphML, and GEXF exports.
5. Add module, symbol, import, and dependency extraction.
6. Strengthen real agent adapters.
7. Add MCP resources and tools.
8. Add benchmark and evolve workflows.

## Enterprise gate

A feature is ready only when it has configuration, schema, validation, tests, docs, examples, safe defaults, and clear failure messages.
