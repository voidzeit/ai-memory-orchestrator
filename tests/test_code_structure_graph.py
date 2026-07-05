import json

from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo


def test_python_modules_symbols_and_imports_are_added(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("import json\n\nclass App:\n    pass\n\ndef run():\n    return json.dumps({})\n", encoding="utf-8")
    scan_repo(tmp_path)

    graph = json.loads(build_graph(tmp_path).read_text(encoding="utf-8"))
    by_id = {node["id"]: node for node in graph["nodes"]}

    assert by_id["module:app"]["level"] == "L2"
    assert "symbol:app:App" in by_id
    assert "symbol:app:run" in by_id
    assert any(edge["source"] == "module:app" and edge["target"] == "module:json" and edge["type"] == "depends_on" for edge in graph["edges"])


def test_python_parse_failure_does_not_break_graph_build(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    scan_repo(tmp_path)

    assert build_graph(tmp_path).exists()
