from pathlib import Path

TEXT_SUFFIXES = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".js", ".ts", ".tsx", ".jsx", ".cs"}


def build_file_index(repo: Path, excludes: set[str]) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    for path in repo.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(repo).as_posix()
        if any(part in excludes for part in path.relative_to(repo).parts):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"AGENTS.md", "LICENSE"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append({"path": rel, "suffix": path.suffix, "size": path.stat().st_size, "lines": len(text.splitlines())})
    return sorted(files, key=lambda item: str(item["path"]))
