# Evidence Ledger

AMO distinguishes observed evidence, derived evidence, compiled artifacts, and declared
memory. The ledger at `.ai/evidence/ledger.jsonl` makes that distinction auditable: every
lifecycle command appends one JSON line describing what ran, what it produced, and how much
authority the result carries.

## Entry format

```json
{
  "timestamp": "2026-07-05T00:00:00+00:00",
  "kind": "validation",
  "source": "amo validate --strict",
  "result": "green",
  "commit": "abc123",
  "authority": 0.9,
  "artifacts": [".ai/machine/validation.json"],
  "limitations": ["does not prove production readiness"]
}
```

`commit` is resolved from `.git/HEAD` when the repository is a Git checkout and is `null`
otherwise. `kind` must be one of: `scan`, `graph_build`, `validation`, `benchmark`,
`context_pack`, `handoff`, `postflight`, `optimizer_trial`, `adapter_export`,
`mcp_tool_invocation`.

## Recording commands

| Command | Kind | Authority |
| --- | --- | --- |
| `amo scan` | `scan` | 0.9 (observed) |
| `amo validate` | `validation` | 0.9 (observed) |
| `amo benchmark` | `benchmark` | 0.9 (observed) |
| `amo graph build` | `graph_build` | 0.8 (derived) |
| `amo optimize params sweep` | `optimizer_trial` | 0.8 (derived) |
| `amo context` / `amo preflight` | `context_pack` | 0.6 (compiled) |
| `amo handoff` | `handoff` | 0.6 (compiled) |
| `amo export` | `adapter_export` | 0.6 (compiled) |
| `amo postflight` | `postflight` | 0.5 (declared) |

Postflight and handoff summaries are agent-declared synthetic evidence: they enter the
ledger with lower authority and a limitation note until corroborated by validation runs.

## Safety rules

- The ledger is append-only. Entries are never rewritten or deleted by AMO.
- `.ai/runtime/` contents are disposable and never recorded as durable truth.
- Ledger evidence never outranks source code: if they disagree, the code wins.
- `ledger.jsonl` is machine-local operational history and is left untracked, like
  `.ai/machine/`; only `README.md` in the same directory is committed.
