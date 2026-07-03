from pathlib import Path

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".cs",
}
SPECIAL_TEXT_FILES = {"AGENTS.md", "LICENSE"}


def build_file_index(repo: Path, excludes: set[str]) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    for path in repo.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(repo).as_posix()
        if _is_excluded(path.relative_to(repo), rel, excludes):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in SPECIAL_TEXT_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append(
            {
                "path": rel,
                "suffix": path.suffix,
                "size": path.stat().st_size,
                "lines": len(text.splitlines()),
            }
        )
    return sorted(files, key=lambda item: str(item["path"]))


def _is_excluded(rel_path: Path, rel: str, excludes: set[str]) -> bool:
    for exclude in excludes:
        normalized = exclude.strip("/")
        if rel == normalized or rel.startswith(f"{normalized}/"):
            return True
        if normalized in rel_path.parts and "/" not in normalized:
            return True
    return False
