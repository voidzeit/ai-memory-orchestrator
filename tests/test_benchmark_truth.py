import json

from amo.core.benchmark import run_benchmark
from amo.core.init import init_repo
from amo.io import write_json, write_text


def _fixture_repo(tmp_path, truth=None):
    init_repo(repo=tmp_path, template="generic")
    write_text(tmp_path / "app" / "auth.py", "def authenticate():\n    return False\n")
    write_text(tmp_path / "app" / "payments.py", "def charge():\n    return 0\n")
    write_text(tmp_path / "tests" / "test_auth.py", "def test_auth():\n    assert True\n")
    if truth is not None:
        write_json(tmp_path / "truth.json", truth)
    return tmp_path


def _metrics(path):
    return json.loads(path.read_text(encoding="utf-8"))["metrics"]


def test_without_truth_precision_recall_stay_unscored(tmp_path):
    repo = _fixture_repo(tmp_path)
    metrics = _metrics(run_benchmark(repo, "fix failing auth tests"))
    assert metrics["file_selection_precision"] is None
    assert metrics["file_selection_recall"] is None
    assert metrics["test_command_accuracy"] == "not_scored_without_fixture_truth"


def test_with_truth_scores_precision_and_recall(tmp_path):
    repo = _fixture_repo(
        tmp_path,
        truth={
            "relevant_files": ["app/auth.py", "tests/test_auth.py"],
            "expected_tests": ["pytest tests/test_auth.py"],
            "must_not_include": [".ai/runtime/last_context.md"],
        },
    )
    metrics = _metrics(run_benchmark(repo, "fix failing auth tests"))
    assert 0.0 <= metrics["file_selection_precision"] <= 1.0
    assert 0.0 <= metrics["file_selection_recall"] <= 1.0
    assert isinstance(metrics["must_not_include_violations"], int)


def test_recall_is_full_when_all_relevant_files_selected(tmp_path):
    repo = _fixture_repo(tmp_path, truth={"relevant_files": ["app/auth.py", "tests/test_auth.py"]})
    metrics = _metrics(run_benchmark(repo, "fix failing auth tests"))
    assert metrics["file_selection_recall"] == 1.0


def test_must_not_include_detects_violations(tmp_path):
    repo = _fixture_repo(tmp_path, truth={"must_not_include": ["Current Truth"]})
    metrics = _metrics(run_benchmark(repo, "fix failing auth tests"))
    assert metrics["must_not_include_violations"] == 1


def test_expected_sections_scored(tmp_path):
    repo = _fixture_repo(
        tmp_path,
        truth={"expected_context_sections": ["Current Truth", "definitely-not-a-section"]},
    )
    metrics = _metrics(run_benchmark(repo, "fix failing auth tests"))
    assert metrics["context_section_coverage"] == 0.5
