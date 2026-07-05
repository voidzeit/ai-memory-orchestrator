import json

from amo.validators.graph import check_graph_contract


def _write_graph(tmp_path, graph):
    path = tmp_path / ".ai" / "machine" / "graph.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(graph), encoding="utf-8")


def test_valid_graph_passes(tmp_path):
    _write_graph(tmp_path, {"schema_version": "0.2", "nodes": [{"id": "a", "type": "file", "label": "a"}], "edges": []})
    assert check_graph_contract(tmp_path) == []


def test_missing_node_id_fails(tmp_path):
    _write_graph(tmp_path, {"schema_version": "0.2", "nodes": [{"type": "file", "label": "a"}], "edges": []})
    assert any("`id`" in error for error in check_graph_contract(tmp_path))


def test_edge_with_missing_target_fails(tmp_path):
    _write_graph(tmp_path, {"schema_version": "0.2", "nodes": [{"id": "a", "type": "file", "label": "a"}], "edges": [{"source": "a", "target": "b", "type": "references"}]})
    assert any("missing node `b`" in error for error in check_graph_contract(tmp_path))


def test_duplicate_node_id_fails(tmp_path):
    node = {"id": "a", "type": "file", "label": "a"}
    _write_graph(tmp_path, {"schema_version": "0.2", "nodes": [node, node], "edges": []})
    assert any("duplicate node id `a`" in error for error in check_graph_contract(tmp_path))
