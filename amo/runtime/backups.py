from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from amo.paths import CANONICAL_FILES

KEEP_BACKUPS = 5


def backup_canonical(repo: Path) -> Path:
    """Copy canonical memory into a timestamped runtime backup before mutation."""
    repo = repo.resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    destination = repo / ".ai" / "runtime" / "backups" / stamp
    destination.mkdir(parents=True, exist_ok=True)
    for name in CANONICAL_FILES:
        source = repo / ".ai" / name
        if source.exists():
            shutil.copy2(source, destination / name)
    _prune(destination.parent)
    return destination


def _prune(root: Path, keep: int = KEEP_BACKUPS) -> None:
    backups = sorted((item for item in root.iterdir() if item.is_dir()), key=lambda item: item.name)
    for stale in backups[:-keep]:
        shutil.rmtree(stale, ignore_errors=True)
