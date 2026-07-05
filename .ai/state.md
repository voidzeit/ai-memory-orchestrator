# State

## Project Identity

AI Memory Orchestrator is a Git-native memory compiler for AI coding agents.

## Current Truth

- The product core is a Python CLI named `amo`.
- Canonical project memory lives in `.ai/`.
- Machine indexes live in `.ai/machine/`.
- Token-optimized context packs live in `.ai/packs/`.
- Runtime/cache lives in `.ai/runtime/` and is gitignored.
- AMO Web is the primary graph viewer.
- Obsidian is an optional rich human graph view.
- Neo4j is an optional graph analytics export.
- Embeddings are optional derived intelligence.

## Implemented

- CLI lifecycle commands: init, scan, context/preflight, handoff, robust postflight, validate, and status.
- Hierarchical graph schema and JSON contract with graph-aware context selection.
- Python module, symbol, import, and dependency extraction.
- JSON, JSON-LD, GraphML, GEXF, Neo4j/Cypher, and collision-safe Obsidian graph exports.
- Executable deterministic benchmark with optional truth fixtures and explicitly unscored metrics when truth is absent.
- Evidence ledger integration for lifecycle, graph, benchmark, optimizer, MCP, and adapter operations.
- Propose-only optimizer suggest/check/plan commands.
- Typed deterministic parameter suggest/sweep/best commands and confirmed safe-only apply.
- Locking, backup, run history, outcome, validation, changed-file, decision, and ledger support in postflight.
- Dependency-free MCP stdio resources and tools; canonical-memory writes require explicit confirmation.
- Interactive organism dashboard with graph inspection, search, filters, node details, warnings, and API endpoints.
- Local deterministic embeddings and search.
- Generated AGENTS/Codex, Claude, Cursor, Cline, and OpenCode adapter profiles.
- Release Check, CI, CodeQL, OpenSSF Scorecard, Dependabot, and trusted-publishing workflow definitions.
- Code of Conduct, Support, Security, Contributing, changelog, roadmap, and alpha release notes.

## Remaining gaps

- The repository is public.
- `main` is protected: pull requests, `test`, and `release-check` are required; force pushes and branch deletion are disabled.
- CI, Release Check, and CodeQL passed on PR #35. OpenSSF Scorecard exposed an invalid workflow-level write permission; the job-scoped fix is in PR #35 and still needs a green run on `main`.
- The `v0.1.0-alpha` tag and GitHub release do not exist.
- PyPI is explicitly deferred for `0.1.0-alpha`; this alpha is source-install only.
- External embedding providers and broader language extraction are future work.
- Federation remains design-only until alpha release gates are green.
## Postflight — 2026-07-04T04:54:53.734060+00:00

Task: make AMO the repo-native memory and graph operating layer

Summary: Stabilized runtime validation and config, integrated foundation branches, added graph contract validation and levels, Python structure extraction, standard exports, collision-safe Obsidian notes, full agent profiles, deterministic benchmark, and safe evolve.
## Postflight — 2026-07-05T05:05:38.264353+00:00

Task: implement staged deterministic optimizable parameters

Summary: Added typed parameter search spaces, deterministic seeded sweeps, normalized evidence-aware objectives, evolutionary trial reports, safe-only promotion, and parameter-driven context ranking.
## Postflight — 2026-07-05T08:13:51.889057+00:00

Task: test postflight

Summary: validated run history

Outcome: completed
Changed files: amo/core/postflight.py
## Postflight — 2026-07-05T09:33:20.452412+00:00

Task: sync project state after operating layer

Summary: Updated canonical state, README, changelog, scorecard, roadmap, release process, release notes, MCP and adapter docs after verifying the implemented operating layer; completed release smoke coverage and the sample Obsidian vault.

