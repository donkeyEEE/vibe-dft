from __future__ import annotations


def test_show_cot_keeps_authority_read_only_and_gates_report_generation(plugin_root):
    text = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")

    assert "在对话中展示完整 COT 后" in text
    assert "询问用户是否需要 HTML" in text
    assert "只有本次调用已得到用户确认时才生成报告" in text
    assert "对 RQ、Spec、Task、Run 及其他权威记录保持只读" in text
    assert "不拥有计算事实或进度状态" in text


def test_show_cot_report_contract_is_narrow_and_reproducible(plugin_root):
    text = (plugin_root / "skills/show-cot/SKILL.md").read_text(encoding="utf-8")

    assert "调用 `$show-me`" in text
    assert ".calc-project/progress-report-YYYY-MM-DD.html" in text
    assert "progress-report-*.html" in text
    assert "删除范围只包括" in text
    assert "不依赖 CDN、远程字体或" in text
    assert "返回新报告的可点击路径" in text


def test_calc_setup_ignores_generated_project_reports(plugin_root):
    skill = (plugin_root / "skills/calc-setup/SKILL.md").read_text(encoding="utf-8")
    structure = (
        plugin_root / "skills/calc-setup/references/project-structure.md"
    ).read_text(encoding="utf-8")

    assert "根 `.gitignore` 包含 `/.calc-project/`" in skill
    assert "`.gitignore` 包含 `/.calc-project/`" in structure
    assert "不属于计算项目结构或进度权威" in structure
