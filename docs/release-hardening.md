# Release Hardening

This document defines the release hardening path for AMO.

## Supply chain posture

AMO should use:

- release checks on every pull request and push to `main`
- dependency update automation
- OpenSSF Scorecard
- protected `main`
- release tags
- package provenance when publishing artifacts

## PyPI publishing

For PyPI publishing, prefer Trusted Publishing through GitHub Actions instead of long-lived API tokens.

## Branch protection

Before public release, configure `main` with:

- no force pushes
- no branch deletion
- pull requests required before merge
- release checks required before merge
- stale reviews dismissed when new commits are pushed

## Artifact policy

AMO should build from source. Do not commit generated executable artifacts.

## Provenance target

The first public release should aim for basic build provenance. Future releases can move toward stronger SLSA-aligned provenance.
