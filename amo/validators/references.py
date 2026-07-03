from pathlib import Path


def check_missing_canonical_files(repo: Path, canonical_files: list[str]) -> list[str]:
    warnings = []
    for rel in canonical_files:
        if not (repo / ".ai" / rel).exists():
            warnings.append(f"Missing canonical memory file: .ai/{rel}")
    return warnings
