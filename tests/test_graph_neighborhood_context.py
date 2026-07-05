import json

from amo.context.explain import explain_selection
from amo.context.graph_neighborhood import graph_proximity, lexical_seed_paths
from amo.context.ranking import rank_units
from amo.core.context import build_context_pack
from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.io import write_text

GRAPH = {
    "schema_version": "0.2",
    "nodes": [
        {"id": "file:app/auth.py", "type": "file", "path": "app/auth.py"},
        {"id": "file:app/session.py", "type": "file", "path": "app/session.py"},
        {"id": "file:docs/far.md", "type": "file", "path": "docs/far.md"},
        {"id": "dir:app", "type": "directory", "path": "app"},
    ],
    "edges": [
        {"source": "dir:app", "target": "file:app/auth.py", "type": "contains"},
        {"source": "dir:app", "target": "file:app/session.py", "type": "contains"},
        {"source": "file:app/session.py", "target": "file:docs/far.md", "type": "documents"},
    ],
}


def test_proximity_decays_per_hop():
    proximity = graph_proximity(GRAPH, ["app/auth.py"], max_hops=2, distance_decay=0.5)
    assert proximity["app/auth.py"] == 1.0
    assert proximity["app/session.py"] == 0.25  # two hops via dir:app
    assert "docs/far.md" not in proximity  # three hops away


def test_max_hops_bounds_expansion():
    proximity = graph_proximity(GRAPH, ["app/auth.py"], max_hops=1, distance_decay=0.5)
    assert set(proximity) == {"app/auth.py"}


def test_lexical_seeds_rank_by_relevance():
    units = [
        {"title": "app/auth.py", "summary": "auth logic", "tags": [], "expand": "app/auth.py"},
        {"title": "docs/far.md", "summary": "unrelated", "tags": [], "expand": "docs/far.md"},
    ]
    assert lexical_seed_paths(units, "fix auth bug", top_k=5) == ["app/auth.py"]


def test_proximity_boosts_ranking():
    units = [
        {"title": "a.py", "summary": "x", "tags": [], "tokens": 10, "expand": "a.py"},
        {"title": "b.py", "summary": "x", "tags": [], "tokens": 10, "expand": "b.py"},
    ]
    proximity = {"b.py": 1.0}
    selected = rank_units(units, task="unrelated-task", budget=15, proximity=proximity, params={"context.graph_weight": 3.0})
    assert selected[0]["expand"] == "b.py"


def test_explanations_include_reasons_and_proximity():
    selected = [
        {"title": "app/auth.py", "summary": "auth", "tags": [], "tokens": 10, "expand": "app/auth.py", "authority": 0.9, "score": 0.5},
    ]
    explained = explain_selection(selected, task="fix auth", proximity={"app/auth.py": 1.0}, seeds=["app/auth.py"])
    assert explained[0]["reasons"] == ["task relevance", "graph seed", "high authority"]
    assert explained[0]["graph_proximity"] == 1.0


def test_pack_includes_neighborhood_and_explain_artifact(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    write_text(tmp_path / "app" / "auth.py", "def authenticate():\n    return False\n")
    write_text(tmp_path / "app" / "session.py", "def start():\n    return None\n")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    pack = build_context_pack(tmp_path, task="fix auth bug", profile="quick")
    content = pack.read_text(encoding="utf-8")
    assert "## Graph Neighborhood" in content
    explain = json.loads((tmp_path / ".ai" / "machine" / "context_explain.json").read_text(encoding="utf-8"))
    assert explain["task"] == "fix auth bug"
    assert explain["selection"]
    assert all("reasons" in item for item in explain["selection"])


def test_pack_still_builds_without_graph(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    pack = build_context_pack(tmp_path, task="fix auth bug", profile="quick")
    assert pack.exists()
