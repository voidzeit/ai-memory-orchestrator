from amo.core.context import build_context_pack
from amo.core.init import init_repo
from amo.core.scan import scan_repo


def test_context_pack_is_generated(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    pack = build_context_pack(tmp_path, task="fix app", profile="quick")
    assert pack.exists()
    text = pack.read_text(encoding="utf-8")
    assert "AMO Context Pack" in text
    assert "fix app" in text
