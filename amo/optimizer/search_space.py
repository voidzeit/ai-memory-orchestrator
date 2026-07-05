from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from amo.optimizer.params import ParameterDefinition


@dataclass(frozen=True)
class SearchSpace:
    version: int
    parameters: dict[str, ParameterDefinition]
    disconnected: tuple[str, ...] = ()

    def defaults(self) -> dict[str, Any]:
        return {name: definition.default for name, definition in self.parameters.items()}

    def sample(self, rng: random.Random) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for name, definition in self.parameters.items():
            if definition.type == "int":
                values[name] = rng.randint(int(definition.low), int(definition.high))
            elif definition.type == "float":
                values[name] = rng.uniform(float(definition.low), float(definition.high))
            elif definition.type == "bool":
                values[name] = bool(rng.getrandbits(1))
            else:
                values[name] = rng.choice(definition.choices)
        return values


def load_search_space(path: Path) -> SearchSpace:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict) or not isinstance(raw.get("parameters"), dict):
        raise ValueError("search space requires a parameters mapping")
    definitions: dict[str, ParameterDefinition] = {}
    errors: list[str] = []
    for name, data in raw["parameters"].items():
        try:
            definitions[str(name)] = ParameterDefinition.from_dict(str(name), data)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        raise ValueError("Invalid search space:\n- " + "\n- ".join(errors))
    return SearchSpace(
        version=int(raw.get("version", 1)),
        parameters=definitions,
        disconnected=tuple(str(item) for item in raw.get("disconnected", ())),
    )
