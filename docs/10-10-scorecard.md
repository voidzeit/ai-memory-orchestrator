# AMO 10/10 Scorecard

This scorecard defines what AMO needs to reach a public, industry-grade 10/10 release state.

## Current position

AMO already has a strong product thesis, CLI, context packs, handoff workflow, graph model, Obsidian export, Neo4j export, optional embeddings, release docs, and a release-check workflow.

The remaining work is not more vision. The remaining work is confidence.

## 10/10 criteria

| Area | 10/10 requirement | Current gap |
|---|---|---|
| Public narrative | Clear category and problem | Mostly done |
| README | First-screen value, quickstart, architecture, commands | Mostly done |
| Architecture | Stable source-of-truth model and schemas | Needs schema validation in CI |
| CLI | Lifecycle commands are coherent and tested | Needs more command-level tests |
| Context discipline | Profiles, budgets, handoff, degradation rules | Mostly done |
| Graph model | Validated graph contract and standard exports | Needs JSON-LD, GraphML, GEXF |
| Obsidian | Real graph-view notes, tags, aliases, links | Needs example fixture |
| Neo4j | Cypher export and docs | Needs sample import docs/test fixture |
| Embeddings | Local optional index, provider abstraction later | Needs provider interface roadmap |
| Testing | Unit + integration + command smoke tests | Needs broader CLI smoke tests |
| CI/release | Release workflow runs and required checks pass | Needs confirmed Actions runs |
| Security posture | Scorecard, dependency updates, branch protection | Needs enforcement/settings |
| Community | Issues, PR template, contributing docs | Needs code of conduct/support docs |
| Packaging | PyPI-ready release path | Needs trusted publishing workflow |
| Evidence | Benchmark proves value | Needs executable benchmark |

## Release blocker checklist

- [ ] Make repository public.
- [ ] Confirm GitHub Actions run on `main`.
- [ ] Protect `main` with required checks.
- [ ] Validate `.ai/machine/graph.json` against `schemas/amo-graph.schema.json`.
- [ ] Add command smoke tests for the CLI.
- [ ] Add sample Obsidian graph fixture.
- [ ] Implement executable benchmark command.
- [ ] Add JSON-LD, GraphML, and GEXF exporters.
- [ ] Add real adapter profile outputs.
- [ ] Add MCP resources/tools.
- [ ] Add PyPI Trusted Publishing release workflow.
- [ ] Create `v0.1.0-alpha` release tag.

## 10/10 principle

A 10/10 AMO release must be:

```txt
understandable in 30 seconds
installable in 60 seconds
validated in CI
measurable by benchmark
safe enough for teams
useful with real agents
portable across graph systems
```
