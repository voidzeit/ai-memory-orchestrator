# Run — fix clean-runner release-check benchmark scope

Timestamp: 2026-07-05T09:39:59.488096+00:00
Outcome: completed

## Summary

Added a root self-benchmark before optimizer checks so a clean GitHub runner has the evidence those checks require; synchronized release documentation and canonical test commands.

## Validation

ruff passed; 127 tests passed; root benchmark, optimizer suggest/check/plan, and strict validation passed.

## Changed files

- `.github/workflows/release-check.yml`
- `README.md`
- `docs/release-process.md`
- `docs/release-notes-0.1.0-alpha.md`
- `.ai/tests.md`
