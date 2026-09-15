import re


def _field_values(text, field):
    return re.findall(rf"^{re.escape(field)}:\s*(.+)$", text, re.MULTILINE)


def test_rq_template(plugin_root):
    text = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()
    for field in (
        "ID: RQ-001",
        "Status: active",
        "## 问题",
        "Boundary:",
        "## 成功判据",
        "## 规范（Spec）",
        "## 决策",
        "## 上下文",
    ):
        assert field in text

    assert text.index("## 规范（Spec）") < text.index("## 决策")
    assert text.index("## 决策") < text.index("## 上下文")
    assert "## Boundary" not in text
    assert text.index("## 问题") < text.index("Boundary:")
    assert text.index("Boundary:") < text.index("## 成功判据")
    assert "RQ 范围内术语和框架" in text


def test_rq_template_documents_allowed_statuses(plugin_root):
    text = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()

    assert _field_values(text, "Status") == ["active"]
    assert "RQ 状态为 `active | concluded`。" in text


def test_rq_skill_has_only_its_rq_template(plugin_root):
    references = plugin_root / "skills/calc-rq/references"

    assert {path.name for path in references.iterdir()} == {"rq-template.md"}
