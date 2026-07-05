# AMO Server

`amo server` serves the local organism UI: a dependency-light dashboard over the
repository's memory, graph, benchmark, findings, and evidence ledger.

Local only:

```bash
amo server --host 127.0.0.1 --port 8787
```

LAN access (requires `AMO_SERVER_TOKEN` and `--token`; clients pass `?token=` or the
`x-amo-token` header):

```bash
amo server --host 0.0.0.0 --port 8787 --token
```

## Views

- **Health** — validation status, graph size by level, finding counts, packs, adapters,
  ledger volume, latest benchmark.
- **Graph Explorer** — searchable node table (type, label, level, authority, source).
- **Context Flow** — compile a pack for a task and see per-unit selection reasons.
- **Benchmark** — latest metrics, honest about unscored values.
- **Findings** — latest optimizer cycle by severity.
- **Evidence Ledger** — most recent provenance entries.

## API

```txt
GET  /api/status      GET  /api/organism    GET  /api/graph
GET  /api/validation  GET  /api/benchmark   GET  /api/evolution
GET  /api/ledger
POST /api/context     POST /api/handoff     POST /api/postflight
```

GET endpoints are read-only. `POST /api/context` and `/api/handoff` write compiled
artifacts only. `POST /api/postflight` mutates canonical memory and therefore requires
`confirm: true` and a non-empty summary; it uses the same lock/backup/run-history path
as the CLI. There is no live WebSocket feed yet — views load on demand.
