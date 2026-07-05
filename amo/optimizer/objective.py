from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


POSITIVE_METRICS = (
    "useful_context_per_token",
    "graph_truthfulness",
    "validation_confidence",
    "memory_durability",
    "interoperability",
)
NEGATIVE_METRICS = (
    "token_cost",
    "stale_context",
    "duplicated_context",
    "wrong_file_selection",
    "graph_drift",
)


@dataclass(frozen=True)
class ObjectiveResult:
    score: float
    unscored: list[str]
    contributions: dict[str, float]


def load_objective_weights(path: Path) -> dict[str, float]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("weights"), dict):
        raise ValueError("objective requires a weights mapping")
    return {str(key): float(value) for key, value in raw["weights"].items()}


def score_objective(metrics: dict[str, object], weights: dict[str, float]) -> ObjectiveResult:
    contributions: dict[str, float] = {}
    unscored: list[str] = []
    for name in (*POSITIVE_METRICS, *NEGATIVE_METRICS):
        value = metrics.get(name)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            unscored.append(name)
            continue
        normalized = min(1.0, max(0.0, float(value)))
        sign = -1.0 if name in NEGATIVE_METRICS else 1.0
        contributions[name] = sign * normalized * weights.get(name, 1.0)
    return ObjectiveResult(round(sum(contributions.values()), 8), unscored, contributions)
