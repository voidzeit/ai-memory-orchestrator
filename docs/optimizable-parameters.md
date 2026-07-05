# Optimizable Parameters

AMO exposes context, graph, benchmark, and optimizer heuristics in
`.amo/optimization/search_space.yaml`. Each declaration has a type, default, safety flag,
description, and either numeric bounds or categorical choices. Boolean parameters require no
bounds. This format is the stable internal contract for future optimization adapters.

## Why the first optimizer is dependency-free

The initial layer deliberately does not depend on Optuna, Ray Tune, Weights & Biases, an LLM, or
background workers. AMO needs a small, inspectable measurement contract before adding orchestration
frameworks. The built-in seeded sampler is deterministic and samples only declared values.

Use `amo optimize params suggest` to validate and inspect the space. Use
`amo optimize params sweep --trials 20 --seed 42` to run it. Trial one evaluates all defaults; later
trials use Python's seeded pseudo-random sampler. A sweep never changes `.amo.yaml`.

## Objective

`.amo/optimization/objective.yaml` weights normalized values from zero to one. The score rewards
useful context per token, graph truthfulness, validation confidence, memory durability, and
interoperability. It subtracts token cost, stale context, duplicated context, wrong-file selection,
and graph drift.

AMO scores only observed metrics. Selection precision, recall, useful context, and wrong-file
selection remain `unscored` when fixture ground truth is absent. It never substitutes a guessed
value. `amo optimize params best` displays the winner, score, rationale, and unscored metrics.

## Artifacts and safety

Generated output is classified as **evolutionary/derived** and lives under `.ai/evolution/`:

- `trials.jsonl` contains one deterministic record per trial.
- `best_params.yaml` contains the winning configuration.
- `parameter-report.md` explains the result and missing evidence.

`amo optimize params apply-safe --confirm` is the only promotion command. It refuses to run without
a best artifact, confirmation, and non-red strict validation. It writes only parameters marked
`safe_to_apply: true`, writes only `.amo.yaml`, lists exact changed keys, and never edits source.

The ranking engine currently consumes `context.max_units`, `context.relevance_weight`,
`context.authority_weight`, `context.token_cost_weight`, and `context.duplicate_penalty`. Other
declarations are visible as disconnected heuristics so their staged integration is explicit.

## Future adapters

Optuna, Ray Tune, W&B, grid search, or remote experiment trackers can later adapt to the same search
space, trial, objective, and promotion contracts. They must preserve AMO's ground-truth rules and
explicit safe-apply boundary.
