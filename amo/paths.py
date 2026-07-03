from pathlib import Path

AI_DIR = ".ai"
MACHINE_DIR = "machine"
PACKS_DIR = "packs"
RUNTIME_DIR = "runtime"
CANONICAL_FILES = ["manifest.yaml", "state.md", "decisions.md", "tasks.md", "tests.md", "graph.md"]


def ai_path(repo: Path, *parts: str) -> Path:
    return repo / AI_DIR / Path(*parts)


def ensure_dirs(repo: Path) -> None:
    ai_path(repo).mkdir(parents=True, exist_ok=True)
    ai_path(repo, MACHINE_DIR).mkdir(parents=True, exist_ok=True)
    ai_path(repo, PACKS_DIR).mkdir(parents=True, exist_ok=True)
    ai_path(repo, RUNTIME_DIR).mkdir(parents=True, exist_ok=True)
