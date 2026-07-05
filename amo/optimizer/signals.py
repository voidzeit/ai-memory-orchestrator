from __future__ import annotations

import json
from pathlib import Path

from amo.config import get_config_value, load_config
from amo.context.profiles import get_budget
from amo.paths import CANONICAL_FILES
from amo.validators.artifacts import check_runtime_pollution

SEVERITIES = ("high", "medium", "low")


def _finding(
    finding_id: str,
    severity: str,
    layer: str,
    message: str,
    evidence: list[str],
    recommendation: str,
    impact: dict[str, float],
) -> dict[str, object]:
    return {
        "id": finding_id,
        "severity": severity,
        "layer": layer,
        "message": message,
        "evidence": evidence,
        "recommendation": recommendation,
        "impact": impact,
    }


def collect_signals(repo: Path) -> list[dict[str, object]]:
    """Collect deterministic, propose-only findings. No LLM, no autofix."""
    repo = repo.resolve()
    findings: list[dict[str, object]] = []
    findings.extend(_graph_signals(repo))
    findings.extend(_context_signals(repo))
    findings.extend(_memory_signals(repo))
    findings.extend(_benchmark_signals(repo))
    findings.extend(_runtime_signals(repo))
    findings.extend(_adapter_signals(repo))
    return findings


