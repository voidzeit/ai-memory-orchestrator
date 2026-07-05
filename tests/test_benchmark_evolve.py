import json

from amo.core.benchmark import run_benchmark
from amo.core.evolve import evolve_safe
from amo.core.init import init_repo


def test_benchmark_writes_deterministic_metrics(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
    result = json.loads(run_benchmark(tmp_path, "fix failing tests").read_text(encoding="utf-8"))
    assert "token_reduction" in result["metrics"]
    assert result["metrics"]["test_command_accuracy"] == "not_scored_without_fixture_truth"


def test_evolve_is_safe_and_writes_expected_outputs(tmp_path):
    init_repo(tmp_path)
    cycle = evolve_safe(tmp_path)
    result = json.loads(cycle.read_text(encoding="utf-8"))
    assert result["mode"] == "safe"
    assert result["llm"] is False
    assert (tmp_path / ".ai" / "evolution" / "metrics.json").exists()
    assert (tmp_path / ".ai" / "evolution" / "findings.md").exists()
