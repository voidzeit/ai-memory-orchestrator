from pathlib import Path

from amo.paths import ai_path


def get_status(repo: Path) -> dict[str, object]:
    repo = repo.resolve()
    checks = {
        "memory": "ok" if ai_path(repo).exists() else "missing",
        "manifest": "ok" if ai_path(repo, "manifest.yaml").exists() else "missing",
        "state": "ok" if ai_path(repo, "state.md").exists() else "missing",
        "context_units": "ok" if ai_path(repo, "machine", "context_units.json").exists() else "missing",
        "graph": "ok" if ai_path(repo, "machine", "graph.json").exists() else "missing",
        "validation": "ok" if ai_path(repo, "machine", "validation.json").exists() else "missing",
    }
    status = "green" if all(value == "ok" for value in checks.values()) else "yellow"
    return {"status": status, "checks": checks}
