from pathlib import Path

import yaml


PLUGIN = Path(__file__).resolve().parents[2]
SKILL = PLUGIN / "skills/literature-review"


def test_literature_review_has_scoped_calc_to_spec_handoff() -> None:
    policy = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert policy["policy"]["allow_implicit_invocation"] is False
    assert "独立使用时仅接受用户显式调用" in body
    assert "`$calc-project:calc-to-spec`" in body
    assert "`06-文献笔记/`" in body
    assert "不覆盖或续写" in body
