from datetime import datetime, timezone
from pathlib import Path

from amo.evidence.ledger import record_evidence
from amo.io import read_text_if_exists, write_text
from amo.paths import ai_path, ensure_dirs
from amo.runtime.backups import backup_canonical
from amo.runtime.lock import memory_lock
from amo.runtime.run_history import write_run_history


def apply_postflight(
    repo: Path,
    task: str,
    summary: str,
    outcome: str = "completed",
    validation: str = "",
    changed_files: list[str] | None = None,
    decision: str = "",
) -> Path:
    repo = repo.resolve()
    ensure_dirs(repo)
    changed_files = changed_files or []
    with memory_lock(repo):
        backup_canonical(repo)
        now = datetime.now(timezone.utc).isoformat()
        tasks_path = ai_path(repo, "tasks.md")
        state_path = ai_path(repo, "state.md")
        current_tasks = read_text_if_exists(tasks_path, "# Tasks\n")
        current_state = read_text_if_exists(state_path, "# State\n")
        note_lines = [
            f"\n## Postflight — {now}",
            "",
            f"Task: {task}",
            "",
            f"Summary: {summary}",
            "",
            f"Outcome: {outcome}",
        ]
        if changed_files:
            note_lines.append(f"Changed files: {', '.join(changed_files)}")
        postflight_note = "\n".join(note_lines) + "\n"
        write_text(tasks_path, current_tasks.rstrip() + postflight_note)
        write_text(state_path, current_state.rstrip() + postflight_note)

        if decision:
            decisions_path = ai_path(repo, "decisions.md")
            current = read_text_if_exists(decisions_path, "# Decisions\n")
            write_text(
                decisions_path,
                current.rstrip() + f"\n\n## Decision — {now}\n\n{decision}\n",
            )
        if validation:
            tests_path = ai_path(repo, "tests.md")
            current = read_text_if_exists(tests_path, "# Tests\n")
            write_text(
                tests_path,
                current.rstrip() + f"\n\n## Validation — {now}\n\n{validation}\n",
            )

        note_path, mirror_path = write_run_history(
            repo,
            task=task,
            summary=summary,
            outcome=outcome,
            validation=validation,
            changed_files=changed_files,
            decision=decision,
        )
        write_text(ai_path(repo, "runtime", "last_postflight.md"), postflight_note)
        record_evidence(
            repo,
            kind="postflight",
            source="amo postflight",
            result=f"task={task}, outcome={outcome}",
            authority=0.5,
            artifacts=(
                ".ai/tasks.md",
                ".ai/state.md",
                str(note_path.relative_to(repo).as_posix()),
                str(mirror_path.relative_to(repo).as_posix()),
            ),
            limitations=("summary is agent-declared until corroborated by validation evidence",),
        )
    return tasks_path
