from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from amo.io import write_json, write_text


def slugify(task: str, limit: int = 40) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", task.lower()).strip("-")
    return slug[:limit].rstrip("-") or "run"


def write_run_history(
    repo: Path,
    task: str,
    summary: str,
    outcome: str,
    validation: str,
    changed_files: list[str],
    decision: str,
) -> tuple[Path, Path]:
    """Write a durable run note and a machine-readable mirror."""
    repo = repo.resolve()
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%H%M%S")
    slug = slugify(task)
    note_path = repo / ".ai" / "runs" / now.strftime("%Y-%m-%d") / f"{stamp}-{slug}.md"
    lines = [
        f"# Run — {task}",
        "",
        f"Timestamp: {now.isoformat()}",
        f"Outcome: {outcome}",
        "",
        "## Summary",
        "",
        summary,
    ]
    if validation:
        lines.extend(["", "## Validation", "", validation])
    if changed_files:
        lines.extend(["", "## Changed files", ""])
        lines.extend(f"- `{path}`" for path in changed_files)
    if decision:
        lines.extend(["", "## Decision", "", decision])
    write_text(note_path, "\n".join(lines) + "\n")

    mirror_path = repo / ".ai" / "machine" / "run_history" / f"{now.strftime('%Y%m%dT%H%M%S')}-{slug}.json"
    write_json(
        mirror_path,
        {
            "timestamp": now.isoformat(),
            "task": task,
            "summary": summary,
            "outcome": outcome,
            "validation": validation or None,
            "changed_files": changed_files,
            "decision": decision or None,
            "note": str(note_path.relative_to(repo).as_posix()),
        },
    )
    return note_path, mirror_path
