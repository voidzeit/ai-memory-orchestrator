from pathlib import Path


def check_runtime_pollution(repo: Path) -> list[str]:
    runtime = repo / ".ai" / "runtime"
    if not runtime.exists():
        return []
    leaked = [path for path in runtime.rglob("*") if path.is_file() and path.name != ".gitkeep"]
    if leaked:
        return ["Runtime files exist; ensure `.ai/runtime/` is gitignored."]
    return []
