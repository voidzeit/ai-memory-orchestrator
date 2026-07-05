# Tests

## Required commands

- ruff check .
- pytest
- amo scan
- amo preflight --task "release readiness" --profile quick
- amo handoff --task "release readiness" --summary "release validation"
- amo graph build
- amo graph export --format json
- amo graph export --format jsonld
- amo graph export --format graphml
- amo graph export --format gexf
- amo graph export --format neo4j
- amo embeddings build
- amo benchmark examples/agent-debug-session --task "fix failing tests"
- amo benchmark . --task "release readiness"
- amo optimize suggest
- amo optimize check
- amo optimize plan
- amo optimize params suggest
- amo optimize params sweep --trials 10 --seed 42
- amo optimize params best
- amo validate --strict
- amo status

## Current test coverage

- The test suite covers lifecycle/config/runtime validation, adapters and CLI registration,
  context and graph neighborhoods, hierarchical graph/code structure, all exporters,
  embeddings, benchmark truth, evidence ledger, optimizer/parameter sweeps, MCP,
  robust postflight, organism server/UI, and example fixtures.

## CI

CI and Release Check passed on `main` at commit `db11b3e` and on PR #35. CodeQL
cannot upload because code scanning is not enabled for the private repository; OpenSSF
Scorecard fails with a GitHub integration-access error. Both need green runs before tagging.

## Validation — 2026-07-05T08:13:51.889057+00:00

pytest passed

## Validation — 2026-07-05T09:33:20.452412+00:00

ruff passed; 127 pytest tests passed; package build and twine check passed; full AMO release path passed after one transient Windows sweep read was rerun successfully

## Validation — 2026-07-05T09:34:47.727544+00:00

All 21 required release commands exited 0; package build produced 0.1.0a1 sdist and wheel; twine check passed both distributions.

## Validation — 2026-07-05T09:37:03.845960+00:00

ruff passed; 127 tests passed; benchmark smoke passed; package build and twine check passed.

## Validation — 2026-07-05T09:39:59.485097+00:00

ruff passed; 127 tests passed; root benchmark, optimizer suggest/check/plan, and strict validation passed.

## Validation — 2026-07-05T09:43:41.370910+00:00

PR #35 CI success; Release Check success; CodeQL failed during SARIF upload with code scanning not enabled.

## Validation — 2026-07-05T10:05:51.670235+00:00

ruff green; 131 tests passed; all release commands exited 0; strict validation green; benchmark precision 1.0 recall 1.0 violations 0; build and twine check passed
