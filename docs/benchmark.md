# Benchmark Plan

AMO should prove that repository memory can improve AI coding workflows.

This benchmark measures whether AMO can produce smaller, more relevant context packs than manual repository reading.

## Metrics

### Token reduction

Compare estimated tokens for full repository reading, selected files, and AMO context packs.

Goal for public alpha examples:

```txt
50% to 90% less context than naive full-repo reading
```

### File selection accuracy

For a task, define the expected relevant files and measure how many AMO selects.

```txt
precision = selected relevant files / selected files
recall    = selected relevant files / expected relevant files
```

### Test command accuracy

Check whether AMO includes the right validation command for the task.

### Drift detection

Create stale memory claims and verify whether validators warn about them.

### Expansion quality

Every compressed context unit should include a path that expands into the original source.

## Example task

```txt
Task: fix failing auth tests
Expected context:
- auth implementation file
- auth test file
- relevant decision note
- test command
- known risk
```

## Automation

```bash
amo benchmark examples/agent-debug-session --task "fix failing tests"
```

The command writes deterministic machine-readable metrics to `.ai/machine/benchmark.json` and a reviewable companion report to `.ai/machine/benchmark.md`. Precision, recall, test-command accuracy, and handoff quality are explicitly marked unscored when a fixture has no ground-truth annotations; AMO does not invent evidence.

## Ground truth

A fixture opts into scored metrics by providing `truth.json` at its root:

```json
{
  "task": "fix failing auth tests",
  "relevant_files": ["app/auth.py", "tests/test_auth.py"],
  "expected_tests": ["pytest tests/test_auth.py"],
  "expected_context_sections": ["Current Truth", "Relevant Context Units", "Postflight"],
  "must_not_include": [".ai/runtime/last_context.md"]
}
```

With truth present, `amo benchmark` computes `file_selection_precision`,
`file_selection_recall`, `test_command_accuracy` (fraction of expected commands present in
the pack), `context_section_coverage`, and `must_not_include_violations`. Note that
precision counts selected task files outside `.ai/`; canonical and derived `.ai/` files are
excluded because canonical memory is rendered into every pack by contract. Unrelated source,
test, and documentation files still count as false positives. The report records
`evaluated_selected_files` so that this denominator is reviewable.
`handoff_quality` remains unscored; it needs a handoff-specific rubric.
