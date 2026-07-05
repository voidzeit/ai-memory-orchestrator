# AMO 10/10 Scorecard

This scorecard defines what AMO needs to reach a public, industry-grade 10/10 release state.

## Current position

AMO has a verified CLI operating layer, context and handoff packs, hierarchical graph, standard exports, truth-aware benchmark, evidence ledger, propose-only optimizer, deterministic parameter sweeps, MCP stdio server, organism dashboard, optional embeddings, adapter profiles, release docs, and release workflows.

The remaining work is not more vision. The remaining work is confidence.

## 10/10 criteria

| Area | 10/10 requirement | Status |
|---|---|---|
| Public narrative | Clear category and problem | Done |
| README | First-screen value, quickstart, architecture, commands | Done |
| Architecture | Stable source-of-truth model and schemas | Done; strict validation executes the checked-in JSON Schema artifact in release-check |
| CLI | Lifecycle commands are coherent and tested | Done; command registration and release smoke paths are tested |
| Context discipline | Profiles, budgets, handoff, degradation rules | Done |
| Graph model | Validated graph contract, hierarchy, code structure, standard exports | Done |
| Obsidian | Real graph-view notes, tags, aliases, links, sample fixture | Done |
| Neo4j | Cypher export and docs | Done |
| Embeddings | Local optional deterministic index | Done for alpha; external providers remain future work |
| Testing | Unit, integration, command registration, release smoke path | Done locally; needs CI confirmation for this branch |
| CI/release | Release workflow runs and required checks pass | Release Check and CI passed on `main`; CodeQL and Scorecard are still blocked/failing |
| Security posture | CodeQL, Scorecard, dependency updates, branch protection | Implemented, needs GitHub visibility/settings and green security runs |
| Community | Issues, PR template, contributing, conduct, support | Done |
| Packaging | Build/check workflow and trusted publishing | Workflow done; publisher configuration and publish timing remain manual |
| Evidence | Truth-aware benchmark and durable ledger | Done |

## Release blocker checklist

- **Done:** executable benchmark, evidence ledger, optimizer, parameter sweep, graph hierarchy and validation, standard exporters, organism UI, MCP, adapter profiles, hardened postflight, command smoke tests, and sample Obsidian vault.
- **Implemented, needs CI confirmation:** expanded `release-check` command path and CodeQL `actions: read` permission.
- **Manual GitHub setting:** make the repository public; protect `main`; require PRs and `release-check`; disable force pushes and branch deletion.
- **Still open:** obtain green CodeQL and OpenSSF Scorecard runs after visibility/settings changes.
- **Done:** PyPI is explicitly deferred; `0.1.0-alpha` is source-install only.
- **Still open:** create `v0.1.0-alpha` only after every release gate is green.

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
