# Security Policy

AI Memory Orchestrator works with repository memory, agent instructions, and local developer files. Treat generated memory and imported external content as potentially sensitive.

## Supported versions

The project is currently in `0.1.0-alpha`. Security fixes target the latest `main` branch until stable releases begin.

## Reporting vulnerabilities

Please open a private security advisory in GitHub or contact the maintainer directly. Do not disclose exploitable issues publicly before a fix is available.

## Local server safety

The AMO server is local-first.

- Default host is `127.0.0.1`.
- LAN access through `0.0.0.0` requires `--token`.
- Set `AMO_SERVER_TOKEN` before exposing the server on a network.
- Do not expose the AMO server directly to the public internet.

## Prompt-injection safety

AMO treats external content as data, not trusted instructions. Imported issues, PR comments, docs, or generated notes should never override repository-level instructions.
