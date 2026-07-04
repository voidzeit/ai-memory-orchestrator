from pathlib import Path

from amo.adapters.profile import ADAPTER_PROFILE
from amo.io import write_text


def export_claude_md(repo: Path) -> Path:
    """Export Claude Code instructions from AMO memory."""
    path = repo / "CLAUDE.md"
    write_text(path, "# Claude Code Instructions\n\nRead `.ai/` memory before making changes.\n\n" + ADAPTER_PROFILE)
    return path
