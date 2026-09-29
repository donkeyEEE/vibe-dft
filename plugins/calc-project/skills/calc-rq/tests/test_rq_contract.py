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
    ):
        assert field in text

    assert text.index("## 规范（Spec）") < text.index("## 决策")
    assert "## 上下文" not in text
    assert "## Context" not in text
    assert "RQ-CONTEXT.md" in text
    assert "## Boundary" not in text
    assert text.index("## 问题") < text.index("Boundary:")
    assert text.index("Boundary:") < text.index("## 成功判据")
    assert "RQ 范围内术语和框架" in text


def test_context_ownership_and_consumers(plugin_root):
    domain = (plugin_root / "skills/domain-research/SKILL.md").read_text()
    assert "`CONTEXT.md`（项目上下文）" in domain
    assert "`RQ-CONTEXT.md`（RQ 上下文）" in domain
    assert "$dev-engineering:domain-modeling" in domain
    assert "`RQ-CONTEXT.md`（RQ 上下文）由本技能维护" in domain
    assert "首次创建 `RQ-CONTEXT.md` 时" in domain
    assert "[共享领域术语](../../resources/project-context.md)" in domain
    assert "项目与插件已有的定义按需读取，不复制到 RQ 术语清单" in domain
    assert (plugin_root / "resources/project-context.md").is_file()
    for name in ("calc-rq", "calc-to-spec", "calc-execute"):
        skill = (plugin_root / "skills" / name / "SKILL.md").read_text()
        if name != "calc-to-spec":
            assert "RQ-CONTEXT.md" in skill
        else:
            assert "提供项目根、RQ 目录及相关记录" in skill
        assert "$domain-research" in skill
        assert "`RQ.md` 的 `## Context`" not in skill
        assert "术语的收录、确认和更新遵循 `$domain-research`" in skill
        assert "实际文件路径" not in skill
        assert "将内容和来源交给它" not in skill


def test_rq_template_documents_allowed_statuses(plugin_root):
    text = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()

    assert _field_values(text, "Status") == ["active"]
    assert "RQ 状态为 `active | concluded`。" in text


def test_rq_skill_has_only_its_rq_template(plugin_root):
    references = plugin_root / "skills/calc-rq/references"

    assert {path.name for path in references.iterdir()} == {"rq-template.md"}


def test_rq_handoff_leaves_design_mode_to_spec_entry(plugin_root):
    template = (plugin_root / "skills/calc-rq/references/rq-template.md").read_text()
    skill = (plugin_root / "skills/calc-rq/SKILL.md").read_text()

    assert "Spec design mode:" not in template
    assert "设计模式" not in template
    assert "展示准确的拟议文件路径和完整 Markdown 变更" in skill
    assert "不在 `RQ.md` 记录设计模式" in skill
    assert "直接进入 `$calc-to-spec`" in skill


def test_rq_expression_check_precedes_approval(plugin_root):
    skill = " ".join((plugin_root / "skills/calc-rq/SKILL.md").read_text().split())

    assert "检查完整 RQ 草稿或修订后的全文，清理冗余表达并核对原意" in skill
    assert skill.index("开始工作时先加载 `$domain-research`") < skill.index("解析唯一计算项目")
    assert skill.index("展示批准前按 `$domain-research`") < skill.index(
        "展示准确的拟议文件路径和完整 Markdown 变更"
    )
