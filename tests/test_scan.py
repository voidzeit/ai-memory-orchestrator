import json

from amo.core.init import init_repo
from amo.core.scan import scan_repo


def test_scan_writes_indexes(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    result = scan_repo(tmp_path)
    assert result["files_indexed"] >= 1
    assert (tmp_path / ".ai" / "machine" / "files.json").exists()
    assert (tmp_path / ".ai" / "machine" / "context_units.json").exists()


def test_scan_does_not_exclude_project_runtime_folder(tmp_path):
    init_repo(tmp_path)
    runtime_dir = tmp_path / "runtime"
    runtime_dir.mkdir()
    (runtime_dir / "engine.py").write_text("print('runtime')\n", encoding="utf-8")
    scan_repo(tmp_path)
    files = json.loads((tmp_path / ".ai" / "machine" / "files.json").read_text())
    paths = {item["path"] for item in files["files"]}
    assert "runtime/engine.py" in paths


def test_scan_excludes_amo_runtime_folder(tmp_path):
    init_repo(tmp_path)
    amo_runtime = tmp_path / ".ai" / "runtime"
    amo_runtime.mkdir(parents=True, exist_ok=True)
    (amo_runtime / "cache.md").write_text("temporary\n", encoding="utf-8")
    scan_repo(tmp_path)
    files = json.loads((tmp_path / ".ai" / "machine" / "files.json").read_text())
    paths = {item["path"] for item in files["files"]}
    assert ".ai/runtime/cache.md" not in paths
