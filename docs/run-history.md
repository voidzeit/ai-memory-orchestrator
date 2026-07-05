# Postflight and Run History

`amo postflight` is the only command that mutates canonical memory, so it is built to be
safe under concurrency and auditable after the fact.

## What a postflight does

1. Acquires `.ai/runtime/postflight.lock` (fails fast if held; replaces it when stale —
   default 10 minutes).
2. Backs up canonical memory into `.ai/runtime/backups/<timestamp>/` (last 5 kept).
3. Appends the postflight note to `.ai/tasks.md` and `.ai/state.md`.
4. Appends to `.ai/decisions.md` **only** when `--decision` is given explicitly.
5. Appends to `.ai/tests.md` only when `--validation` is given.
6. Writes a durable run note to `.ai/runs/YYYY-MM-DD/<time>-<slug>.md` and a
   machine-readable mirror to `.ai/machine/run_history/<timestamp>-<slug>.json`.
7. Writes `.ai/runtime/last_postflight.md` and appends an evidence-ledger entry.

## CLI

```bash
amo postflight \
  --task "fix failing auth tests" \
  --summary "normalized password comparison" \
  --outcome completed \
  --validation "pytest passed" \
  --changed-files "app/auth.py,tests/test_auth.py" \
  --decision "Auth comparisons must be None-safe."
```

## Classification

- `.ai/runs/` notes are durable history — commit them.
- `.ai/machine/run_history/` mirrors are derived — regenerable, left untracked.
- `.ai/runtime/backups/` are disposable safety copies — never durable truth.
