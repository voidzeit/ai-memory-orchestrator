from pathlib import Path


def build_context_units(repo: Path, files: list[dict[str, object]]) -> list[dict[str, object]]:
    units: list[dict[str, object]] = []
    for item in files:
        path = str(item["path"])
        tags = [Path(path).suffix.lstrip(".") or Path(path).name]
        if path.startswith("amo/"):
            tags.append("implementation")
        if path.startswith("tests/"):
            tags.append("tests")
        if path.startswith("docs/"):
            tags.append("docs")
        if path.startswith(".ai/"):
            tags.append("memory")
        units.append({
            "id": f"file:{path}",
            "type": "file_summary",
            "title": path,
            "summary": f"Repository file `{path}` with {item['lines']} lines.",
            "tokens": max(12, int(item["lines"]) * 4),
            "authority": 0.9 if path.startswith(".ai/") else 0.7,
            "freshness": 1.0,
            "tags": tags,
            "expand": path,
        })
    return units