def _graph_signals(repo: Path) -> list[dict[str, object]]:
    path = repo / ".ai" / "machine" / "graph.json"
    if not path.exists():
        return [
            _finding(
                "graph_missing",
                "medium",
                "graph",
                "No graph index found.",
                [".ai/machine/graph.json missing"],
                "Run `amo graph build`.",
                {"graph_truthfulness": -0.3},
            )
        ]
    graph = json.loads(path.read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_ids = {node.get("id") for node in nodes}
    findings = []

    seen: set[tuple[object, object, object]] = set()
    duplicates = 0
    for edge in edges:
        key = (edge.get("source"), edge.get("target"), edge.get("type"))
        if key in seen:
            duplicates += 1
        seen.add(key)
    if duplicates:
        findings.append(
            _finding(
                "duplicate_graph_edges",
                "medium",
                "graph",
                f"{duplicates} duplicate edges found in graph.",
                [f"{duplicates} repeated (source, target, type) triples"],
                "Deduplicate edges during graph build.",
                {"graph_drift": 0.1, "token_cost": 0.05},
            )
        )

    dangling = [
        edge
        for edge in edges
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids
    ]
    if dangling:
        findings.append(
            _finding(
                "edge_references_missing_node",
                "high",
                "graph",
                f"{len(dangling)} edges reference nodes that do not exist.",
                [f"first: {dangling[0].get('source')} -> {dangling[0].get('target')}"],
                "Rebuild the graph; if it persists, fix the offending extractor.",
                {"graph_truthfulness": -0.3},
            )
        )

    referenced = {edge.get("source") for edge in edges} | {edge.get("target") for edge in edges}
    orphans = [node["id"] for node in nodes if node.get("id") not in referenced and node.get("type") != "repository"]
    if orphans:
        findings.append(
            _finding(
                "orphan_nodes",
                "low",
                "graph",
                f"{len(orphans)} nodes have no edges.",
                [f"first: {orphans[0]}"],
                "Connect orphan nodes or drop them from the build.",
                {"graph_drift": 0.05},
            )
        )

    has_python_files = any(str(node.get("path", "")).endswith(".py") for node in nodes if node.get("type") == "file")
    has_symbols = any(node.get("type") in {"module", "symbol"} for node in nodes)
    if has_python_files and not has_symbols:
        findings.append(
            _finding(
                "missing_symbol_nodes",
                "medium",
                "graph",
                "Python files exist but the graph has no module or symbol nodes.",
                ["no nodes of type module/symbol in graph.json"],
                "Run `amo graph build` with structure extraction enabled.",
                {"graph_truthfulness": -0.2, "useful_context_per_token": -0.1},
            )
        )

    tested = {edge.get("source") for edge in edges if edge.get("type") == "tested_by"}
    untested = [
        node["id"]
        for node in nodes
        if node.get("type") == "file"
        and str(node.get("path", "")).endswith(".py")
        and not str(node.get("path", "")).startswith("tests/")
        and node.get("id") not in tested
    ]
    if untested:
        findings.append(
            _finding(
                "missing_test_edges",
                "low",
                "graph",
                f"{len(untested)} Python files have no tested_by edge.",
                [f"first: {untested[0]}"],
                "Add tests or map existing tests to their subjects.",
                {"validation_confidence": -0.1},
            )
        )
    return findings


def _context_signals(repo: Path) -> list[dict[str, object]]:
    packs_dir = repo / ".ai" / "packs"
    packs = sorted(packs_dir.glob("*.md")) if packs_dir.exists() else []
    if not packs:
        return [
            _finding(
                "missing_context_pack",
                "medium",
                "context",
                "No compiled context pack found.",
                [".ai/packs/ has no .md files"],
                "Run `amo preflight --task <task> --profile quick`.",
                {"useful_context_per_token": -0.2},
            )
        ]
    findings = []
    config = load_config(repo)
    for pack in packs:
        content = pack.read_text(encoding="utf-8")
        profile = pack.stem
        budget = get_budget(profile, config=config)
        estimated_tokens = len(content) // 4
        if estimated_tokens > budget:
            findings.append(
                _finding(
                    "context_pack_over_budget",
                    "medium",
                    "context",
                    f"Pack {pack.name} is ~{estimated_tokens} tokens; budget is {budget}.",
                    [f".ai/packs/{pack.name}"],
                    "Lower context.max_units or raise the profile budget deliberately.",
                    {"token_cost": 0.2},
                )
            )
        if "amo validate" not in content:
            findings.append(
                _finding(
                    "missing_validation_commands",
                    "low",
                    "context",
                    f"Pack {pack.name} does not tell the agent how to validate.",
                    [f".ai/packs/{pack.name}"],
                    "Regenerate the pack with a current AMO version.",
                    {"validation_confidence": -0.1},
                )
            )
    return findings


def _memory_signals(repo: Path) -> list[dict[str, object]]:
    findings = []
    missing = [name for name in CANONICAL_FILES if not (repo / ".ai" / name).exists()]
    if missing:
        findings.append(
            _finding(
                "missing_canonical_memory",
                "high",
                "memory",
                f"Missing canonical memory files: {', '.join(missing)}.",
                [f".ai/{name} missing" for name in missing],
                "Run `amo init` or restore the files from history.",
                {"memory_durability": -0.4},
            )
        )
    for name, finding_id in (("decisions.md", "empty_decisions"), ("tests.md", "empty_tests")):
        path = repo / ".ai" / name
        if path.exists():
            body = "\n".join(
                line for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")
            )
            if not body:
                findings.append(
                    _finding(
                        finding_id,
                        "medium",
                        "memory",
                        f".ai/{name} has headers but no durable content.",
                        [f".ai/{name} body is empty"],
                        f"Record real project knowledge in .ai/{name}.",
                        {"memory_durability": -0.2},
                    )
                )
    return findings


def _benchmark_signals(repo: Path) -> list[dict[str, object]]:
    path = repo / ".ai" / "machine" / "benchmark.json"
    if not path.exists():
        return [
            _finding(
                "benchmark_missing",
                "medium",
                "benchmark",
                "No benchmark result found.",
                [".ai/machine/benchmark.json missing"],
                "Run `amo benchmark` with a fixture.",
                {"useful_context_per_token": -0.2, "validation_confidence": 0.0},
            )
        ]
    metrics = json.loads(path.read_text(encoding="utf-8")).get("metrics", {})
    findings = []
    precision = metrics.get("file_selection_precision")
    recall = metrics.get("file_selection_recall")
    if not isinstance(precision, (int, float)) or not isinstance(recall, (int, float)):
        findings.append(
            _finding(
                "benchmark_unscored_precision_recall",
                "low",
                "benchmark",
                "Benchmark precision/recall are unscored.",
                ["file_selection_precision or file_selection_recall is not numeric"],
                "Add fixture ground truth (truth.json) and rerun `amo benchmark`.",
                {"validation_confidence": -0.1},
            )
        )
    config = load_config(repo)
    minimum = float(get_config_value(config, "benchmark.min_token_reduction", 0.5))
    reduction = metrics.get("token_reduction")
    if isinstance(reduction, (int, float)) and reduction < minimum:
        findings.append(
            _finding(
                "low_token_reduction",
                "medium",
                "benchmark",
                f"Token reduction {reduction} is below the minimum {minimum}.",
                [".ai/machine/benchmark.json"],
                "Tune context parameters with `amo optimize params sweep`.",
                {"token_cost": 0.3},
            )
        )
    return findings


def _runtime_signals(repo: Path) -> list[dict[str, object]]:
    findings = []
    for warning in check_runtime_pollution(repo):
        if "not ignored" in warning:
            finding_id, severity = "runtime_not_ignored", "high"
        elif "tracked by Git" in warning:
            finding_id, severity = "runtime_tracked", "high"
        elif "leaked into derived output" in warning:
            finding_id, severity = "runtime_leak_to_machine_or_packs", "high"
        else:
            finding_id, severity = "runtime_unknown_file", "low"
        findings.append(
            _finding(
                finding_id,
                severity,
                "runtime",
                warning,
                [warning],
                "Keep `.ai/runtime/` disposable, ignored, and free of durable truth.",
                {"memory_durability": -0.2},
            )
        )
    return findings


def _adapter_signals(repo: Path) -> list[dict[str, object]]:
    if (repo / "AGENTS.md").exists():
        return []
    return [
        _finding(
            "missing_agent_adapter_output",
            "low",
            "adapter",
            "No AGENTS.md adapter output found at the repository root.",
            ["AGENTS.md missing"],
            "Run `amo export --target agents`.",
            {"interoperability": -0.1},
        )
    ]
