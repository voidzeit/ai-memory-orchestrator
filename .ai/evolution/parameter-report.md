# AMO Parameter Optimization Report

Classification: **evolutionary/derived**

Completed 10 deterministic trials. Trial 6 won with score `3.986`.

## Why it won

- `graph_truthfulness`: 1.0
- `validation_confidence`: 1.0
- `memory_durability`: 1.0
- `interoperability`: 1.0
- `token_cost`: 0.014000000000000012
- `stale_context`: 0.0
- `graph_drift`: 0.0

## Unscored metrics

- `useful_context_per_token` (ground truth or evidence unavailable)
- `duplicated_context` (ground truth or evidence unavailable)
- `wrong_file_selection` (ground truth or evidence unavailable)
- `benchmark.file_selection_precision` (ground truth or evidence unavailable)
- `benchmark.file_selection_recall` (ground truth or evidence unavailable)

## Best parameters

- `context.max_units`: `7`
- `context.relevance_weight`: `4.025229003856071`
- `context.authority_weight`: `1.2034943610669868`
- `context.token_cost_weight`: `0.13237721042309447`
- `context.duplicate_penalty`: `2.739408372556635`
- `context.graph_weight`: `1.7015401544355067`
- `context.stale_penalty`: `2.1537428121569278`
- `context.large_file_penalty`: `0.6378796321624218`
- `graph.seed_top_k`: `32`
- `graph.max_hops`: `4`
- `graph.distance_decay`: `0.8846831538867025`
- `graph.authority_boost`: `1.9285556106012727`
- `graph.dedup_edges`: `False`
- `benchmark.min_token_reduction`: `0.26488016649805246`
- `benchmark.min_precision`: `0.24662750769398345`
- `benchmark.min_recall`: `0.5613681341631508`
- `benchmark.required_truth`: `False`
- `optimizer.max_trials`: `765`
- `optimizer.seed`: `1840109255`
- `optimizer.min_improvement`: `0.897822883602477`
