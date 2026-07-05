# Tasks

## Immediate

- [ ] Review and merge the alpha-readiness reconciliation PR with green CI and Release Check.
- [ ] Make the repository public.
- [ ] Protect `main`, require PRs and `release-check`, and disable force pushes and branch deletion.
- [ ] Obtain green CodeQL and OpenSSF Scorecard runs on `main`.
- [ ] Configure or explicitly defer PyPI trusted publishing.
- [ ] Create `v0.1.0-alpha` only after all release gates are green.

## Next product work

- [ ] Deepen Python dependency extraction and define a language extractor interface.
- [ ] Add test-source linking and graph drift detection.
- [ ] Expand benchmark, MCP-client, onboarding, and Obsidian examples.
- [ ] Add semantic ranking as an optional derived enhancement.
- [ ] Keep federation design-only until alpha release gates are green.

## Done

- [x] Bootstrap MVP merged to `main`.
- [x] Add CLI commands for init, scan, context, preflight, postflight, validate, status, graph, server, export, and Obsidian sync.
- [x] Add basic adapters for AGENTS.md, Claude, Cursor, Cline, and OpenCode.
- [x] Add release hardening changes for public readiness.
- [x] Add hierarchical graph levels, Python structure extraction, and standard graph exports.
- [x] Add executable truth-aware benchmarks and evidence ledger integration.
- [x] Add propose-only optimization and deterministic optimizable parameter sweeps.
- [x] Add robust postflight locking, backups, run history, and structured outcomes.
- [x] Add MCP stdio resources/tools and the organism dashboard.
- [x] Add full adapter profiles, graph validation, release workflows, and community documents.
- [x] Add a reviewable sample Obsidian graph vault.
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
