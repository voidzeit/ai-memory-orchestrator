import json

import pytest

from amo.core.init import init_repo
from amo.core.scan import scan_repo
from amo.core.validate import validate_repo
from amo.evidence.ledger import read_ledger, record_evidence
from amo.evidence.schema import EvidenceEntry


def test_record_evidence_appends_jsonl(tmp_path):
    record_evidence(tmp_path, "scan", "amo scan", "1 file indexed", 0.9)
    record_evidence(tmp_path, "validation", "amo validate", "green", 0.9)
    ledger = tmp_path / ".ai" / "evidence" / "ledger.jsonl"
    lines = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert [entry["kind"] for entry in lines] == ["scan", "validation"]
    assert all(entry["timestamp"] for entry in lines)


def test_ledger_directory_gets_readme(tmp_path):
    record_evidence(tmp_path, "scan", "amo scan", "ok", 0.9)
    readme = tmp_path / ".ai" / "evidence" / "README.md"
    assert "append-only" in readme.read_text(encoding="utf-8")


def test_unknown_kind_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="Unknown evidence kind"):
        record_evidence(tmp_path, "guess", "amo guess", "ok", 0.9)


def test_authority_bounds_are_enforced():
    with pytest.raises(ValueError, match="authority"):
        EvidenceEntry(kind="scan", source="amo scan", result="ok", authority=1.5)


def test_scan_and_validate_write_ledger_entries(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    validate_repo(tmp_path, strict=False)
    kinds = [entry["kind"] for entry in read_ledger(tmp_path)]
    assert "scan" in kinds
    assert "validation" in kinds


def test_ledger_grows_across_runs(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    scan_repo(tmp_path)
    first = len(read_ledger(tmp_path))
    scan_repo(tmp_path)
    assert len(read_ledger(tmp_path)) > first


def test_read_ledger_empty_when_missing(tmp_path):
    assert read_ledger(tmp_path) == []
