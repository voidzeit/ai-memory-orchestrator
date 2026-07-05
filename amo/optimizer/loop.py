from __future__ import annotations

from collections import Counter
from pathlib import Path

from amo.evidence.ledger import record_evidence
from amo.io import write_json, write_text
from amo.optimizer.signals import SEVERITIES, collect_signals


def run_suggest(repo: Path) -> Path:
    """Collect deterministic findings and write one evolution cycle. Propose only."""
    repo = repo.resolve()
    findings = collect_signals(repo)
    root = repo / ".ai" / "evolution"
    root.mkdir(parents=True, exist_ok=True)
    cycle_number = len(sorted(root.glob("cycle-*.json"))) + 1
    cycle = {
        "cycle": cycle_number,
        "mode": "suggest",
        "llm": False,
        "auto_fix": False,
        "background_work": False,
        "findings": findings,
    }
    output = root / f"cycle-{cycle_number:04d}.json"
    write_json(output, cycle)
    by_severity = Counter(str(finding["severity"]) for finding in findings)
    by_layer = Counter(str(finding["layer"]) for finding in findings)
    write_json(
        root / "metrics.json",
        {
            "cycle": cycle_number,
            "findings_total": len(findings),
            "by_severity": dict(by_severity),
            "by_layer": dict(by_layer),
        },
    )
    write_text(root / "findings.md", render_findings(findings, cycle_number))
    record_evidence(
        repo,
        kind="optimizer_trial",
        source="amo optimize suggest",
        result=f"cycle={cycle_number}, findings={len(findings)}",
        authority=0.8,
        artifacts=(
            f".ai/evolution/cycle-{cycle_number:04d}.json",
            ".ai/evolution/findings.md",
            ".ai/evolution/metrics.json",
        ),
        limitations=("deterministic heuristics; proposes only, changes nothing",),
    )
    return output


def findings_require_action(findings: list[dict[str, object]]) -> bool:
    return any(finding["severity"] in {"high", "medium"} for finding in findings)


def render_findings(findings: list[dict[str, object]], cycle_number: int) -> str:
    lines = [
        "# Evolution Findings",
        "",
        f"Cycle {cycle_number}. Deterministic signals only — no LLM, no autofix.",
        "",
    ]
    if not findings:
        lines.append("No findings. All monitored signals are clean.")
        return "\n".join(lines) + "\n"
    for severity in SEVERITIES:
        matched = [finding for finding in findings if finding["severity"] == severity]
        if not matched:
            continue
        lines.extend([f"## {severity.capitalize()}", ""])
        for finding in matched:
            lines.append(f"- `{finding['id']}` ({finding['layer']}): {finding['message']}")
            for item in finding["evidence"]:
                lines.append(f"  - evidence: {item}")
            lines.append(f"  - recommendation: {finding['recommendation']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
