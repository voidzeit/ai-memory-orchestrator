from __future__ import annotations

from pathlib import Path

from amo.io import write_text
from amo.optimizer.signals import SEVERITIES, collect_signals


def write_plan(repo: Path) -> Path:
    repo = repo.resolve()
    findings = collect_signals(repo)
    output = repo / ".ai" / "evolution" / "plan.md"
    write_text(output, render_plan(findings))
    return output


def render_plan(findings: list[dict[str, object]]) -> str:
    lines = [
        "# Evolution Plan",
        "",
        "Propose-only plan derived from deterministic findings. AMO does not apply",
        "these changes itself; a human or supervised agent must.",
        "",
    ]
    if not findings:
        lines.append("Nothing to plan. All monitored signals are clean.")
        return "\n".join(lines) + "\n"
    step = 1
    for severity in SEVERITIES:
        matched = [finding for finding in findings if finding["severity"] == severity]
        if not matched:
            continue
        lines.extend([f"## {severity.capitalize()} priority", ""])
        for finding in matched:
            lines.append(f"{step}. {finding['recommendation']} (`{finding['id']}`, {finding['layer']})")
            step += 1
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
