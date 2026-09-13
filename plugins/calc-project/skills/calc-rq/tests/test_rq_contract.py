import re


def _field_values(text, field):
    return re.findall(rf"^{re.escape(field)}:\s*(.+)$", text, re.MULTILINE)


def test_rq_template(plugin_root):
    text = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()
    for field in (
        "ID: RQ-001",
        "Status: active",
        "## Question",
        "## Boundary",
        "## Success Criterion",
        "## Decisions",
        "## Specs",
    ):
        assert field in text


def test_rq_template_documents_allowed_statuses(plugin_root):
    text = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()

    assert _field_values(text, "Status") == ["active"]
    assert "RQ status is `active | concluded`." in text


def test_rq_skill_has_only_its_rq_template(plugin_root):
    references = plugin_root / "skills/calc-rq/references"

    assert {path.name for path in references.iterdir()} == {"rq-template.md"}
