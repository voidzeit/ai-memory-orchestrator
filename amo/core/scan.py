from pathlib import Path
from typing import Any

from amo.config import get_config_value, load_config
from amo.index.artifacts import build_artifact_index
from amo.index.context_units import build_context_units
from amo.index.files import build_file_index
from amo.io import write_json
from amo.paths import ai_path, ensure_dirs

_DEFAULT_EXCLUDES: set[str] = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ai/runtime",
}


def normalize_excludes(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {value}
    if isinstance(value, (list, tuple, set)):
        return {str(item) for item in value if item}
    return set()


def scan_repo(repo: Path) -> dict[str, int]:
    repo = repo.resolve()
    ensure_dirs(repo)
    config = load_config(repo)
    configured_excludes = normalize_excludes(get_config_value(config, "scan.excludes", []))
    excludes = _DEFAULT_EXCLUDES | configured_excludes
    files = build_file_index(repo, excludes=excludes)
    artifacts = build_artifact_index(repo, files)
    units = build_context_units(repo, files)
    write_json(ai_path(repo, "machine", "files.json"), {"files": files})
    write_json(ai_path(repo, "machine", "artifacts.json"), {"artifacts": artifacts})
    write_json(ai_path(repo, "machine", "context_units.json"), {"units": units})
    return {"files_indexed": len(files), "context_units": len(units)}
