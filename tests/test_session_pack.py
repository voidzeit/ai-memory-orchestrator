from amo.core.handoff import build_handoff
from amo.core.init import init_repo


def test_session_pack_is_written(tmp_path):
    init_repo(tmp_path)
    path = build_handoff(tmp_path, task="fix tests", summary="next step")
    assert path.exists()
    assert (tmp_path / ".ai" / "packs" / "handoff.md").exists()
    assert (tmp_path / ".ai" / "runtime" / "session_handoff.md").exists()
