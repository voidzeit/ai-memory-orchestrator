import shutil
from pathlib import Path

from amo.validators.json_schema import check_graph_schema


FIXTURES = Path(__file__).parent / "fixtures"
SCHEMA = Path("schemas/amo-graph.schema.json")


def _schema_repo(tmp_path: Path, fixture: str) -> Path:
    graph_dir = tmp_path / ".ai" / "machine"
    schema_dir = tmp_path / "schemas"
    graph_dir.mkdir(parents=True)
    schema_dir.mkdir()
    shutil.copyfile(FIXTURES / fixture, graph_dir / "graph.json")
    shutil.copyfile(SCHEMA, schema_dir / SCHEMA.name)
    return tmp_path


def test_checked_in_schema_accepts_valid_graph_fixture(tmp_path):
    repo = _schema_repo(tmp_path, "graph_valid.json")

    assert check_graph_schema(repo) == []


def test_checked_in_schema_rejects_graph_missing_node_id(tmp_path):
    repo = _schema_repo(tmp_path, "graph_invalid_missing_id.json")

    errors = check_graph_schema(repo)

    assert len(errors) == 1
    assert "$.nodes[0]" in errors[0]
    assert "'id' is a required property" in errors[0]
