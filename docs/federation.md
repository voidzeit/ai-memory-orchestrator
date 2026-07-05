# Federation Layer — Design

**Status: design only.** Nothing in this document is implemented. Federation must not
be built until single-repo AMO is mature: benchmark evidence, the recursive optimizer,
and graph intelligence all need to be stable first, because federation multiplies every
weakness they still have.

## Problem

Organizations do not have one repository. A task like "migrate auth across services"
spans an API service, client SDKs, and infrastructure. Single-repo AMO can compile
excellent context for each repo in isolation but cannot answer:

- Which repositories does this change touch?
- Which downstream services break if `packages/api/auth.py` changes?
- Which decisions made in one repo constrain another?

## Model

Each repository keeps its own sovereign AMO memory. Federation is a read-mostly merge
layer above them:

```txt
RepoGraphᵢ = AMO(repoᵢ)

FederatedGraph =
  merge(
    RepoGraph₁,
    RepoGraph₂,
    ...,
    cross_repo_dependencies,   # package imports, API contracts, event schemas
    shared_decisions,          # decisions declared as org-wide
    shared_agents,             # agent profiles reused across repos
    shared_owners              # ownership and review boundaries
  )
```

Node ids gain a repo namespace (`repo-name:file:path`) so per-repo graphs merge without
collisions — the same collision-safety rule the Obsidian exporter already follows.

## Planned modules

```txt
amo/federation/
  registry.py   # which repos belong to the federation; local paths or remotes
  merge.py      # namespace + merge RepoGraphs; detect cross-repo edges
  context.py    # federated context packs: per-repo sections, one shared truth header
  impact.py     # reverse-dependency impact: file -> affected repos/files/tests
```

## Planned commands

```bash
amo federation init
amo federation scan
amo federation graph build
amo federation context --task "migrate auth across services"
amo federation impact --file packages/api/auth.py
```

## Authority and evidence rules

- A repo's own memory always outranks federated claims about that repo.
- Cross-repo edges are **derived** evidence: they carry the extractor's authority
  (≤ 0.8), never canonical authority.
- The federated graph is a cache; if it disagrees with any member repo's graph, the
  member repo wins and the federated graph is stale.
- Every federated build appends to each member's evidence ledger.
- Federated context packs must label which repo each unit came from; agents must not
  mutate memory in a repo they were not invoked in.

## Preconditions before implementation

1. Benchmark suite with ground-truth fixtures for at least two multi-repo tasks.
2. Optimizer signals extended with federation-layer checks (stale member graphs,
   namespace collisions, orphan cross-repo edges).
3. A tested contract for cross-repo dependency extraction (Python imports and package
   manifests first).
4. MCP resources for federated views, guarded by the same read-only defaults.

Until those exist, `amo federation ...` should not appear in the CLI at all — a
documented design is a promise we can keep; a stub command is a promise we cannot.
