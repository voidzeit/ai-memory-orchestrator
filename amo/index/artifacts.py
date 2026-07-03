from pathlib import Path


def build_artifact_index(repo: Path, files: list[dict[str, object]]) -> list[dict[str, object]]:
    artifacts = []
    for item in files:
        path = str(item["path"])
        artifact_type = "source"
        if path.startswith(".ai/machine/"):
            artifact_type = "machine-index"
        elif path.startswith(".ai/packs/"):
            artifact_type = "context-pack"
        elif path.startswith(".ai/"):
            artifact_type = "canonical-memory"
        artifacts.append({"path": path, "type": artifact_type, "repo": repo.name})
    return artifacts
