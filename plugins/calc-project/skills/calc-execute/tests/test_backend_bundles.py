def test_execute_does_not_embed_a_backend_inventory(plugin_root):
    """Keep backend discovery out of the main execution workflow."""
    text = (plugin_root / "skills/calc-execute/SKILL.md").read_text(encoding="utf-8")
    assert "Preferred backend bundles" not in text
    assert "| Branch | Exact bundle |" not in text
