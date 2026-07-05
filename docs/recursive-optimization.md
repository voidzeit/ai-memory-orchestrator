# Recursive Optimization

`amo optimize` is AMO inspecting its own memory quality. It is deliberately boring:
deterministic heuristics over existing artifacts, no LLM, no autofix, no background jobs.
It proposes; humans (or supervised agents) apply.

## Commands

```bash
amo optimize suggest   # collect findings, write .ai/evolution/cycle-N.json + findings.md + metrics.json
amo optimize check     # exit 1 when high/medium findings require action
amo optimize plan      # write a prioritized propose-only plan to .ai/evolution/plan.md
```

`amo optimize params ...` is the sibling layer for numeric parameter tuning; see
[optimizable-parameters](optimizable-parameters.md).

## Signals

| Layer | Signal | Severity |
| --- | --- | --- |
| graph | `edge_references_missing_node` | high |
| graph | `duplicate_graph_edges`, `missing_symbol_nodes`, `graph_missing` | medium |
| graph | `orphan_nodes`, `missing_test_edges` | low |
| context | `missing_context_pack`, `context_pack_over_budget` | medium |
| context | `missing_validation_commands` | low |
| memory | `missing_canonical_memory` | high |
| memory | `empty_decisions`, `empty_tests` | medium |
| benchmark | `benchmark_missing`, `low_token_reduction` | medium |
| benchmark | `benchmark_unscored_precision_recall` | low |
| runtime | `runtime_not_ignored`, `runtime_tracked`, `runtime_leak_to_machine_or_packs` | high |
| runtime | `runtime_unknown_file` | low |
| adapter | `missing_agent_adapter_output` | low |

Every finding carries `id`, `severity`, `layer`, `message`, `evidence`, `recommendation`,
and an estimated `impact` on objective metrics. `stale_tasks` is intentionally not
implemented yet: a wall-clock staleness heuristic would make cycles non-reproducible.

## Guarantees

- Findings come only from files that already exist (`graph.json`, `validation.json`,
  `benchmark.json`, packs, canonical memory, runtime state).
- `suggest` writes only under `.ai/evolution/` and appends one evidence-ledger entry.
- `check` writes nothing; it is safe for CI gates that tolerate a non-zero exit.
- The optimizer never edits source code, canonical memory, or configuration.
