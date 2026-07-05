from datetime import datetime, timezone
from pathlib import Path

from amo.evidence.ledger import record_evidence
from amo.io import read_text_if_exists, write_text
from amo.paths import ai_path, ensure_dirs


def apply_postflight(repo: Path, task: str, summary: str) -> Path:
    repo = repo.resolve()
    ensure_dirs(repo)
    now = datetime.now(timezone.utc).isoformat()
    tasks_path = ai_path(repo, "tasks.md")
    state_path = ai_path(repo, "state.md")
    current_tasks = read_text_if_exists(tasks_path, "# Tasks\n")
    current_state = read_text_if_exists(state_path, "# State\n")
    postflight_note = f"\n## Postflight — {now}\n\nTask: {task}\n\nSummary: {summary}\n"
    write_text(tasks_path, current_tasks.rstrip() + postflight_note)
    write_text(state_path, current_state.rstrip() + postflight_note)
    write_text(ai_path(repo, "runtime", "last_postflight.md"), postflight_note)
    record_evidence(
        repo,
        kind="postflight",
        source="amo postflight",
        result=f"task={task}",
        authority=0.5,
        artifacts=(".ai/tasks.md", ".ai/state.md"),
        limitations=("summary is agent-declared until corroborated by validation evidence",),
    )
    return tasks_path
