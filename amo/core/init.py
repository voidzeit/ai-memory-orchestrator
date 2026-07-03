from pathlib import Path
import shutil

from amo.paths import ensure_dirs


def init_repo(repo: Path, template: str = "generic") -> str:
    repo = repo.resolve()
    ensure_dirs(repo)

    templates_root = Path(__file__).resolve().parents[2] / "templates"
    generic_root = templates_root / "generic"
    selected_root = templates_root / template

    if not generic_root.exists():
        _write_embedded_default(repo)
    else:
        _copy_template(generic_root, repo, overwrite=False)

    if template != "generic" and selected_root.exists():
        _copy_template(selected_root, repo, overwrite=True)

    gitignore = repo / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if ".ai/runtime/" not in current:
        gitignore.write_text(current.rstrip() + "\n.ai/runtime/\n", encoding="utf-8")

    if not (repo / ".amo.yaml").exists():
        (repo / ".amo.yaml").write_text(
            "version: 0.1\nmemory:\n  source_of_truth: .ai\n",
            encoding="utf-8",
        )

    return str(repo / ".ai")


def _copy_template(template_root: Path, repo: Path, overwrite: bool) -> None:
    for src in template_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(template_root)
        dst = repo / rel
        if dst.exists() and not overwrite:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)


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
