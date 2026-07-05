from amo.context.profiles import DEGRADATION_SIGNALS, PRIORITY_ORDER, get_profile


def render_context_pack(
    task: str,
    profile: str,
    budget: int,
    canonical: dict[str, str],
    units: list[dict[str, object]],
    seeds: list[str] | None = None,
    neighborhood: list[tuple[str, float]] | None = None,
) -> str:
    profile_data = get_profile(profile)
    lines = [
        "# AMO Context Pack",
        "",
        "## Task",
        "",
        task,
        "",
        "## Budget",
        "",
        f"Profile: `{profile}`",
        f"Max tokens: `{budget}`",
        f"Purpose: {profile_data['purpose']}",
        "",
        "## Agent Operating Rules",
        "",
        f"- {profile_data['agent_rule']}",
        "- Treat this context pack as the session entrypoint.",
        "- Prefer expansion paths over asking the user to repeat context.",
        "- Use canonical memory before chat history when facts conflict.",
        "- Keep the working set small; expand only when evidence is missing.",
        "",
        "## Authority Order",
        "",
    ]
    lines.extend([f"{index + 1}. `{source}`" for index, source in enumerate(PRIORITY_ORDER)])
    lines.extend(
        [
            "",
            "## Degradation Signals",
            "",
            "Start a handoff or compact the session when any of these appear:",
            "",
        ]
    )
    lines.extend([f"- {signal}" for signal in DEGRADATION_SIGNALS])
    lines.extend(
        [
            "",
            "## Current Truth",
            "",
            _first_nonempty(canonical.get("state", ""), "No state memory found."),
            "",
            "## Decisions Snapshot",
            "",
            _first_nonempty(canonical.get("decisions", ""), "No decision memory found."),
            "",
            "## Tests Snapshot",
            "",
            _first_nonempty(canonical.get("tests", ""), "No test memory found."),
            "",
            "## Relevant Context Units",
            "",
            "| Unit | Type | Tokens | Expand |",
            "|---|---|---:|---|",
        ]
    )
    for unit in units:
        lines.append(
            f"| {unit.get('title')} | {unit.get('type')} | {unit.get('tokens', '')} | `{unit.get('expand')}` |"
        )
    if seeds or neighborhood:
        lines.extend(["", "## Graph Neighborhood", ""])
        if seeds:
            lines.append("Selection was seeded from these task-relevant files:")
            lines.append("")
            lines.extend(f"- `{seed}`" for seed in seeds)
        if neighborhood:
            lines.extend(
                [
                    "",
                    "Structurally near files (expansion candidates, by graph proximity):",
                    "",
                ]
            )
            lines.extend(f"- `{path}` (proximity {score:.2f})" for path, score in neighborhood)
    lines.extend(
        [
            "",
            "## Expansion Map",
            "",
            "Open referenced files only when deeper context is needed. Do not load the entire repository by default.",
            "",
            "## Session Handoff Rule",
            "",
            "Before the chat becomes long or noisy, run:",
            "",
            "```bash",
            f"amo handoff --task {task!r} --summary \"<current state and next step>\"",
            "```",
            "",
            "## Postflight",
            "",
            "After completing the task, run:",
            "",
            "```bash",
            f"amo postflight --task {task!r} --summary \"<what changed>\"",
            "amo validate",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def _first_nonempty(text: str, fallback: str) -> str:
    stripped = text.strip()
    if not stripped:
        return fallback
    return "\n".join(stripped.splitlines()[:30])
