from __future__ import annotations

from pathlib import Path

from amo.core.validate import validate_repo
from amo.io import write_json, write_text


def evolve_safe(repo: Path) -> Path:
    repo = repo.resolve()
    root = repo / ".ai" / "evolution"
    root.mkdir(parents=True, exist_ok=True)
    cycles = sorted(root.glob("cycle-*.json"))
    cycle_number = len(cycles) + 1
    validation = validate_repo(repo, strict=False)
    metrics = {"cycles": cycle_number, "validation_status": validation["status"], "finding_count": len(validation["warnings"])}
    cycle = {"cycle": cycle_number, "mode": "safe", "llm": False, "auto_fix": False, "background_work": False, "findings": validation["warnings"]}
    write_json(root / "metrics.json", metrics)
    output = root / f"cycle-{cycle_number:04d}.json"
    write_json(output, cycle)
    findings = validation["warnings"] or ["No deterministic validation findings."]
    write_text(root / "findings.md", "# Evolution Findings\n\n" + "\n".join(f"- {item}" for item in findings) + "\n")
    return output
