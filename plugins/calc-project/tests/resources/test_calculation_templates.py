from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[2]
SHARED = PLUGIN / "resources" / "calculation-templates"
MAGNETIC = PLUGIN / "skills" / "magnetic-workflow" / "assets" / "templates"
EXPECTED_SHARED = {
    "common/prepare_and_submit.sh.template",
    "common/prepare_run.sh.template",
    "common/submit_run.sh.template",
    "common/validate_run.sh.template",
    "vasp/cluster-env.sh.template",
    "vasp/run_vasp.pbs.template",
    "vasp/run_vasp_band.pbs.template",
}
EXPECTED_MAGNETIC = {
    "tb2j/cluster-env.sh.template",
    "tb2j/run_tb2j.pbs.template",
    "vampire/cluster-env.sh.template",
    "vampire/run_vampire.pbs.template",
    "wannier/cluster-env.sh.template",
    "wannier/run_vasp_wannier_prerun.pbs.template",
    "wannier/run_wannier90.pbs.template",
}


def inventory(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in root.rglob("*.template")}


def test_calculation_template_inventory_matches_resource_owners() -> None:
    """Catch a template assigned to the wrong owner or lost during packaging."""
    assert inventory(SHARED) == EXPECTED_SHARED
    assert inventory(MAGNETIC) == EXPECTED_MAGNETIC


def test_shared_templates_declare_multiple_workflow_consumers() -> None:
    """Catch shared calculation resources becoming an undifferentiated dump."""
    declaration = (SHARED / "README.md").read_text(encoding="utf-8")
    assert "calc-workflows" in declaration
    assert "vasp-workflow" in declaration
    assert "magnetic-workflow" in declaration
    assert "script-management" in declaration


def test_calc_acceptance_is_recorded() -> None:
    """Catch promoting calculation templates without calc-owner evidence."""
    acceptance = (SHARED / "ACCEPTANCE.md").read_text(encoding="utf-8")
    assert "calc-project source revision" in acceptance
    assert "test_pbs_input_layout.py" in acceptance
    assert "test_magnetic_workflow.py" in acceptance


def test_pbs_templates_keep_preparation_and_handoff_guards() -> None:
    """Catch templates that bypass prepared task inputs or scheduler guards."""
    pbs_templates = tuple(SHARED.glob("**/*.pbs.template")) + tuple(
        MAGNETIC.glob("**/*.pbs.template")
    )
    assert pbs_templates
    for path in pbs_templates:
        text = path.read_text(encoding="utf-8")
        assert 'RUN_TAG="${RUN_TAG:-}"' in text
        assert 'INPUTS_DIR="$TASK_ROOT/inputs"' in text
        assert 'source "$INPUTS_DIR/cluster-env.sh"' in text
        assert "#PBS -o" not in text and "#PBS -e" not in text


def test_magnetic_templates_keep_safe_input_boundaries() -> None:
    """Catch magnetic templates mutating their immutable task input copies."""
    for relative in (
        "tb2j/run_tb2j.pbs.template",
        "vampire/run_vampire.pbs.template",
    ):
        text = (MAGNETIC / relative).read_text(encoding="utf-8")
        assert 'rm -f "$RUN_INPUTS' not in text
        assert 'sed -i "$RUN_INPUTS' not in text
        assert '> "$RUN_INPUTS' not in text
