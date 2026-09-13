def test_spec_template(plugin_root):
    text = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text()
    for field in (
        "ID: SPEC-001",
        "Status: ready",
        "RQ: ../RQ.md",
        "## Judgment",
        "## Tasks",
        "### TASK-001:",
        "Blocked by:",
        "Condition:",
        "Acceptance:",
        "#### Runs",
        "| Run | Status | Current | Path | Result |",
    ):
        assert field in text


def test_design_flow_keeps_full_draft_internal_until_summary_approval(plugin_root):
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    lower = text.casefold()
    assert "$dev-engineering:grill-with-docs" in text
    assert text.index("$dev-engineering:grill-with-docs") < text.index(
        "Draft the Spec"
    )
    assert "keep the complete spec draft internal" in lower
    assert "present only the target path, design summary" in lower
    assert "approval does not require displaying the complete markdown" in lower
    assert "output is one reviewable draft" not in lower
    assert "full markdown draft" not in lower
    assert "complete overwritten spec" not in lower
    assert "each recorded run row has" not in lower


def test_spec_separates_scientific_commitments_from_execution_discretion(plugin_root):
    spec = (plugin_root / "skills/calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    template = (
        plugin_root / "skills/calc-to-spec/references/spec-template.md"
    ).read_text(encoding="utf-8")

    spec_flat = " ".join(spec.split())
    template_flat = " ".join(template.split())
    assert "execution-owned" in spec_flat
    assert "minimum sufficient evidence" in spec_flat
    assert "execution-owned" in template_flat
    assert "favorable scientific outcome" in template_flat
