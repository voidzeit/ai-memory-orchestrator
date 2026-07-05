# Evolution Findings

Cycle 7. Deterministic signals only — no LLM, no autofix.

## Low

- `missing_test_edges` (graph): 80 Python files have no tested_by edge.
  - evidence: first: file:amo/__init__.py
  - recommendation: Add tests or map existing tests to their subjects.
- `benchmark_unscored_precision_recall` (benchmark): Benchmark precision/recall are unscored.
  - evidence: file_selection_precision or file_selection_recall is not numeric
  - recommendation: Add fixture ground truth (truth.json) and rerun `amo benchmark`.
