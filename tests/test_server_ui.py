import pytest
from fastapi.testclient import TestClient

from amo.core.graph import build_graph
from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.core.validate import validate_repo
from amo.server.app import create_app


@pytest.fixture()
def client(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    build_graph(tmp_path)
    validate_repo(tmp_path)
    return TestClient(create_app(tmp_path))


def test_index_serves_organism_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "AMO" in response.text
    assert "Organism" in response.text


def test_organism_snapshot_endpoint(client):
    snapshot = client.get("/api/organism").json()
    assert snapshot["status"] in {"green", "yellow", "red", "unknown"}
    assert snapshot["graph"]["nodes"] > 0
    assert "adapters" in snapshot


def test_validation_endpoint(client):
    assert client.get("/api/validation").json()["status"] in {"green", "yellow", "red"}


def test_benchmark_missing_returns_404(client):
    assert client.get("/api/benchmark").status_code == 404


def test_context_flow_returns_pack_and_explanation(client):
    response = client.post("/api/context", json={"task": "fix failing tests", "profile": "quick"})
    body = response.json()
    assert response.status_code == 200
    assert body["pack"] == ".ai/packs/quick.md"
    assert "AMO Context Pack" in body["content"]
    assert body["explanation"]["task"] == "fix failing tests"


def test_postflight_requires_confirm(client):
    response = client.post("/api/postflight", json={"task": "t", "summary": "s"})
    assert response.status_code == 400


def test_confirmed_postflight_applies(client):
    response = client.post("/api/postflight", json={"task": "t", "summary": "done", "confirm": True})
    assert response.status_code == 200
    assert response.json()["status"] == "applied"


def test_ledger_endpoint_lists_entries(client):
    body = client.get("/api/ledger").json()
    assert body["total"] >= 1
    assert body["entries"]


def test_token_gate_when_required(tmp_path, monkeypatch):
    monkeypatch.setenv("AMO_SERVER_TOKEN", "secret")
    init_repo(repo=tmp_path, template="generic")
    client = TestClient(create_app(tmp_path, require_token=True))
    assert client.get("/api/organism").status_code == 401
    assert client.get("/api/organism", headers={"x-amo-token": "secret"}).status_code == 200
