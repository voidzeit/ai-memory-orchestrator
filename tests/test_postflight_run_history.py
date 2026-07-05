import json
import time

import pytest

from amo.core.init import init_repo
from amo.core.postflight import apply_postflight
from amo.runtime.lock import LockHeldError, acquire_lock, lock_path, memory_lock
from amo.runtime.run_history import slugify


def _repo(tmp_path):
    init_repo(repo=tmp_path, template="generic")
    return tmp_path


def test_postflight_writes_run_note_and_mirror(tmp_path):
    repo = _repo(tmp_path)
    apply_postflight(repo, task="fix auth", summary="fixed", outcome="completed")
    notes = list((repo / ".ai" / "runs").rglob("*-fix-auth.md"))
    mirrors = list((repo / ".ai" / "machine" / "run_history").glob("*-fix-auth.json"))
    assert len(notes) == 1
    assert len(mirrors) == 1
    mirror = json.loads(mirrors[0].read_text(encoding="utf-8"))
    assert mirror["outcome"] == "completed"
    assert mirror["note"].startswith(".ai/runs/")


def test_postflight_updates_state_and_tasks(tmp_path):
    repo = _repo(tmp_path)
    apply_postflight(repo, task="fix auth", summary="fixed")
    assert "fix auth" in (repo / ".ai" / "tasks.md").read_text(encoding="utf-8")
    assert "fix auth" in (repo / ".ai" / "state.md").read_text(encoding="utf-8")


def test_decision_appended_only_when_provided(tmp_path):
    repo = _repo(tmp_path)
    before = (repo / ".ai" / "decisions.md").read_text(encoding="utf-8")
    apply_postflight(repo, task="a", summary="b")
    assert (repo / ".ai" / "decisions.md").read_text(encoding="utf-8") == before
    apply_postflight(repo, task="a", summary="b", decision="Use dependency-free locks.")
    assert "Use dependency-free locks." in (repo / ".ai" / "decisions.md").read_text(encoding="utf-8")


def test_validation_appended_to_tests_when_provided(tmp_path):
    repo = _repo(tmp_path)
    apply_postflight(repo, task="a", summary="b", validation="pytest passed")
    assert "pytest passed" in (repo / ".ai" / "tests.md").read_text(encoding="utf-8")


def test_backup_created_before_mutation(tmp_path):
    repo = _repo(tmp_path)
    apply_postflight(repo, task="a", summary="b")
    backups = list((repo / ".ai" / "runtime" / "backups").iterdir())
    assert len(backups) == 1
    assert (backups[0] / "state.md").exists()


def test_lock_released_after_postflight(tmp_path):
    repo = _repo(tmp_path)
    apply_postflight(repo, task="a", summary="b")
    assert not lock_path(repo).exists()


def test_held_lock_blocks_postflight(tmp_path):
    repo = _repo(tmp_path)
    acquire_lock(repo)
    with pytest.raises(LockHeldError):
        apply_postflight(repo, task="a", summary="b")
    assert lock_path(repo).exists()


def test_stale_lock_is_replaced(tmp_path):
    repo = _repo(tmp_path)
    acquire_lock(repo)
    time.sleep(0.01)
    with memory_lock(repo, stale_after=0.001):
        pass
    assert not lock_path(repo).exists()


def test_slugify_is_filesystem_safe():
    assert slugify("Fix: failing AUTH tests!") == "fix-failing-auth-tests"
    assert slugify("///") == "run"
