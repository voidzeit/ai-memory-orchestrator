# Quickstart

AMO is a Git-native memory compiler for AI coding agents.

> Status: `0.1.0-alpha` is source-install only. PyPI publishing is intentionally deferred until a stable release.

## Install the alpha from source

```bash
git clone https://github.com/voidzeit/ai-memory-orchestrator.git
cd ai-memory-orchestrator
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

## Add AMO to a repository

From the repository you want to give persistent agent memory:

```bash
amo init
amo scan
amo context --task "fix failing tests"
amo validate
```

AMO creates canonical memory under `.ai/`, derived indexes under `.ai/machine/`, and task-specific context packs under `.ai/packs/`.

## Serve the graph UI

```bash
amo graph build
amo server --host 127.0.0.1 --port 8787
```

LAN access requires an explicit token:

```bash
export AMO_SERVER_TOKEN="change-me"
amo server --host 0.0.0.0 --port 8787 --token
```

## Future stable install

Once PyPI publishing is enabled for a stable release, installation will become:

```bash
pip install ai-memory-orchestrator
```
