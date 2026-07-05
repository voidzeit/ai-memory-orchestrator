import random
from pathlib import Path

import pytest
import yaml

from amo.context.ranking import rank_units
from amo.optimizer.objective import score_objective
from amo.optimizer.search_space import load_search_space
from amo.optimizer.trials import Trial, select_best


def _write_space(path, parameters):
    path.write_text(yaml.safe_dump({"version": 1, "parameters": parameters}), encoding="utf-8")


def test_loading_search_space():
    space = load_search_space(Path(".amo/optimization/search_space.yaml"))
    assert space.parameters["context.max_units"].default == 25
    assert space.parameters["context.max_units"].safe_to_apply is True
    assert len(space.parameters) == 20


def test_invalid_parameter_bounds_are_reported(tmp_path):
    path = tmp_path / "space.yaml"
    _write_space(
        path,
        {
            "bad": {
                "type": "int",
                "default": 3,
                "low": 5,
                "high": 1,
                "safe_to_apply": False,
                "description": "invalid",
            }
        },
    )
    with pytest.raises(ValueError, match="low must be less than or equal to high"):
        load_search_space(path)


def test_objective_scoring_marks_missing_ground_truth_unscored():
    result = score_objective(
        {"graph_truthfulness": 1.0, "token_cost": 0.25},
        {"graph_truthfulness": 2.0, "token_cost": 1.0},
    )
    assert result.score == 1.75
    assert "useful_context_per_token" in result.unscored
    assert "wrong_file_selection" in result.unscored


def test_trial_generation_is_deterministic_for_seed():
    space = load_search_space(Path(".amo/optimization/search_space.yaml"))
    first_rng = random.Random(42)
    second_rng = random.Random(42)
    first = [space.sample(first_rng) for _ in range(2)]
    second = [space.sample(second_rng) for _ in range(2)]
    assert first == second


def test_best_params_selection_prefers_score_then_earliest_trial():
    trials = [
        Trial(1, 42, {"x": 1}, {}, 0.5, []),
        Trial(2, 42, {"x": 2}, {}, 0.8, []),
        Trial(3, 42, {"x": 3}, {}, 0.8, []),
    ]
    assert select_best(trials).trial == 2


def test_ranking_uses_configured_context_max_units():
    units = [
        {"title": f"unit {index}", "summary": "fix tests", "tags": [], "tokens": 1}
        for index in range(10)
    ]
    selected = rank_units(units, task="fix tests", budget=100, params={"context.max_units": 3})
    assert len(selected) == 3


def test_ranking_preserves_default_limit_without_params():
    units = [
        {"title": f"unit {index}", "summary": "fix tests", "tags": [], "tokens": 1}
        for index in range(30)
    ]
    assert len(rank_units(units, task="fix tests", budget=100)) == 25
