# Agent Context Discipline

AMO treats context as a managed resource.

Modern AI coding workflows degrade when long chats become the working memory of the project. AMO keeps durable context in the repository instead.

## Core loop

```bash
amo scan
amo preflight --task "your task" --profile quick
```

The generated context pack is the agent entrypoint.

## Profiles

```txt
micro         focused edit or clarification
quick         default task context
debug         bug investigation
architecture  cross-module planning
handoff       restart or compaction boundary
full          broad review, use sparingly
```

## Degradation signals

Create a handoff when:

- the chat repeats resolved work
- the agent loses the test plan
- the agent edits outside scope
- the chat contains more process than evidence
- the prompt depends on copied summaries from older turns

## Handoff

```bash
amo handoff --task "your task" --summary "current state and next step"
```

This writes:

```txt
.ai/packs/handoff.md
.ai/runtime/session_handoff.md
```

Use `handoff.md` to restart the agent without carrying the old chat.

## Postflight

After the work:

```bash
amo postflight --task "your task" --summary "what changed"
amo validate
```

## Rule

Chat history is not source of truth. Reviewed repo memory is source of truth.
