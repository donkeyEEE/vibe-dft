import yaml


EXPECTED = {
    "ask-lyz",
    "calc-setup",
    "calc-rq",
    "calc-to-spec",
    "calc-execute",
    "calc-review",
}


def test_exact_roster(plugin_root):
    assert {
        path.name for path in (plugin_root / "skills").iterdir() if path.is_dir()
    } == EXPECTED
    assert {
        path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")
    } == EXPECTED


def test_model_invoked_metadata(plugin_root):
    for name in sorted(EXPECTED):
        metadata = plugin_root / "skills" / name / "agents" / "openai.yaml"
        data = yaml.safe_load(metadata.read_text(encoding="utf-8"))

        assert "policy" not in data
        assert f"${name}" in data["interface"]["default_prompt"]
        assert data["interface"]["display_name"]
        assert data["interface"]["short_description"]
