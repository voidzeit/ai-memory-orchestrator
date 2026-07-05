from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from amo.evidence.ledger import read_ledger


def _read_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def organism_snapshot(repo: Path) -> dict[str, object]:
    """Aggregate the organism's vital signs from existing artifacts. Read-only."""
    repo = repo.resolve()
    machine = repo / ".ai" / "machine"

    validation = _read_json(machine / "validation.json")
    benchmark = _read_json(machine / "benchmark.json")
    evolution_metrics = _read_json(repo / ".ai" / "evolution" / "metrics.json")

    graph = _read_json(machine / "graph.json") or {}
    nodes = graph.get("nodes", []) if isinstance(graph.get("nodes"), list) else []
    edges = graph.get("edges", []) if isinstance(graph.get("edges"), list) else []
    graph_summary = {
        "nodes": len(nodes),
        "edges": len(edges),
        "by_level": dict(Counter(str(node.get("level", "unknown")) for node in nodes)),
        "by_type": dict(Counter(str(node.get("type", "unknown")) for node in nodes).most_common(12)),
    }

    packs_dir = repo / ".ai" / "packs"
    packs = sorted(item.name for item in packs_dir.glob("*.md")) if packs_dir.exists() else []
    adapters = {
        "agents": (repo / "AGENTS.md").exists(),
        "claude": (repo / "CLAUDE.md").exists(),
        "cursor": (repo / ".cursor").exists(),
        "cline": (repo / ".clinerules").exists() or (repo / "memory-bank").exists(),
        "opencode": (repo / "opencode.json").exists(),
    }

    ledger = read_ledger(repo)
    by_severity: dict[str, int] = {}
    if evolution_metrics and isinstance(evolution_metrics.get("by_severity"), dict):
        by_severity = {str(key): int(value) for key, value in evolution_metrics["by_severity"].items()}

    status = "unknown"
    if validation:
        status = str(validation.get("status", "unknown"))
    if by_severity.get("high"):
        status = "red"

    return {
        "status": status,
        "validation": validation,
        "graph": graph_summary,
        "benchmark": (benchmark or {}).get("metrics"),
        "evolution": evolution_metrics,
        "packs": packs,
        "adapters": adapters,
        "ledger_entries": len(ledger),
        "ledger_tail": ledger[-20:],
    }
