from __future__ import annotations

import json
from pathlib import Path

from amo.config import get_config_value, load_config
from amo.context.explain import explain_selection
from amo.context.graph_neighborhood import compute_neighborhood
from amo.context.profiles import get_budget
from amo.context.ranking import DEFAULT_RANKING_PARAMS, rank_units
from amo.context.render import render_context_pack
from amo.evidence.ledger import record_evidence
from amo.io import read_text_if_exists, write_json, write_text
from amo.paths import ai_path, ensure_dirs

DEFAULT_GRAPH_PARAMS: dict[str, int | float] = {
    "graph.seed_top_k": 10,
    "graph.max_hops": 2,
    "graph.distance_decay": 0.75,
}


def build_context_pack(
    repo: Path,
    task: str,
    profile: str = "",
    params: dict[str, object] | None = None,
) -> Path:
    repo = repo.resolve()
    ensure_dirs(repo)
    config = load_config(repo)

    if not profile:
        profile = get_config_value(config, "context.default_profile", "quick")

    units_path = ai_path(repo, "machine", "context_units.json")
    if units_path.exists():
        units = json.loads(units_path.read_text(encoding="utf-8")).get("units", [])
    else:
        units = []

    canonical = {
        "manifest": read_text_if_exists(ai_path(repo, "manifest.yaml")),
        "state": read_text_if_exists(ai_path(repo, "state.md")),
        "decisions": read_text_if_exists(ai_path(repo, "decisions.md")),
        "tasks": read_text_if_exists(ai_path(repo, "tasks.md")),
        "tests": read_text_if_exists(ai_path(repo, "tests.md")),
    }
    budget = get_budget(profile, config=config)
    ranking_params = {
        key: get_config_value(config, key, default)
        for key, default in DEFAULT_RANKING_PARAMS.items()
    }
    ranking_params.update(params or {})
    graph_params = {
        key: get_config_value(config, key, default)
        for key, default in DEFAULT_GRAPH_PARAMS.items()
    }
    graph_params.update({key: value for key, value in (params or {}).items() if key in DEFAULT_GRAPH_PARAMS})
    proximity, seeds = compute_neighborhood(
        repo,
        units,
        task,
        seed_top_k=int(graph_params["graph.seed_top_k"]),
        max_hops=int(graph_params["graph.max_hops"]),
        distance_decay=float(graph_params["graph.distance_decay"]),
    )
    selected = rank_units(units, task=task, budget=budget, params=ranking_params, proximity=proximity)
    explanations = explain_selection(selected, task=task, proximity=proximity, seeds=seeds)
    write_json(
        ai_path(repo, "machine", "context_explain.json"),
        {"task": task, "profile": profile, "seeds": seeds, "selection": explanations},
    )
    selected_paths = {str(unit.get("expand") or unit.get("title") or "") for unit in selected}
    neighborhood = [
        (path, score)
        for path, score in sorted(proximity.items(), key=lambda item: (-item[1], item[0]))
        if path not in seeds and path not in selected_paths
    ][:8]
    content = render_context_pack(
        task=task,
        profile=profile,
        budget=budget,
        canonical=canonical,
        units=selected,
        seeds=seeds,
        neighborhood=neighborhood,
    )
    output = ai_path(repo, "packs", f"{profile}.md")
    write_text(output, content)
    write_text(ai_path(repo, "runtime", "last_context.md"), content)
    record_evidence(
        repo,
        kind="context_pack",
        source="amo context",
        result=f"profile={profile}, units={len(selected)}",
        authority=0.6,
        artifacts=(f".ai/packs/{profile}.md",),
        limitations=("compiled selection, not ground truth",),
    )
    return output
