# Support

## Where to get help

- **Bugs and feature requests** — open a
  [GitHub issue](https://github.com/voidzeit/ai-memory-orchestrator/issues) using the
  provided templates.
- **Usage questions** — start with the [quickstart](docs/quickstart.md), the
  [architecture overview](docs/architecture.md), and the docs directory; open a
  discussion or issue if the docs do not answer your question.
- **Security reports** — never open a public issue; follow [SECURITY.md](SECURITY.md).

## What to include

Please include your AMO version (`pip show ai-memory-orchestrator`), operating system,
the exact command you ran, and the output of `amo status` and `amo validate` when
relevant. `.ai/machine/validation.json` and `.ai/evidence/ledger.jsonl` excerpts make
most problems reproducible.

## Status of the project

AMO is in public alpha. Interfaces can change between minor versions; the memory
layout under `.ai/` is the most stable contract.
