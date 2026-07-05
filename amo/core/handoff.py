from pathlib import Path

from amo.evidence.ledger import record_evidence
from amo.io import read_text_if_exists, write_text
from amo.paths import ai_path, ensure_dirs


def build_handoff(repo: Path, task: str, summary: str = "") -> Path:
    repo = repo.resolve()
    ensure_dirs(repo)
    state = read_text_if_exists(ai_path(repo, "state.md"))
    tasks = read_text_if_exists(ai_path(repo, "tasks.md"))
    decisions = read_text_if_exists(ai_path(repo, "decisions.md"))
    tests = read_text_if_exists(ai_path(repo, "tests.md"))
    last_context = read_text_if_exists(ai_path(repo, "runtime", "last_context.md"))

    content = render_handoff(
        task=task,
        summary=summary,
        state=state,
        tasks=tasks,
        decisions=decisions,
        tests=tests,
        last_context=last_context,
    )
    output = ai_path(repo, "packs", "handoff.md")
    write_text(output, content)
    write_text(ai_path(repo, "runtime", "session_handoff.md"), content)
    record_evidence(
        repo,
        kind="handoff",
        source="amo handoff",
        result=f"task={task}",
        authority=0.6,
        artifacts=(".ai/packs/handoff.md",),
        limitations=("session summary is agent-declared synthetic evidence",),
    )
    return output


def render_handoff(task: str, summary: str, state: str, tasks: str, decisions: str, tests: str, last_context: str) -> str:
    return "\n".join(
        [
            "# AMO Session Handoff",
            "",
            "Use this file to restart an agent session without carrying a long chat history.",
            "",
            "## Active Task",
            "",
            task,
            "",
            "## Current Session Summary",
            "",
            summary or "No summary provided.",
            "",
            "## Current Truth",
            "",
            _first_lines(state, 20, "No state memory found."),
            "",
            "## Open Tasks",
            "",
            _first_lines(tasks, 20, "No task memory found."),
            "",
            "## Decisions",
            "",
            _first_lines(decisions, 20, "No decision memory found."),
            "",
            "## Validation",
            "",
            _first_lines(tests, 20, "No test memory found."),
            "",
            "## Last Context Pack Pointer",
            "",
            "The previous context pack is available at `.ai/runtime/last_context.md` when deeper expansion is needed.",
            "",
            "## Agent Rules",
            "",
            "- Start from this handoff, not the old chat transcript.",
            "- Use `.ai/` memory as the project truth.",
            "- Expand files only when evidence is missing.",
            "- After work, run `amo postflight` and `amo validate`.",
            "",
        ]
    )


def _first_lines(text: str, limit: int, fallback: str) -> str:
    stripped = text.strip()
    if not stripped:
        return fallback
    return "\n".join(stripped.splitlines()[:limit])
