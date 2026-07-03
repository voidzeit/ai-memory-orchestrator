from pathlib import Path

from amo.io import write_text


def export_opencode_instructions(repo: Path) -> Path:
    """Export OpenCode-oriented repository instructions."""
    path = repo / "OPENCODE.md"
    write_text(path, "# OpenCode Instructions\n\nRead AGENTS.md and `.ai/` memory before making changes.\n")
    return path
