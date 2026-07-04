from pathlib import Path

from amo.adapters.profile import ADAPTER_PROFILE
from amo.io import write_text


def export_cline_memory_bank(repo: Path) -> Path:
    """Export a minimal Cline Memory Bank from AMO memory."""
    path = repo / "memory-bank" / "activeContext.md"
    write_text(path, "# Active Context\n\nGenerated from AMO `.ai/` memory.\n\n" + ADAPTER_PROFILE)
    return path
