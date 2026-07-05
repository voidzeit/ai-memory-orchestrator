# Release Process

## Gates

Every release must pass the full `release-check` workflow, which runs:

```bash
ruff check .
pytest
amo scan
amo preflight --task "release readiness" --profile quick
amo handoff --task "release readiness" --summary "release validation"
amo graph build
amo graph export --format neo4j
amo graph export --format jsonld
amo graph export --format graphml
amo graph export --format gexf
amo embeddings build
amo benchmark examples/agent-debug-session --task "fix failing auth tests"
amo optimize suggest
amo validate --strict
amo status
```

Plus the security workflows: CodeQL analysis, OpenSSF Scorecard, and Dependabot
update PRs.

## Steps

1. Confirm `release-check` is green on `main`.
2. Update `CHANGELOG.md` and the release notes under `docs/`.
3. Bump `version` in `pyproject.toml`.
4. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z"` and push the tag.
5. Create a GitHub release from the tag; the `publish` workflow builds, runs
   `twine check`, and publishes to PyPI via trusted publishing.
   `workflow_dispatch` runs build and check only — it never publishes.

## Repository settings checklist

These are GitHub settings, not code; they must be configured manually in the
repository settings and are **not** guaranteed by anything in this tree:

- [ ] `main` branch protected; PRs required; force pushes and deletion disabled
- [ ] `release-check` required as a status check
- [ ] PyPI trusted publisher configured for the `publish` workflow
      (`pypi` environment)
- [ ] Repository visibility as intended

## Honesty rules

- Never claim a gate passed without running it.
- Benchmarks report `unscored` metrics as unscored — do not edit results by hand.
- The publish workflow must not be triggered while any release gate is red.
