# Run — release readiness

Timestamp: 2026-07-05T10:05:51.673236+00:00
Outcome: completed

## Summary

Added direct checked-in JSON Schema artifact validation with valid and invalid fixtures; removed graph-neighborhood pollution from filesystem and generated-graph hubs; made benchmark selection evidence scoped and reproducibly achieved precision 1.0, recall 1.0, and zero prohibited inclusions; completed 131 tests and the full release and package path.

## Validation

ruff green; 131 tests passed; all release commands exited 0; strict validation green; benchmark precision 1.0 recall 1.0 violations 0; build and twine check passed

## Changed files

- `amo/validators/json_schema.py`
- `amo/core/validate.py`
- `amo/core/graph.py`
- `amo/core/benchmark.py`
- `amo/context/graph_neighborhood.py`
- `amo/context/ranking.py`
- `tests/test_schema_artifact.py`
- `tests/test_benchmark_evolve.py`
- `docs/schema-contract.md`
- `docs/benchmark.md`
