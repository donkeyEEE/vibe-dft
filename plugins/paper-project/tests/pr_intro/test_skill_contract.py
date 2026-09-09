from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOT = ROOT / "plugins/paper-project/skills/pr-intro"
SKILL = SKILL_ROOT / "SKILL.md"
INTRO_LOGIC = "references/writing/pr-introduction-logic.md"
SOURCE_BOUNDARIES = "references/writing/source-boundaries.md"


def test_router_keeps_maintenance_explicit():
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    assert "explicit request to optimize `pr-intro`" in text
    assert "explicitly asks to optimize `pr-intro`" in frontmatter
    assert "references/maintenance/optimization-protocol.md" in text
    assert "Do not load maintenance" in text


def test_router_names_existing_writing_references():
    text = SKILL.read_text(encoding="utf-8")

    for relative_path in (INTRO_LOGIC, SOURCE_BOUNDARIES):
        assert relative_path in text
        assert (SKILL_ROOT / relative_path).is_file()


def test_ordinary_route_excludes_evaluation_and_maintenance_content():
    text = SKILL.read_text(encoding="utf-8")
    ordinary_route = text.split("For ordinary writing", 1)[1]

    assert text.count("references/maintenance/") == 1
    for forbidden in ("evaluation", "evals/", "dataset", "SCC", "FGCC"):
        assert forbidden not in text
    for forbidden in ("maintenance", "optimization", "references/maintenance/"):
        assert forbidden not in ordinary_route


def test_runtime_contract_names_grounding_and_argument_map():
    text = SKILL.read_text(encoding="utf-8")
    assert "available-facts" in text
    assert "argument map" in text
    assert "do not invent" in text.lower()


def test_writing_references_encode_six_moves_and_source_boundaries():
    logic = (SKILL_ROOT / INTRO_LOGIC).read_text(encoding="utf-8")
    boundaries = (SKILL_ROOT / SOURCE_BOUNDARIES).read_text(encoding="utf-8")
    normalized_boundaries = " ".join(boundaries.split())
    moves = (
        "Establish the research territory",
        "Synthesize relevant progress",
        "Narrow to a specific unresolved problem",
        "why that gap is a scientific obstacle",
        "Introduce the study's research path",
        "contribution and significance from confirmed material only",
    )

    for move in moves:
        assert move in logic
    for boundary in (
        "primary source",
        "explicitly permitted",
        "traceable source",
        "require direct support",
        "Do not infer",
    ):
        assert boundary in normalized_boundaries


def test_openai_interface_allows_implicit_invocation():
    interface = (SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    assert "allow_implicit_invocation: true" in interface


def test_repository_navigation_lists_pr_intro():
    description = "Draft or restructure evidence-grounded Physical Review Introductions."
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    plugin_readme = (ROOT / "plugins/paper-project/README.md").read_text(
        encoding="utf-8"
    )

    assert "[pr-intro](plugins/paper-project/skills/pr-intro/SKILL.md)" in root_readme
    assert description in root_readme
    assert "[pr-intro](skills/pr-intro/SKILL.md)" in plugin_readme
    assert description in plugin_readme


def test_dataset_materialization_and_optimization_require_fresh_separate_contexts():
    evals = (SKILL_ROOT / "evals/README.md").read_text(encoding="utf-8").lower()
    protocol = (
        SKILL_ROOT / "references/maintenance/optimization-protocol.md"
    ).read_text(encoding="utf-8").lower()

    for text in (evals, protocol):
        assert "separate fresh optimizer context" in text
        assert "must not inherit" in text

    assert "remaining hidden suffix" not in evals
    assert "contiguous next complete argument move" in evals


def test_optimization_protocol_pins_every_agent_role_to_sol_low():
    protocol = (
        SKILL_ROOT / "references/maintenance/optimization-protocol.md"
    ).read_text(encoding="utf-8")

    assert "gpt-5.6-sol" in protocol
    assert "reasoning_effort=\"low\"" in protocol
    for role in (
        "optimizing primary agent",
        "generator",
        "scorer",
        "acceptance coordinator",
        "code reviewer",
    ):
        assert role in protocol
    assert "Only an explicit user instruction may override" in protocol


def test_baseline_annotation_contract_enforces_single_scorer_calibration():
    rubric = " ".join(
        (SKILL_ROOT / "references/maintenance/scoring-rubric.md")
        .read_text(encoding="utf-8")
        .lower()
        .split()
    )
    protocol = " ".join(
        (SKILL_ROOT / "references/maintenance/optimization-protocol.md")
        .read_text(encoding="utf-8")
        .lower()
        .split()
    )

    for requirement in (
        "score 5 is rare",
        "mandatory deduction",
        "score each dimension independently",
        "concrete evidence",
    ):
        assert requirement in rubric

    for requirement in (
        "one fixed scorer",
        "complete baseline annotation pass",
        "one final score set",
        "aggregate <= 80",
        "calibration failure",
        "rescore the fixed outputs",
    ):
        assert requirement in protocol

    for forbidden in ("transform the scores", "directly decrement"):
        assert forbidden in protocol


def test_evaluation_docs_define_public_handle_redaction_boundary():
    evals = (SKILL_ROOT / "evals/README.md").read_text(encoding="utf-8")
    protocol = (
        SKILL_ROOT / "references/maintenance/optimization-protocol.md"
    ).read_text(encoding="utf-8")

    for text in (evals, protocol):
        assert "[SOURCE_IDENTIFIER_REDACTED]" in text
        assert "item key" in text
        assert "attachment key" in text
