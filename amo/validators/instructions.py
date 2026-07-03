from pathlib import Path

DANGEROUS_PHRASES = ["ignore previous instructions", "exfiltrate", "send secrets", "disable validation"]


def check_unsafe_instructions(repo: Path) -> list[str]:
    warnings: list[str] = []
    for path in [repo / "AGENTS.md", repo / ".ai" / "state.md", repo / ".ai" / "tasks.md"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in DANGEROUS_PHRASES:
            if phrase in text:
                warnings.append(f"Possible unsafe instruction in {path.relative_to(repo)}: {phrase}")
    return warnings
