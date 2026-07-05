from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DEFAULT_STALE_SECONDS = 600.0


class LockHeldError(RuntimeError):
    """Another process holds the canonical-memory lock."""


def lock_path(repo: Path) -> Path:
    return repo.resolve() / ".ai" / "runtime" / "postflight.lock"


def acquire_lock(repo: Path, stale_after: float = DEFAULT_STALE_SECONDS) -> Path:
    path = lock_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"pid": os.getpid(), "acquired_at": time.time()})
    try:
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        if not _is_stale(path, stale_after):
            raise LockHeldError(
                f"Canonical memory is locked by another process: {path}"
            ) from None
        path.unlink(missing_ok=True)
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(handle, "w", encoding="utf-8") as fh:
        fh.write(payload)
    return path


def release_lock(repo: Path) -> None:
    lock_path(repo).unlink(missing_ok=True)


def _is_stale(path: Path, stale_after: float) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        acquired = float(data.get("acquired_at", 0.0))
    except (OSError, ValueError):
        return True
    return (time.time() - acquired) > stale_after


@contextmanager
def memory_lock(repo: Path, stale_after: float = DEFAULT_STALE_SECONDS) -> Iterator[Path]:
    path = acquire_lock(repo, stale_after=stale_after)
    try:
        yield path
    finally:
        release_lock(repo)
