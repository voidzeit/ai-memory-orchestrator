import json

from amo.core.graph import build_graph, export_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.graph.obsidian_rich import safe_note_name


def test_graph_build_has_schema_version(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    path = build_graph(tmp_path)
    text = path.read_text(encoding="utf-8")
    assert "schema_version" in text
    assert "repo:" in text


def test_graph_build_assigns_l0_and_l1_levels(tmp_path):
    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
    scan_repo(tmp_path)
    graph = json.loads(build_graph(tmp_path).read_text(encoding="utf-8"))

    assert any(node["type"] == "file" and node["level"] == "L0" for node in graph["nodes"])
    assert any(node["type"] == "memory" and node["level"] == "L1" for node in graph["nodes"])


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


def test_standard_graph_exports(tmp_path):
    from xml.etree import ElementTree as ET

    init_repo(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')\n", encoding="utf-8")
    scan_repo(tmp_path)
    build_graph(tmp_path)

    jsonld = json.loads(export_graph(tmp_path, "jsonld").read_text(encoding="utf-8"))
    assert jsonld["@context"] and jsonld["@graph"]
    assert ET.parse(export_graph(tmp_path, "graphml")).getroot().tag.endswith("graphml")
    assert ET.parse(export_graph(tmp_path, "gexf")).getroot().tag.endswith("gexf")


def test_obsidian_note_names_are_collision_safe():
    assert safe_note_name("file:a/b") != safe_note_name("file:a - b")
    assert len(safe_note_name("x" * 200).split("--")[0]) <= 80
