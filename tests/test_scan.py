from amo.core.init import init_repo
from amo.core.scan import scan_repo


def test_scan_writes_indexes(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    result = scan_repo(tmp_path)
    assert result["files_indexed"] >= 1
    assert (tmp_path / ".ai" / "machine" / "files.json").exists()
    assert (tmp_path / ".ai" / "machine" / "context_units.json").exists()
