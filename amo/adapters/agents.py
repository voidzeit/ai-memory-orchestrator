from pathlib import Path

from amo.adapters.profile import ADAPTER_PROFILE
from amo.io import write_text

AGENTS_TEMPLATE = """# Agent Instructions

This repository uses AI Memory Orchestrator.

Read first if present:

- `.ai/manifest.yaml`
- `.ai/state.md`
- `.ai/tasks.md`
- `.ai/decisions.md`
- `.ai/packs/quick.md`

Rules:

- `.ai/` is canonical memory.
- `.ai/machine/` and `.ai/packs/` are derived.
- `.ai/runtime/` is disposable.
- Make the smallest safe change.
- Do not expose secrets.
- Update memory via `amo postflight` when project state changes.

""" + ADAPTER_PROFILE


def export_agents_md(repo: Path) -> Path:
    path = repo / "AGENTS.md"
    write_text(path, AGENTS_TEMPLATE)
    return path
