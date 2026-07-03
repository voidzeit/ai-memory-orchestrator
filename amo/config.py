from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "version": 1,
    "context": {
        "default_profile": "quick",
        "profiles": {
            "micro": {"max_tokens": 1200},
            "quick": {"max_tokens": 3000},
            "debug": {"max_tokens": 8000},
            "architecture": {"max_tokens": 12000},
            "handoff": {"max_tokens": 2500},
            "full": {"max_tokens": 20000},
        },
    },
    "scan": {
        "excludes": [
            ".git",
            ".venv",
            "node_modules",
            "dist",
            "build",
            "__pycache__",
            ".pytest_cache",
            ".ai/runtime",
        ],
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8787,
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(repo: Path) -> dict[str, Any]:
    config_path = repo / ".amo.yaml"
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with config_path.open("r", encoding="utf-8") as file:
            user_config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {config_path}: {exc}") from exc
    if not isinstance(user_config, dict):
        return DEFAULT_CONFIG.copy()
    return deep_merge(DEFAULT_CONFIG, user_config)


def get_config_value(config: dict[str, Any], path: str, default: Any = None) -> Any:
    keys = path.split(".")
    current: Any = config
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return default
        else:
            return default
    return current


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, sort_keys=False, allow_unicode=True)
