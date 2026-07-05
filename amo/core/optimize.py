from __future__ import annotations

from pathlib import Path

from amo.optimizer.loop import findings_require_action, run_suggest
from amo.optimizer.planner import write_plan
from amo.optimizer.signals import collect_signals


def optimize_suggest(repo: Path) -> Path:
    return run_suggest(repo)


def optimize_check(repo: Path) -> tuple[bool, list[dict[str, object]]]:
    """Return (action_required, findings) from a fresh deterministic pass."""
    findings = collect_signals(repo)
    return findings_require_action(findings), findings


def optimize_plan(repo: Path) -> Path:
    return write_plan(repo)
