# Demo Script

This script shows the public alpha story for AMO.

## Goal

Show how a repository becomes agent-ready in less than a minute.

## Script

```bash
amo init
amo scan
amo preflight --task "fix failing tests"
amo graph build
amo validate
amo status
```

## What to show

1. `.ai/` appears as canonical project memory.
2. `.ai/machine/context_units.json` appears as machine context.
3. `.ai/packs/quick.md` appears as task context.
4. `amo status` shows memory health.
5. The server can show graph JSON locally.

## Message

AMO gives every coding agent a verified place to start.
