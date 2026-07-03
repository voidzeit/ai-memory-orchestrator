from pathlib import Path
import shutil

from amo.paths import ensure_dirs


def init_repo(repo: Path, template: str = "generic") -> str:
    repo = repo.resolve()
    ensure_dirs(repo)

    template_root = Path(__file__).resolve().parents[2] / "templates" / template
    if not template_root.exists():
        template_root = Path(__file__).resolve().parents[2] / "templates" / "generic"
    if not template_root.exists():
        _write_embedded_default(repo)
    else:
        for src in template_root.rglob("*"):
            if src.is_dir():
                continue
            rel = src.relative_to(template_root)
            dst = repo / rel
            if dst.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

    gitignore = repo / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if ".ai/runtime/" not in current:
        gitignore.write_text(current.rstrip() + "\n.ai/runtime/\n", encoding="utf-8")

    if not (repo / ".amo.yaml").exists():
        (repo / ".amo.yaml").write_text("version: 0.1\nmemory:\n  source_of_truth: .ai\n", encoding="utf-8")

    return str(repo / ".ai")


def _write_embedded_default(repo: Path) -> None:
    files = {
        ".ai/manifest.yaml": "project:\n  name: generic-project\n  type: generic\n",
        ".ai/state.md": "# State\n\nAMO memory initialized.\n",
        ".ai/decisions.md": "# Decisions\n\n## DEC-0001 — `.ai/` is source of truth\n",
        ".ai/tasks.md": "# Tasks\n\n- [ ] Review generated AMO memory.\n",
        ".ai/tests.md": "# Tests\n\nNo test commands configured yet.\n",
        ".ai/graph.md": "# Graph\n\nRun `amo graph build`.\n",
        "AGENTS.md": "# Agent Instructions\n\nRead `.ai/` memory before making changes.\n",
    }
    for path, content in files.items():
        dst = repo / path
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8")
