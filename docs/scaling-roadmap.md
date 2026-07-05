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

## Alpha foundation completed

1. Graph contract validation in strict validation and release-check.
2. Graph fixtures and CLI smoke tests.
3. Collision-safe Obsidian export and sample vault.
4. JSON-LD, GraphML, and GEXF exports.
5. Initial Python module, symbol, import, and dependency extraction.
6. Generated agent adapter profiles.
7. MCP resources and tools.
8. Benchmark, evidence, evolve, and propose-only optimizer workflows.

## Next scaling work

1. Broaden language extractors and dependency semantics.
2. Add test-source linking and graph drift detection.
3. Expand truth fixtures and adoption examples.
4. Implement federation only after the alpha release gates are green.

## Enterprise gate

A feature is ready only when it has configuration, schema, validation, tests, docs, examples, safe defaults, and clear failure messages.
