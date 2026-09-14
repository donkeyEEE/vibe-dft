import yaml


EXPECTED = {
    "ask-lyz",
    "calc-setup",
    "calc-rq",
    "calc-to-spec",
    "calc-execute",
    "calc-review",
    "show-cot",
}


def test_exact_roster(plugin_root):
    assert {
        path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()
    } == EXPECTED
    assert {
        path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
    } == EXPECTED


def test_model_invoked_metadata(plugin_root):
    for name in sorted(EXPECTED - {"show-cot"}):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert "policy" not in data
        assert f"${name}" in data["interface"]["default_prompt"]
        assert data["interface"]["display_name"]
        assert data["interface"]["short_description"]


def test_show_cot_is_explicit_read_only_entry(plugin_root):
    metadata = plugin_root / "skills" / "show-cot" / "agents" / "openai.yaml"
    data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

    assert data["policy"]["allow_implicit_invocation"] is False
    assert "$show-cot" in data["interface"]["default_prompt"]
