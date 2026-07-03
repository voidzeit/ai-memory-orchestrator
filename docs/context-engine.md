# Context Engine

AMO optimizes for maximum useful context with minimum token cost.

```txt
ContextPack = Compress(Select(Rank(Retrieve(repo, memory, task))))
```

## Context hierarchy

1. Manifest
2. Current state
3. Task context pack
4. Graph neighborhood
5. Relevant snippets
6. Full files only when necessary
7. Raw logs/history only on demand

Every compressed context unit must include an expansion pointer.
