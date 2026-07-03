from pathlib import Path

from amo.index.artifacts import build_artifact_index
from amo.index.context_units import build_context_units
from amo.index.files import build_file_index
from amo.io import write_json
from amo.paths import ai_path, ensure_dirs

DEFAULT_EXCLUDES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ai/runtime",
}


def scan_repo(repo: Path) -> dict[str, int]:
    repo = repo.resolve()
    ensure_dirs(repo)
    files = build_file_index(repo, excludes=DEFAULT_EXCLUDES)
    artifacts = build_artifact_index(repo, files)
    units = build_context_units(repo, files)
    write_json(ai_path(repo, "machine", "files.json"), {"files": files})
    write_json(ai_path(repo, "machine", "artifacts.json"), {"artifacts": artifacts})
    write_json(ai_path(repo, "machine", "context_units.json"), {"units": units})
    return {"files_indexed": len(files), "context_units": len(units)}
