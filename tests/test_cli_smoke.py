import pytest
from typer.testing import CliRunner

from amo.cli import app


runner = CliRunner()


def test_top_level_cli_commands_are_registered():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    for command in (
        "benchmark",
        "context",
        "embeddings",
        "evolve",
        "export",
        "graph",
        "handoff",
        "mcp",
        "optimize",
        "postflight",
        "preflight",
        "server",
        "validate",
    ):
        assert command in result.stdout


def test_nested_cli_commands_are_registered():
    expectations = {
        ("graph", "--help"): ("build", "export"),
        ("embeddings", "--help"): ("build", "search"),
        ("mcp", "--help"): ("serve",),
        ("optimize", "--help"): ("check", "params", "plan", "suggest"),
        ("optimize", "params", "--help"): ("apply-safe", "best", "suggest", "sweep"),
    }

    for arguments, commands in expectations.items():
        result = runner.invoke(app, list(arguments))
        assert result.exit_code == 0
        for command in commands:
            assert command in result.stdout


@pytest.mark.parametrize(
    ("target", "output"),
    (
        ("agents", "AGENTS.md"),
        ("codex", "AGENTS.md"),
        ("claude", "CLAUDE.md"),
        ("cursor", ".cursor/rules/amo.mdc"),
        ("cline", "memory-bank/activeContext.md"),
        ("opencode", "OPENCODE.md"),
    ),
)
def test_each_cli_adapter_target_exports(tmp_path, target, output):
    result = runner.invoke(app, ["export", "--target", target, "--repo", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / output).is_file()
