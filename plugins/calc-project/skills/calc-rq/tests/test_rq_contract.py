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


def test_decision_ticket_template_has_open_and_resolution_shapes(plugin_root):
    text = (
        plugin_root / "skills/calc-rq/references/decision-ticket-template.md"
    ).read_text()

    for field in (
        "ID: DT-001",
        "Status: open",
        "Blocked by:",
        "## Question",
        "Status: resolved",
        "## Answer",
    ):
        assert field in text
    assert "Ticket status is `open | resolved`." in text


def test_decision_ticket_dependencies_are_same_parent_ids(plugin_root):
    text = (
        plugin_root / "skills/calc-rq/references/decision-ticket-template.md"
    ).read_text()

    assert "Blocked by: DT-001, DT-002" in text
    assert "same RQ" in text
