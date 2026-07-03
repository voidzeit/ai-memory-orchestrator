# Tests

## Required commands

- ruff check .
- pytest
- amo scan
- amo preflight --task "release readiness" --profile quick
- amo handoff --task "release readiness" --summary "release validation"
- amo graph build
- amo graph export --format neo4j
- amo embeddings build
- amo validate --strict
- amo status

## Current test coverage

- tests/test_init.py
- tests/test_scan.py
- tests/test_context.py
- tests/test_validate.py
- tests/test_adapters.py
- tests/test_status.py
- tests/test_graph_exports.py
- tests/test_embeddings.py
- tests/test_session_pack.py

## CI

The repository includes GitHub Actions workflows for linting, tests, and release checks.
