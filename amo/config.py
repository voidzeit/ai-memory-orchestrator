from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "version": 0.1,
    "memory": {"source_of_truth": ".ai"},
    "context": {"default_profile": "quick"},
}


def load_config(repo: Path) -> dict[str, Any]:
    config_path = repo / ".amo.yaml"
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or DEFAULT_CONFIG.copy()


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, sort_keys=False, allow_unicode=True)
