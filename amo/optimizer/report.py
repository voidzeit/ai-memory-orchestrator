from __future__ import annotations

from amo.optimizer.trials import Trial


def render_parameter_report(trials: list[Trial], best: Trial) -> str:
    scored = [(name, value) for name, value in best.metrics.items() if isinstance(value, (int, float))]
    lines = [
        "# AMO Parameter Optimization Report",
        "",
        "Classification: **evolutionary/derived**",
        "",
        f"Completed {len(trials)} deterministic trials. Trial {best.trial} won with score `{best.objective_score}`.",
        "",
        "## Why it won",
        "",
    ]
    lines.extend(f"- `{name}`: {value}" for name, value in scored)
    lines.extend(["", "## Unscored metrics", ""])
    lines.extend(f"- `{name}` (ground truth or evidence unavailable)" for name in best.unscored)
    lines.extend(["", "## Best parameters", ""])
    lines.extend(f"- `{name}`: `{value}`" for name, value in best.params.items())
    return "\n".join(lines) + "\n"
