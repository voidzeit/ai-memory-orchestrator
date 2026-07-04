from amo.adapters.agents import export_agents_md
from amo.adapters.claude import export_claude_md
from amo.adapters.cline import export_cline_memory_bank
from amo.adapters.cursor import export_cursor_rules
from amo.adapters.opencode import export_opencode_instructions


def test_agent_exporters_write_expected_files(tmp_path):
    assert export_agents_md(tmp_path).name == "AGENTS.md"
    assert export_claude_md(tmp_path).name == "CLAUDE.md"
    assert export_cursor_rules(tmp_path).as_posix().endswith(".cursor/rules/amo.mdc")
    assert export_cline_memory_bank(tmp_path).as_posix().endswith("memory-bank/activeContext.md")
    assert export_opencode_instructions(tmp_path).name == "OPENCODE.md"


def test_adapters_include_lifecycle_and_runtime_policy(tmp_path):
    paths = [export_agents_md(tmp_path), export_claude_md(tmp_path), export_cursor_rules(tmp_path), export_cline_memory_bank(tmp_path), export_opencode_instructions(tmp_path)]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "amo preflight" in text
        assert "amo handoff" in text
        assert "amo postflight" in text
        assert "amo validate --strict" in text
        assert ".ai/runtime/" in text
