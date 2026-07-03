# Contributing

Thanks for helping improve AI Memory Orchestrator.

## Development setup

```bash
git clone https://github.com/voidzeit/ai-memory-orchestrator.git
cd ai-memory-orchestrator
pip install -e '.[dev]'
```

## Validation

Before opening a pull request, run:

```bash
ruff check .
pytest
amo scan
amo graph build
amo validate --strict
amo status
```

## Branching

Use feature branches and pull requests. Do not push directly to `main` unless you are performing a repository administration task.

## Memory rules

AMO dogfoods its own memory model.

When your change affects project state, update:

- `.ai/state.md`
- `.ai/tasks.md`
- `.ai/decisions.md` when a durable decision is made
- `.ai/tests.md` when validation changes

Do not commit `.ai/runtime/`.

## Pull request checklist

- [ ] Change is scoped and intentional.
- [ ] Tests or docs were updated when needed.
- [ ] AMO memory was updated when project state changed.
- [ ] No secrets or local machine paths were committed.
