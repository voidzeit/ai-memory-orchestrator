from pathlib import Path


def test_obsidian_graph_fixture_has_reviewable_vault_structure():
    root = Path("examples/obsidian-graph-vault/Graph")

    assert (root / "index.md").is_file()
    assert list((root / "Nodes").glob("*.md"))
    groups = (root / "Views" / "Groups.md")
    assert groups.is_file()
    assert "amo/node/file" in groups.read_text(encoding="utf-8")

    for note in (root / "Nodes").glob("*.md"):
        text = note.read_text(encoding="utf-8")
        for marker in ("amo_id:", "amo_type:", "source_path:", "tags:", "aliases:", "## Inbound", "## Outbound"):
            assert marker in text
