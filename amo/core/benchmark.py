from __future__ import annotations

import json
from pathlib import Path

from amo.core.context import build_context_pack
from amo.core.scan import scan_repo
from amo.evidence.ledger import record_evidence
from amo.io import write_json

UNSCORED = "not_scored_without_fixture_truth"


def load_truth(repo: Path) -> dict[str, object] | None:
    path = repo / "truth.json"
    if not path.exists():
        return None
    truth = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(truth, dict):
        raise ValueError("truth.json must contain a JSON object")
    return truth


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
    selected = _selected_paths(repo, files, pack)
    total_tokens = max(1, sum(int(item.get("size", 0)) for item in files) // 4)
    pack_tokens = max(1, len(pack) // 4)

    metrics: dict[str, object] = {
        "token_reduction": round(max(0.0, 1 - pack_tokens / total_tokens), 4),
        "file_selection_precision": None,
        "file_selection_recall": None,
        "test_command_accuracy": UNSCORED,
        "handoff_quality": UNSCORED,
        "context_section_coverage": None,
        "must_not_include_violations": None,
        "selected_files": len(selected),
    }
    truth = load_truth(repo)
    if truth is not None:
        metrics.update(_score_against_truth(truth, selected, pack))

    result = {"task": task, "files_indexed": scan["files_indexed"], "metrics": metrics}
    output = repo / ".ai" / "machine" / "benchmark.json"
    write_json(output, result)
    record_evidence(
        repo,
        kind="benchmark",
        source="amo benchmark",
        result=f"token_reduction={metrics['token_reduction']}",
        authority=0.9,
        artifacts=(".ai/machine/benchmark.json",),
        limitations=(
            ("scored against truth.json fixture ground truth",)
            if truth is not None
            else ("precision/recall unscored without fixture ground truth",)
        ),
    )
    return output


def _selected_paths(repo: Path, files: list[dict[str, object]], pack: str) -> set[str]:
    """Prefer the compiler's explained selection; fall back to pack-text matching."""
    explain_path = repo / ".ai" / "machine" / "context_explain.json"
    if explain_path.exists():
        explain = json.loads(explain_path.read_text(encoding="utf-8"))
        paths = {str(item.get("path")) for item in explain.get("selection", []) if item.get("path")}
        if paths:
            return paths
    return {str(item["path"]) for item in files if str(item["path"]) in pack}


def _score_against_truth(
    truth: dict[str, object],
    selected: set[str],
    pack: str,
) -> dict[str, object]:
    scored: dict[str, object] = {}
    relevant = {str(path) for path in truth.get("relevant_files", []) if path}
    if relevant:
        relevant_selected = len(selected & relevant)
        scored["file_selection_precision"] = round(relevant_selected / len(selected), 4) if selected else 0.0
        scored["file_selection_recall"] = round(relevant_selected / len(relevant), 4)
    expected_tests = [str(command) for command in truth.get("expected_tests", []) if command]
    if expected_tests:
        scored["test_command_accuracy"] = round(
            sum(command in pack for command in expected_tests) / len(expected_tests), 4
        )
    sections = [str(section) for section in truth.get("expected_context_sections", []) if section]
    if sections:
        scored["context_section_coverage"] = round(
            sum(section in pack for section in sections) / len(sections), 4
        )
    banned = [str(item) for item in truth.get("must_not_include", []) if item]
    scored["must_not_include_violations"] = sum(item in pack for item in banned)
    return scored
