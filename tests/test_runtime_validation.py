import subprocess
from pathlib import Path

from amo.core.context import build_context_pack
from amo.core.handoff import build_handoff
from amo.core.init import init_repo
from amo.core.validate import validate_repo
from amo.validators.artifacts import check_runtime_pollution


def _git_repo(path: Path, *, ignore_runtime: bool = True) -> None:
    subprocess.run(["git", "init", "--quiet", str(path)], check=True)
    if ignore_runtime:
        (path / ".gitignore").write_text(".ai/runtime/\n", encoding="utf-8")


def test_strict_validation_passes_after_build_context_pack(tmp_path):
    _git_repo(tmp_path)
    init_repo(tmp_path)
    build_context_pack(tmp_path, task="validation smoke", profile="quick")

    assert validate_repo(tmp_path, strict=True)["status"] == "green"


def test_strict_validation_passes_after_build_handoff(tmp_path):
    _git_repo(tmp_path)
    init_repo(tmp_path)
    build_context_pack(tmp_path, task="validation smoke", profile="quick")
    build_handoff(tmp_path, task="validation smoke", summary="runtime allowed")

    assert validate_repo(tmp_path, strict=True)["status"] == "green"


def test_known_runtime_files_are_allowed(tmp_path):
    _git_repo(tmp_path)
    runtime = tmp_path / ".ai" / "runtime"
    runtime.mkdir(parents=True)
    (runtime / "last_context.md").write_text("context", encoding="utf-8")
    (runtime / "session_handoff.md").write_text("handoff", encoding="utf-8")

    assert check_runtime_pollution(tmp_path) == []


def test_unknown_runtime_file_is_reported(tmp_path):
    runtime = tmp_path / ".ai" / "runtime"
    runtime.mkdir(parents=True)
    (runtime / "cache.tmp").write_text("cache", encoding="utf-8")

    assert check_runtime_pollution(tmp_path) == [
        "Unexpected runtime file: `.ai/runtime/cache.tmp`."
    ]


def test_tracked_runtime_file_is_reported(tmp_path):
    _git_repo(tmp_path, ignore_runtime=False)
    runtime = tmp_path / ".ai" / "runtime"
    runtime.mkdir(parents=True)
    artifact = runtime / "last_context.md"
    artifact.write_text("context", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", str(artifact)], check=True)

    warnings = check_runtime_pollution(tmp_path)

    assert "`.ai/runtime/` is not ignored by Git." in warnings
    assert "Runtime file is tracked by Git: `.ai/runtime/last_context.md`." in warnings


def test_missing_runtime_directory_is_ok(tmp_path):
    assert check_runtime_pollution(tmp_path) == []


def test_runtime_artifact_in_derived_output_is_reported(tmp_path):
    leaked = tmp_path / ".ai" / "machine" / "last_context.md"
    leaked.parent.mkdir(parents=True)
    leaked.write_text("context", encoding="utf-8")
    (tmp_path / ".ai" / "runtime").mkdir()

    assert "Runtime artifact leaked into derived output: `.ai/machine/last_context.md`." in (
        check_runtime_pollution(tmp_path)
    )
