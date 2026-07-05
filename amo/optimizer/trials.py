from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Trial:
    trial: int
    seed: int
    params: dict[str, Any]
    metrics: dict[str, object]
    objective_score: float
    unscored: list[str]
    status: str = "completed"

    def as_dict(self) -> dict[str, object]:
        return {
            "trial": self.trial,
            "seed": self.seed,
            "classification": "evolutionary/derived",
            "params": self.params,
            "metrics": self.metrics,
            "objective_score": self.objective_score,
            "unscored": self.unscored,
            "status": self.status,
        }


def write_trials(path: Path, trials: list[Trial]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(trial.as_dict(), sort_keys=True) + "\n" for trial in trials), encoding="utf-8")


def select_best(trials: list[Trial]) -> Trial:
    completed = [trial for trial in trials if trial.status == "completed"]
    if not completed:
        raise ValueError("No completed trials")
    return max(completed, key=lambda trial: (trial.objective_score, -trial.trial))
