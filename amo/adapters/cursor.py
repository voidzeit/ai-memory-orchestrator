from pathlib import Path

from amo.io import write_text


def export_cursor_rules(repo: Path) -> Path:
    """Export Cursor rules from AMO memory."""
    path = repo / ".cursor" / "rules" / "amo.mdc"
    write_text(path, "# AMO Cursor Rules\n\nUse `.ai/packs/quick.md` as the first context surface.\n")
    return path
