# AMO and Obsidian

AMO and Obsidian solve different problems.

## AMO

AMO is the repository memory system.

It owns:

- canonical `.ai/` memory
- machine indexes
- context packs
- validation reports
- graph JSON
- adapter exports

AMO is optimized for AI coding agents and Git workflows.

## Obsidian

Obsidian is a rich human knowledge interface.

It is excellent for:

- visual exploration
- writing notes
- backlinks
- human review
- knowledge synthesis

## Relationship

```txt
AMO owns the memory.
Obsidian visualizes the memory.
Agents consume the memory.
Validators protect the memory.
```

## Is Obsidian richer?

For human navigation, yes. Obsidian has mature note-taking and graph exploration.

For agent governance, no. AMO has canonical truth, validation, task-specific context packs, and adapter exports.

## Best architecture

Use AMO as the source of truth and export to Obsidian when a human graph is useful.

```bash
amo obsidian sync
amo graph export --format obsidian
```

Obsidian should not become the canonical source of truth unless AMO explicitly imports reviewed changes.
