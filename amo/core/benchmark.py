from __future__ import annotations

import json
from pathlib import Path

from amo.core.context import build_context_pack
from amo.core.scan import scan_repo
from amo.io import write_json


def run_benchmark(
    repo: Path,
    task: str,
    params: dict[str, object] | None = None,
    scan_excludes: set[str] | None = None,
) -> Path:
    repo = repo.resolve()
    scan = scan_repo(repo, extra_excludes=scan_excludes)
    pack_path = build_context_pack(repo, task=task, profile="quick", params=params)
    files = json.loads((repo / ".ai" / "machine" / "files.json").read_text(encoding="utf-8")).get("files", [])
    pack = pack_path.read_text(encoding="utf-8")
    selected = [item for item in files if str(item["path"]) in pack]
    total_tokens = max(1, sum(int(item.get("size", 0)) for item in files) // 4)
    pack_tokens = max(1, len(pack) // 4)
    result = {
        "task": task,
        "files_indexed": scan["files_indexed"],
        "metrics": {
            "token_reduction": round(max(0.0, 1 - pack_tokens / total_tokens), 4),
            "file_selection_precision": None,
            "file_selection_recall": None,
            "test_command_accuracy": "not_scored_without_fixture_truth",
            "handoff_quality": "not_scored_without_fixture_truth",
            "selected_files": len(selected),
        },
    }
    output = repo / ".ai" / "machine" / "benchmark.json"
    write_json(output, result)
    return output
