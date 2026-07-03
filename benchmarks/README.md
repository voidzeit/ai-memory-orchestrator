# AMO Benchmarks

AMO benchmarks are designed to measure whether repository memory improves context quality for AI coding workflows.

## Current benchmark dimensions

- token reduction
- file selection accuracy
- test command accuracy
- drift detection
- expansion quality

## Manual alpha benchmark

1. Choose a task.
2. Define expected relevant files.
3. Run `amo scan`.
4. Run `amo preflight --task "<task>"`.
5. Compare `.ai/packs/quick.md` against the expected context.

## Future benchmark command

```bash
amo benchmark examples/agent-debug-session --task "fix failing auth tests"
```
