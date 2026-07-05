import json

from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.optimize import optimize_check, optimize_plan, optimize_suggest
from amo.core.scan import scan_repo
from amo.io import write_json
from amo.optimizer.signals import collect_signals


def _prepared_repo(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    return tmp_path


def test_suggest_writes_cycle_findings_and_metrics(tmp_path):
    repo = _prepared_repo(tmp_path)
    output = optimize_suggest(repo)
    assert output.name == "cycle-0001.json"
    cycle = json.loads(output.read_text(encoding="utf-8"))
    assert cycle["mode"] == "suggest"
    assert cycle["auto_fix"] is False
    assert (repo / ".ai" / "evolution" / "findings.md").exists()
    metrics = json.loads((repo / ".ai" / "evolution" / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["findings_total"] == len(cycle["findings"])


def test_suggest_increments_cycle_number(tmp_path):
    repo = _prepared_repo(tmp_path)
    optimize_suggest(repo)
    second = optimize_suggest(repo)
    assert second.name == "cycle-0002.json"


def test_benchmark_missing_finding(tmp_path):
    repo = _prepared_repo(tmp_path)
    ids = {finding["id"] for finding in collect_signals(repo)}
    assert "benchmark_missing" in ids


def test_edge_references_missing_node_is_high(tmp_path):
    repo = _prepared_repo(tmp_path)
    graph_path = repo / ".ai" / "machine" / "graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["edges"].append({"source": "ghost:a", "target": "ghost:b", "type": "contains"})
    write_json(graph_path, graph)
    findings = {finding["id"]: finding for finding in collect_signals(repo)}
    assert findings["edge_references_missing_node"]["severity"] == "high"


def test_check_reports_action_required(tmp_path):
    repo = _prepared_repo(tmp_path)
    action_required, findings = optimize_check(repo)
    assert action_required is True
    assert any(finding["id"] == "benchmark_missing" for finding in findings)


def test_plan_lists_recommendations_by_priority(tmp_path):
    repo = _prepared_repo(tmp_path)
    output = optimize_plan(repo)
    content = output.read_text(encoding="utf-8")
    assert "Propose-only" in content
    assert "benchmark" in content


def test_findings_follow_contract(tmp_path):
    repo = _prepared_repo(tmp_path)
    for finding in collect_signals(repo):
        assert set(finding) == {"id", "severity", "layer", "message", "evidence", "recommendation", "impact"}
        assert finding["severity"] in {"high", "medium", "low"}
