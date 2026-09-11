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


def test_publication_gate_requires_complete_approved_documents(plugin_root):
    text = " ".join(
        (plugin_root / "skills/calc-to-spec/SKILL.md")
        .read_text(encoding="utf-8")
        .split()
    )

    lower = text.casefold()
    assert "complete proposed spec" in lower
    assert "current rq" in lower
    assert "before any write" in lower
    assert "approval of malformed content" in lower
    assert "does not authorize filling or changing" in text
    for field in (
        "`Question`, `Boundary`, `Success Criterion`, `Decisions`, and `Specs`",
        "`ID`, `Status`, `RQ`, `Judgment`, and `Tasks`",
        "`Status`, `Path`, `Blocked by`, `Condition`, `Purpose`, `Acceptance`, and `Runs`",
        "Run ID, `Status`, `Current`, `Path`, and `Result`",
    ):
        assert field in text