Outcome: completed
Changed files: .ai/manifest.yaml, .ai/state.md, .ai/tasks.md, .ai/decisions.md, .ai/tests.md, README.md, CHANGELOG.md, docs/10-10-scorecard.md, docs/roadmap.md, docs/release-process.md, docs/release-notes-0.1.0-alpha.md, docs/mcp.md, docs/adapters.md, .github/workflows/release-check.yml, .github/workflows/codeql.yml, pyproject.toml, amo/__init__.py, amo/mcp/server.py, tests/test_cli_smoke.py, tests/test_example_fixtures.py, examples/obsidian-graph-vault/Graph/Views/Groups.md
## Postflight — 2026-07-05T09:34:47.727544+00:00

Task: final 0.1.0-alpha release readiness validation

Summary: Completed the exact local release path on the reconciled tree: lint, 127 tests, lifecycle commands, six graph outputs including native JSON, embeddings, truth-aware benchmark, optimizer suggest/check/plan, deterministic 10-trial parameter sweep, strict validation, and status all passed.

Outcome: completed
Changed files: .ai/manifest.yaml, .ai/state.md, .ai/tasks.md, .ai/decisions.md, .ai/tests.md, .ai/graph.md, .ai/evolution, README.md, CHANGELOG.md, docs/10-10-scorecard.md, docs/roadmap.md, docs/release-process.md, docs/release-notes-0.1.0-alpha.md, docs/mcp.md, docs/adapters.md, .gitignore
## Postflight — 2026-07-05T09:37:03.845960+00:00

Task: complete executable benchmark output contract

Summary: Added deterministic benchmark Markdown output beside JSON, documented it, and covered unscored rendering in tests.

Outcome: completed
Changed files: amo/core/benchmark.py, tests/test_benchmark_evolve.py, docs/benchmark.md
## Postflight — 2026-07-05T09:39:59.485097+00:00

Task: fix clean-runner release-check benchmark scope

Summary: Added a root self-benchmark before optimizer checks so a clean GitHub runner has the evidence those checks require; synchronized release documentation and canonical test commands.

Outcome: completed
Changed files: .github/workflows/release-check.yml, README.md, docs/release-process.md, docs/release-notes-0.1.0-alpha.md, .ai/tests.md
## Postflight — 2026-07-05T09:43:41.370910+00:00

Task: record final GitHub security gate state

Summary: Recorded that CI and Release Check pass on PR #35 while CodeQL remains blocked because code scanning is disabled for the private repository and OpenSSF Scorecard remains blocked by GitHub integration access.

Outcome: completed
Changed files: .ai/state.md, .ai/tests.md
## Postflight — 2026-07-05T10:05:51.670235+00:00

Task: release readiness

Summary: Added direct checked-in JSON Schema artifact validation with valid and invalid fixtures; removed graph-neighborhood pollution from filesystem and generated-graph hubs; made benchmark selection evidence scoped and reproducibly achieved precision 1.0, recall 1.0, and zero prohibited inclusions; completed 131 tests and the full release and package path.

Outcome: completed
Changed files: amo/validators/json_schema.py, amo/core/validate.py, amo/core/graph.py, amo/core/benchmark.py, amo/context/graph_neighborhood.py, amo/context/ranking.py, tests/test_schema_artifact.py, tests/test_benchmark_evolve.py, docs/schema-contract.md, docs/benchmark.md
## Postflight — 2026-07-05T10:09:15.526111+00:00

Task: public alpha GitHub gates

Summary: Verified public visibility and protected main with PR, test, and release-check requirements; disabled force pushes and deletion; obtained green CodeQL on PR 35; fixed Scorecard workflow permission scope; explicitly deferred PyPI and documented source-install-only alpha distribution.

Outcome: completed
Changed files: .github/workflows/scorecard.yml, README.md, CHANGELOG.md, docs/release-notes-0.1.0-alpha.md, docs/release-process.md, docs/10-10-scorecard.md, docs/roadmap.md, .ai/state.md, .ai/tasks.md
