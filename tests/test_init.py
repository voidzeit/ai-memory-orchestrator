from amo.core.init import init_repo


def test_init_repo_creates_ai_memory(tmp_path):
    init_repo(tmp_path)
    assert (tmp_path / ".ai" / "state.md").exists()
    assert (tmp_path / ".ai" / "manifest.yaml").exists()
    assert (tmp_path / "AGENTS.md").exists()
