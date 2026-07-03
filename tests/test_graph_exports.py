from amo.core.graph import build_graph, export_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo


def test_graph_build_has_schema_version(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    path = build_graph(tmp_path)
    text = path.read_text(encoding="utf-8")
    assert "schema_version" in text
    assert "repo:" in text


def test_graph_export_neo4j(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    path = export_graph(tmp_path, "neo4j")
    text = path.read_text(encoding="utf-8")
    assert "CREATE CONSTRAINT" in text
    assert "AMONode" in text


def test_graph_export_obsidian(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    output = export_graph(tmp_path, "obsidian")
    assert (output / "index.md").exists()
