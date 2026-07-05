from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from amo.config import deep_merge, get_config_value, load_config, write_yaml
from amo.core.validate import validate_repo
from amo.io import write_text
from amo.optimizer.report import render_parameter_report
from amo.optimizer.search_space import SearchSpace, load_search_space
from amo.optimizer.sweep import run_sweep
from amo.optimizer.trials import Trial


def optimization_root(repo: Path) -> Path:
    return repo.resolve() / ".amo" / "optimization"


def load_project_search_space(repo: Path) -> SearchSpace:
    return load_search_space(optimization_root(repo) / "search_space.yaml")


def suggest_params(repo: Path) -> SearchSpace:
    return load_project_search_space(repo)


def sweep_params(repo: Path, trials: int, seed: int) -> Trial:
    repo = repo.resolve()
    space = load_project_search_space(repo)
    completed, best = run_sweep(
        repo,
        space,
        optimization_root(repo) / "objective.yaml",
        trials,
        seed,
    )
    evolution = repo / ".ai" / "evolution"
    best_data = {
        "version": 1,
        "classification": "evolutionary/derived",
        "source": "amo optimize params sweep",
        "trial": best.trial,
        "score": best.objective_score,
        "params": best.params,
        "unscored": best.unscored,
    }
    write_yaml(evolution / "best_params.yaml", best_data)
    write_text(evolution / "parameter-report.md", render_parameter_report(completed, best))
    return best


def load_best_params(repo: Path) -> dict[str, Any]:
    path = repo.resolve() / ".ai" / "evolution" / "best_params.yaml"
    if not path.exists():
        raise FileNotFoundError("Best parameters do not exist; run 'amo optimize params sweep' first")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("params"), dict):
        raise ValueError("Best parameters artifact is invalid")
    return data


def _nested_param(name: str, value: object) -> dict[str, object]:
    nested: dict[str, object] = {name.split(".")[-1]: value}
    for key in reversed(name.split(".")[:-1]):
        nested = {key: nested}
    return nested


def apply_safe_params(repo: Path, confirm: bool) -> dict[str, object]:
    if not confirm:
        raise ValueError("Refusing to apply parameters without --confirm")
    repo = repo.resolve()
    best = load_best_params(repo)
    validation = validate_repo(repo, strict=True)
    if validation["status"] == "red":
        raise ValueError("Refusing to apply parameters while validation is red")
    space = load_project_search_space(repo)
    eligible = {
        name: value
        for name, value in best["params"].items()
        if name in space.parameters and space.parameters[name].safe_to_apply
    }
    config = load_config(repo)
    changed = {
        name: value
        for name, value in eligible.items()
        if get_config_value(config, name, object()) != value
    }
    for name, value in changed.items():
        config = deep_merge(config, _nested_param(name, value))
    write_yaml(repo / ".amo.yaml", config)
    return changed
