from __future__ import annotations

import json
from pathlib import Path

from amo.evidence.schema import EvidenceEntry

_README = """# Evidence Ledger

`ledger.jsonl` is an append-only provenance log. Every AMO command that observes,
derives, or compiles repository knowledge appends one JSON line describing what
ran, what it produced, and how much authority the result carries.

Authority bands:

- `0.9` observed evidence (scan, validation, benchmark)
- `0.8` derived evidence (graph build, optimizer trials)
- `0.6` compiled artifacts (context packs, handoffs, adapter exports)
- `0.5` declared memory updates (postflight summaries are agent-declared
  until corroborated by validation evidence)

Rules:

- The ledger is append-only; entries are never rewritten or deleted.
- `.ai/runtime/` contents are never durable truth and are not recorded here.
- If ledger evidence contradicts source code, source code wins.
"""


def ledger_path(repo: Path) -> Path:
    return repo.resolve() / ".ai" / "evidence" / "ledger.jsonl"


def record_evidence(
    repo: Path,
    kind: str,
    source: str,
    result: str,
    authority: float,
    artifacts: tuple[str, ...] = (),
    limitations: tuple[str, ...] = (),
) -> EvidenceEntry:
    entry = EvidenceEntry(
        kind=kind,
        source=source,
        result=result,
        authority=authority,
        commit=resolve_head_commit(repo),
        artifacts=artifacts,
        limitations=limitations,
    )
    path = ledger_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    readme = path.parent / "README.md"
    if not readme.exists():
        readme.write_text(_README, encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry.as_dict(), sort_keys=True) + "\n")
    return entry


def read_ledger(repo: Path) -> list[dict[str, object]]:
    path = ledger_path(repo)
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def resolve_head_commit(repo: Path) -> str | None:
    """Resolve the current commit from .git metadata without spawning git."""
    git_dir = repo.resolve() / ".git"
    try:
        head = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not head.startswith("ref: "):
        return head or None
    ref = head[len("ref: ") :]
    ref_file = git_dir / Path(ref)
    try:
        return ref_file.read_text(encoding="utf-8").strip() or None
    except OSError:
        pass
    try:
        packed = (git_dir / "packed-refs").read_text(encoding="utf-8")
    except OSError:
        return None
    for line in packed.splitlines():
        if line.endswith(ref) and not line.startswith("#"):
            return line.split(" ", 1)[0]
    return None
