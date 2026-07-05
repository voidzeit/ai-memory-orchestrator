from __future__ import annotations

import json
import random
from pathlib import Path

from amo.core.benchmark import run_benchmark
from amo.core.graph import build_graph
from amo.core.scan import scan_repo
from amo.core.validate import validate_repo
from amo.optimizer.objective import load_objective_weights, score_objective
from amo.optimizer.search_space import SearchSpace
from amo.optimizer.trials import Trial, select_best, write_trials


def _graph_metrics(repo: Path) -> tuple[float | None, float | None]:
    path = repo / ".ai" / "machine" / "graph.json"
    if not path.exists():
        return None, None
    graph = json.loads(path.read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    ids = {node.get("id") for node in nodes}
    truthful = sum(edge.get("source") in ids and edge.get("target") in ids for edge in edges)
    truthfulness = truthful / len(edges) if edges else 1.0
    interoperability = 1.0 if graph.get("schema_version") and nodes is not None and edges is not None else 0.0
    return truthfulness, interoperability


def evaluate_params(repo: Path, params: dict[str, object]) -> dict[str, object]:
    benchmark_path = run_benchmark(
        repo,
        "optimize context parameters",
        params=params,
        scan_excludes={".ai/machine", ".ai/packs", ".ai/evolution"},
    )
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))["metrics"]
    validation = validate_repo(repo, strict=False)
    warnings = [str(item).lower() for item in validation["warnings"]]
    graph_truthfulness, interoperability = _graph_metrics(repo)
    canonical = ("manifest.yaml", "state.md", "decisions.md", "tasks.md", "tests.md", "graph.md")
    durability = sum((repo / ".ai" / name).exists() for name in canonical) / len(canonical)
    token_reduction = benchmark.get("token_reduction")
    return {
        "useful_context_per_token": None,
        "graph_truthfulness": graph_truthfulness,
        "validation_confidence": 1.0 if validation["status"] == "green" else 0.5,
        "memory_durability": durability,
        "interoperability": interoperability,
        "token_cost": 1.0 - float(token_reduction) if isinstance(token_reduction, (int, float)) else None,
        "stale_context": float(any("stale" in warning for warning in warnings)),
        "duplicated_context": None,
        "wrong_file_selection": None,
        "graph_drift": float(any("graph" in warning or "drift" in warning for warning in warnings)),
        "benchmark.file_selection_precision": benchmark.get("file_selection_precision"),
        "benchmark.file_selection_recall": benchmark.get("file_selection_recall"),
    }


def run_sweep(
    repo: Path,
    space: SearchSpace,
    objective_path: Path,
    trials_count: int,
    seed: int,
) -> tuple[list[Trial], Trial]:
    if trials_count < 1:
        raise ValueError("trials must be at least 1")
    repo = repo.resolve()
    scan_repo(repo, extra_excludes={".ai/machine", ".ai/packs", ".ai/evolution"})
    build_graph(repo)
    rng = random.Random(seed)
    weights = load_objective_weights(objective_path)
    trials: list[Trial] = []
    for number in range(1, trials_count + 1):
        params = space.defaults() if number == 1 else space.sample(rng)
        metrics = evaluate_params(repo, params)
        result = score_objective(metrics, weights)
        all_unscored = result.unscored + [
            name for name, value in metrics.items() if value is None and name not in result.unscored
        ]
        trials.append(Trial(number, seed, params, metrics, result.score, all_unscored))
    write_trials(repo / ".ai" / "evolution" / "trials.jsonl", trials)
    best = select_best(trials)
    return trials, best
