from __future__ import annotations

import subprocess
from pathlib import Path


ALLOWED_RUNTIME_FILES = {
    ".ai/runtime/last_context.md",
    ".ai/runtime/last_postflight.md",
    ".ai/runtime/session_handoff.md",
    ".ai/runtime/postflight.lock",
}
ALLOWED_RUNTIME_PREFIXES = (".ai/runtime/backups/",)
RUNTIME_ARTIFACT_NAMES = {Path(path).name for path in ALLOWED_RUNTIME_FILES}


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None


def _is_git_repo(repo: Path) -> bool:
    result = _run_git(repo, "rev-parse", "--is-inside-work-tree")
    return result is not None and result.returncode == 0 and result.stdout.strip() == "true"


def is_git_ignored(repo: Path, relative_path: str) -> bool:
    """Return whether Git ignores a repository-relative path."""
    result = _run_git(repo, "check-ignore", "--quiet", "--", relative_path)
    return result is not None and result.returncode == 0


def is_git_tracked(repo: Path, relative_path: str) -> bool:
    """Return whether a repository-relative path is tracked by Git."""
    result = _run_git(repo, "ls-files", "--error-unmatch", "--", relative_path)
    return result is not None and result.returncode == 0


def check_runtime_pollution(repo: Path) -> list[str]:
    runtime = repo / ".ai" / "runtime"
    if not runtime.exists():
        return []

    warnings: list[str] = []
    git_repo = _is_git_repo(repo)
    if git_repo and not is_git_ignored(repo, ".ai/runtime/"):
        warnings.append("`.ai/runtime/` is not ignored by Git.")

    for path in sorted(runtime.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        relative = path.relative_to(repo).as_posix()
        if git_repo and is_git_tracked(repo, relative):
            warnings.append(f"Runtime file is tracked by Git: `{relative}`.")
        if relative not in ALLOWED_RUNTIME_FILES and not relative.startswith(ALLOWED_RUNTIME_PREFIXES):
            warnings.append(f"Unexpected runtime file: `{relative}`.")

    for directory in (repo / ".ai" / "machine", repo / ".ai" / "packs"):
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.name in RUNTIME_ARTIFACT_NAMES:
                relative = path.relative_to(repo).as_posix()
                warnings.append(f"Runtime artifact leaked into derived output: `{relative}`.")

    return warnings
