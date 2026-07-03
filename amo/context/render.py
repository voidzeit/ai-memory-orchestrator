def render_context_pack(task: str, profile: str, budget: int, canonical: dict[str, str], units: list[dict[str, object]]) -> str:
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
        "",
        "## Current Truth",
        "",
        _first_nonempty(canonical.get("state", ""), "No state memory found."),
        "",
        "## Relevant Context Units",
        "",
        "| Unit | Type | Expand |",
        "|---|---|---|",
    ]
    for unit in units:
        lines.append(f"| {unit.get('title')} | {unit.get('type')} | `{unit.get('expand')}` |")
    lines.extend([
        "",
        "## Expansion Map",
        "",
        "Open the referenced files only when deeper context is needed.",
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
    ])
    return "\n".join(lines)


def _first_nonempty(text: str, fallback: str) -> str:
    stripped = text.strip()
    if not stripped:
        return fallback
    return "\n".join(stripped.splitlines()[:30])
