# AMO Parameter Optimization Report

Classification: **evolutionary/derived**

Completed 10 deterministic trials. Trial 6 won with score `3.983`.

## Why it won

- `graph_truthfulness`: 1.0
- `validation_confidence`: 1.0
- `memory_durability`: 1.0
- `interoperability`: 1.0
- `token_cost`: 0.017000000000000015
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
- `context.stale_penalty`: `1.7015401544355067`
- `context.large_file_penalty`: `2.1537428121569278`
- `graph.seed_top_k`: `14`
- `graph.max_hops`: `4`
- `graph.distance_decay`: `0.39563190106066426`
- `graph.authority_boost`: `2.7436427692216308`
- `graph.dedup_edges`: `False`
- `benchmark.min_token_reduction`: `0.14287159044206266`
- `benchmark.min_precision`: `0.1396303195255063`
- `benchmark.min_recall`: `0.7449889820916066`
- `benchmark.required_truth`: `True`
- `optimizer.max_trials`: `270`
- `optimizer.seed`: `1840109255`
- `optimizer.min_improvement`: `0.897822883602477`
