# Quickstart

AMO is a Git-native memory compiler for AI coding agents.

```bash
pip install ai-memory-orchestrator
cd your-repo
amo init
amo scan
amo context --task "fix failing tests"
amo validate
```

Serve the graph UI:

```bash
amo graph build
amo server --host 127.0.0.1 --port 8787
```

LAN access:

```bash
amo server --host 0.0.0.0 --port 8787 --token
```
