from pathlib import Path

from amo.io import read_text_if_exists, write_text
from amo.paths import ai_path


def sync_obsidian(repo: Path, output_path: Path | None = None) -> Path:
    repo = repo.resolve()
    output = output_path or repo / ".obsidian" / "project-memory"
    output.mkdir(parents=True, exist_ok=True)
    pages = {
        "00 Overview.md": "# AMO Project Memory\n\nGenerated from `.ai/`.\n",
        "01 State.md": read_text_if_exists(ai_path(repo, "state.md"), "# State\n"),
        "02 Decisions.md": read_text_if_exists(ai_path(repo, "decisions.md"), "# Decisions\n"),
        "03 Tasks.md": read_text_if_exists(ai_path(repo, "tasks.md"), "# Tasks\n"),
        "04 Graph.md": read_text_if_exists(ai_path(repo, "graph.md"), "# Graph\n"),
        "05 Tests.md": read_text_if_exists(ai_path(repo, "tests.md"), "# Tests\n"),
    }
    for name, content in pages.items():
        write_text(output / name, content)
    return output
