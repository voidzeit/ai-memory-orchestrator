# Example: Agent Debug Session

This example describes the intended AMO workflow for a debugging task.

## Without AMO

The assistant must inspect the repository manually, infer current architecture, guess relevant files, and ask for test commands.

## With AMO

```bash
amo init
amo scan
amo preflight --task "fix failing auth tests"
```

The agent starts from `.ai/packs/quick.md`, which should include:

- current project truth
- relevant files
- relevant decisions
- known risks
- test commands
- expansion paths

## Intended outcome

The agent spends less context on discovery and more context on the actual change.

## Ground truth

`truth.json` declares which files matter for the task, the expected test command, and
what the context pack must (and must not) contain. `amo benchmark` uses it to score
file-selection precision/recall honestly instead of guessing:

```bash
amo benchmark examples/agent-debug-session --task "fix failing auth tests"
```
