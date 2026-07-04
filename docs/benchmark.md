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

The command writes deterministic metrics to `.ai/machine/benchmark.json`. Precision, recall, test-command accuracy, and handoff quality are explicitly marked unscored when a fixture has no ground-truth annotations; AMO does not invent evidence.
