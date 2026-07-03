import json
from pathlib import Path

from amo.context.ranking import rank_units
from amo.context.render import render_context_pack
from amo.io import read_text_if_exists, write_text
from amo.paths import ai_path, ensure_dirs

PROFILE_BUDGETS = {"tiny": 1500, "quick": 3000, "debug": 10000, "architecture": 14000, "full": 24000}


def build_context_pack(repo: Path, task: str, profile: str = "quick") -> Path:
    repo = repo.resolve()
    ensure_dirs(repo)
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
    budget = PROFILE_BUDGETS.get(profile, PROFILE_BUDGETS["quick"])
    selected = rank_units(units, task=task, budget=budget)
    content = render_context_pack(task=task, profile=profile, budget=budget, canonical=canonical, units=selected)
    output = ai_path(repo, "packs", f"{profile}.md")
    write_text(output, content)
    write_text(ai_path(repo, "runtime", "last_context.md"), content)
    return output
