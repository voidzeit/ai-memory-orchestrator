# The Repository Memory Manifesto

AI coding agents are becoming part of everyday software development, but repository context is still unmanaged.

Every team is inventing its own memory layer:

- `AGENTS.md`
- `CLAUDE.md`
- Cursor rules
- Cline Memory Bank
- project notes
- chat transcripts
- copied prompts
- stale architecture docs

These fragments drift. They duplicate each other. They contradict the code. They waste tokens. Most importantly, they make agents act confidently with incomplete context.

AMO exists to make repository memory explicit, durable, validated, and portable.

## Thesis

```txt
AI agents do not need bigger context windows first.
They need better memory discipline.
```

## Principles

### 1. The repository is reality

Source code and Git history are the highest authority.

### 2. Memory must be canonical

A project needs one clear memory source of truth. In AMO, that is `.ai/`.

### 3. Context packs are compiled artifacts

Agents should not read the whole repository by default. They should receive the smallest sufficient context for the task.

### 4. Every summary needs an expansion path

Compressed context must always point back to the file, decision, test, or graph node that can expand it.

### 5. Runtime is not memory

Caches, logs, temporary notes, and session files must not become canonical truth.

### 6. Adapters are not truth

`AGENTS.md`, `CLAUDE.md`, Cursor rules, Cline Memory Bank, OpenCode instructions, and Obsidian notes are adapters. `.ai/` remains the source of truth.

### 7. Verification beats volume

More context is not intelligence. Verified context is intelligence.

## Goal

AMO aims to make every repository agent-ready:

```txt
canonical memory + machine indexes + project graph + validators + context compiler
```

That is the missing layer between source code and AI coding agents.
