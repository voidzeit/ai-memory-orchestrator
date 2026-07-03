# Problem: Context Rot

Context rot is stale, duplicated, incomplete, or contradictory repository knowledge in AI coding workflows.

It is the AI-era version of documentation drift.

## Symptoms

- The coding assistant reads irrelevant files.
- The assistant misses the current architecture decision.
- The assistant trusts old notes over source code.
- The assistant cannot identify the right test command.
- Different tools use different memory files and drift apart.

## Why it is getting worse

Teams are rapidly adding AI coding tools, but repository context is still managed manually.

A single repo may now contain many context surfaces: instructions, editor rules, memory banks, README files, architecture notes, issue threads, pull request comments, and local notes.

Each surface can contain useful information. Each surface can also become stale.

## The AMO answer

AMO separates truth from views:

```txt
.ai/         = canonical memory
machine/     = derived indexes
packs/       = compiled task context
runtime/     = disposable state
adapters     = generated views for tools
```

This gives coding tools one verified place to start while still supporting different editor and agent workflows.
