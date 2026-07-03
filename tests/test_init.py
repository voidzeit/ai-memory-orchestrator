from amo.core.init import init_repo
from amo.core.validate import validate_repo


def test_init_repo_creates_ai_memory(tmp_path):
    init_repo(tmp_path)
    assert (tmp_path / ".ai" / "state.md").exists()
    assert (tmp_path / ".ai" / "manifest.yaml").exists()
    assert (tmp_path / "AGENTS.md").exists()


def test_python_template_inherits_generic_memory(tmp_path):
    init_repo(tmp_path, template="python")
    assert (tmp_path / ".ai" / "state.md").exists()
    assert (tmp_path / ".ai" / "decisions.md").exists()
    assert (tmp_path / ".ai" / "tasks.md").exists()
    assert (tmp_path / ".ai" / "tests.md").exists()
    assert (tmp_path / ".ai" / "graph.md").exists()
    assert (tmp_path / ".ai" / "manifest.yaml").exists()
    result = validate_repo(tmp_path, strict=True)
    assert result["status"] == "green"
