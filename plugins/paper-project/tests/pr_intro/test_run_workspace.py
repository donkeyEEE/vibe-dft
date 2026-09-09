"""Candidate isolation and transactional source application contracts."""

import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest


SCRIPTS = Path(__file__).resolve().parents[2] / "skills/pr-intro/scripts"
sys.path.insert(0, str(SCRIPTS))


@pytest.fixture
def api():
    assert (SCRIPTS / "prepare_optimization_run.py").is_file(), "workspace implementation absent"
    return importlib.import_module("prepare_optimization_run")


@pytest.fixture
def inputs(tmp_path):
    skill = tmp_path / "formal"
    files = {
        "SKILL.md": "# Intro\nRead [logic](references/writing/logic.md).\nRead `references/maintenance/scoring-rubric.md`.\n",
        "references/writing/logic.md": "# Logic\nOriginal argument.\n",
        "references/maintenance/scoring-rubric.md": "Fixed evaluator.\n",
        "scripts/eval_model.py": "# immutable\n",
    }
    for name, content in files.items():
        path = skill / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    dataset = tmp_path / "dataset"
    dataset.mkdir()
    record = {"seed": 17, "development": [], "acceptance": []}
    for index in range(20):
        split = "development" if index < 15 else "acceptance"
        item = f"item-{index}"
        cases = [{
            "case_id": f"case-{index}-{kind}", "case_type": kind, "split": split,
            "visible_context": "Visible scientific context.",
            "fact_packet": ["Measured a gap."] if kind == "FGCC" else [],
            "reference_continuation": "SECRET reference continuation",
            "item_key": item, "attachment_key": "SECRET attachment", "content_hash": "SECRET hash",
        } for kind in ("SCC", "FGCC")]
        record[split].append({"item_key": item, "cases": cases})
    (dataset / "dataset.json").write_text(json.dumps(record))
    return skill, dataset, tmp_path / "runs"


def prepared(api, inputs):
    return api.prepare_run(*inputs, "run-1")


def test_prepare_copies_only_runtime_files_and_sanitizes_prompts(api, inputs):
    run = prepared(api, inputs)
    assert (run.baseline / "SKILL.md").is_file()
    assert (run.candidate / "references/writing/logic.md").is_file()
    assert not (run.candidate / "references/maintenance").exists()
    assert not (run.candidate / "scripts").exists()
    assert (run.root / "iterations.jsonl").read_text() == ""
    manifest = json.loads((run.root / "workspace.json").read_text())
    assert set(manifest["source_hashes"]) == {"SKILL.md", "references/writing/logic.md"}
    assert len(manifest["dataset_hash"]) == 64
    prompts = list((run.root / "prompts/development").glob("*.json"))
    assert len(prompts) == 30
    assert not (run.root / "prompts/acceptance").exists()
    for prompt in prompts:
        payload = json.loads(prompt.read_text())
        assert set(payload) <= {"case_id", "case_type", "visible_context", "fact_packet"}
        assert "SECRET" not in prompt.read_text()
    assert not (run.baseline / "SKILL.md").stat().st_mode & 0o222


@pytest.mark.parametrize(
    "field,value",
    [
        ("fact_packet", ["Zotero item item-0 supplies this fact."]),
    ],
)
def test_prepare_refuses_to_emit_prompts_with_internal_retrieval_handles(api, inputs, field, value):
    skill, dataset, runs = inputs
    record = json.loads((dataset / "dataset.json").read_text())
    record["development"][0]["cases"][1][field] = value
    (dataset / "dataset.json").write_text(json.dumps(record))

    with pytest.raises(ValueError, match="retrieval handle"):
        api.prepare_run(skill, dataset, runs, "unsafe-run")

    assert not (runs / "unsafe-run").exists()


@pytest.mark.parametrize(
    "value",
    [
        "See doi:10.1103/PhysRevLett.130.123456",
        "Source: /private/dataset/sources/public-paper.json",
        "Preprint arXiv:2609.01234v2",
        "Mirror https://example.org/paper",
        r"Local copy \\server\share\paper.pdf",
        "Local copy ~/papers/source.pdf",
    ],
)
def test_prepare_redacts_public_handles_before_emitting_prompt(api, inputs, value):
    skill, dataset, runs = inputs
    record = json.loads((dataset / "dataset.json").read_text())
    record["development"][0]["cases"][1]["visible_context"] = value
    (dataset / "dataset.json").write_text(json.dumps(record))

    run = api.prepare_run(skill, dataset, runs, "redacted-run")
    prompt_text = "\n".join(
        path.read_text() for path in (run.root / "prompts/development").glob("*.json")
    )

    assert value not in prompt_text
    assert "[SOURCE_IDENTIFIER_REDACTED]" in prompt_text


def test_patch_and_apply_preserve_baseline_and_immutable_files(api, inputs):
    run = prepared(api, inputs)
    logic = "references/writing/logic.md"
    (run.candidate / logic).write_text("# Logic\nImproved argument.\n")
    patch = api.candidate_patch(run)
    assert "--- a/references/writing/logic.md" in patch
    assert "+++ b/references/writing/logic.md" in patch
    assert "-Original argument." in patch and "+Improved argument." in patch
    changed = api.apply_candidate(run)
    assert list(changed) == [run.formal_skill / logic]
    assert (run.formal_skill / logic).read_text().endswith("Improved argument.\n")
    assert (run.baseline / logic).read_text().endswith("Original argument.\n")
    assert (run.formal_skill / "references/maintenance/scoring-rubric.md").read_text() == "Fixed evaluator.\n"
    assert (run.root / "candidate.patch").read_text() == patch


@pytest.mark.parametrize("drift", ["modify", "add", "delete"])
def test_source_drift_blocks_all_writes(api, inputs, drift):
    run = prepared(api, inputs)
    (run.candidate / "SKILL.md").write_text("Candidate change.\n")
    target = run.formal_skill / "references/writing/logic.md"
    if drift == "modify":
        target.write_text("External change.\n")
    elif drift == "delete":
        target.unlink()
    else:
        (target.parent / "external.md").write_text("External file.\n")
    before = (run.formal_skill / "SKILL.md").read_bytes()
    with pytest.raises(api.SourceDriftError):
        api.apply_candidate(run)
    assert (run.formal_skill / "SKILL.md").read_bytes() == before


@pytest.mark.parametrize("path", ["scripts/eval_model.py", "references/maintenance/rule.md", "references/writing/nested/rule.md", "evals/cases.json"])
def test_candidate_cannot_extend_mutable_allowlist(api, inputs, path):
    run = prepared(api, inputs)
    target = run.candidate / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("unauthorized")
    with pytest.raises(api.WorkspaceError):
        api.apply_candidate(run)


@pytest.mark.parametrize("link", ["[missing](references/writing/missing.md)", "`references/writing/missing.md`", "[escape](../secret.md)"])
def test_broken_and_escaping_links_block_apply(api, inputs, link):
    run = prepared(api, inputs)
    original = (run.formal_skill / "SKILL.md").read_text()
    (run.candidate / "SKILL.md").write_text(link + "\n")
    with pytest.raises(api.WorkspaceError):
        api.apply_candidate(run)
    assert (run.formal_skill / "SKILL.md").read_text() == original


def test_writing_additions_and_deletions_are_transactional(api, inputs):
    run = prepared(api, inputs)
    (run.candidate / "references/writing/logic.md").unlink()
    (run.candidate / "references/writing/new.md").write_text("New logic.\n")
    (run.candidate / "SKILL.md").write_text("Read [new](references/writing/new.md).\n")
    patch = api.candidate_patch(run)
    assert "--- /dev/null" in patch and "+++ /dev/null" in patch
    api.apply_candidate(run)
    assert not (run.formal_skill / "references/writing/logic.md").exists()
    assert (run.formal_skill / "references/writing/new.md").read_text() == "New logic.\n"


def test_replace_failure_restores_formal_tree(api, inputs, monkeypatch):
    run = prepared(api, inputs)
    before = {p.relative_to(run.formal_skill): p.read_bytes() for p in run.formal_skill.rglob("*") if p.is_file()}
    (run.candidate / "SKILL.md").write_text("New router.\n")
    (run.candidate / "references/writing/logic.md").write_text("New logic.\n")
    real_replace = api.os.replace
    failed = False

    def fail_second(source, destination):
        nonlocal failed
        if Path(destination) == run.formal_skill / "references/writing/logic.md" and not failed:
            failed = True
            raise OSError("simulated replacement failure")
        return real_replace(source, destination)

    monkeypatch.setattr(api.os, "replace", fail_second)
    with pytest.raises(OSError, match="simulated"):
        api.apply_candidate(run)
    assert {p.relative_to(run.formal_skill): p.read_bytes() for p in run.formal_skill.rglob("*") if p.is_file()} == before


def test_baseline_tampering_blocks_application(api, inputs):
    run = prepared(api, inputs)
    baseline = run.baseline / "SKILL.md"
    baseline.chmod(0o644)
    baseline.write_text("Tampered baseline.\n")
    with pytest.raises(api.WorkspaceError):
        api.apply_candidate(run)


def test_symlink_candidate_rejected(api, inputs):
    run = prepared(api, inputs)
    path = run.candidate / "references/writing/logic.md"
    path.unlink()
    path.symlink_to(run.formal_skill / "references/writing/logic.md")
    with pytest.raises(api.WorkspaceError):
        api.apply_candidate(run)


def test_preparation_rejects_overlaps_and_existing_runs(api, inputs):
    skill, dataset, runs = inputs
    with pytest.raises(api.WorkspaceError):
        api.prepare_run(skill, dataset, skill / "runs", "run-1")
    with pytest.raises(api.WorkspaceError):
        api.prepare_run(skill, dataset, runs, "../escape")
    run = prepared(api, inputs)
    with pytest.raises(api.WorkspaceError):
        prepared(api, inputs)
    assert (run.candidate / "SKILL.md").is_file()


def test_cli_prepares_and_prints_reviewable_patch(api, inputs):
    skill, dataset, runs = inputs
    script = SCRIPTS / "prepare_optimization_run.py"
    result = subprocess.run([sys.executable, str(script), "prepare", "--skill-root", str(skill), "--dataset-root", str(dataset), "--runs-root", str(runs), "--run-id", "cli-run"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    (runs / "cli-run/candidate/references/writing/logic.md").write_text("Changed.\n")
    patch = subprocess.run([sys.executable, str(script), "patch", str(runs / "cli-run")], capture_output=True, text=True)
    assert patch.returncode == 0, patch.stderr
    assert "+Changed." in patch.stdout


def test_empty_added_file_is_represented_in_patch(api, inputs):
    run = prepared(api, inputs)
    (run.candidate / "references/writing/empty.md").touch()
    patch = api.candidate_patch(run)
    assert "diff --git a/references/writing/empty.md b/references/writing/empty.md" in patch
    assert "new file mode 100644" in patch
    check = subprocess.run(["git", "apply", "--check"], input=patch, cwd=run.formal_skill, capture_output=True, text=True)
    assert check.returncode == 0, check.stderr


def test_dataset_drift_blocks_application(api, inputs):
    run = prepared(api, inputs)
    (run.candidate / "SKILL.md").write_text("New router.\n")
    (run.dataset_root / "dataset.json").write_text("{}")
    with pytest.raises(api.WorkspaceError, match="dataset"):
        api.apply_candidate(run)
    assert (run.formal_skill / "SKILL.md").read_text().startswith("# Intro")


def test_deleted_skill_and_broken_reference_definition_are_rejected(api, inputs):
    run = prepared(api, inputs)
    (run.candidate / "SKILL.md").unlink()
    with pytest.raises(api.WorkspaceError):
        api.candidate_patch(run)
    (run.candidate / "SKILL.md").write_text("Read [guide].\n\n[guide]: references/writing/absent.md\n")
    with pytest.raises(api.WorkspaceError, match="broken relative link"):
        api.apply_candidate(run)


def test_run_cannot_store_private_prompts_inside_any_repository(api, inputs, tmp_path):
    repository = tmp_path / "other-repository"
    repository.mkdir()
    (repository / ".git").mkdir()
    with pytest.raises(api.WorkspaceError, match="outside a Git repository"):
        api.prepare_run(inputs[0], inputs[1], repository / "runs", "run-1")
    assert not (repository / "runs").exists()


def test_patch_preserves_no_trailing_newline_and_source_permissions(api, inputs):
    inputs[0].joinpath("SKILL.md").chmod(0o640)
    run = prepared(api, inputs)
    (run.candidate / "SKILL.md").write_text("New router without newline")
    patch = api.candidate_patch(run)
    assert "+New router without newline\n\\ No newline at end of file\n" in patch
    api.apply_candidate(run)
    assert (run.formal_skill / "SKILL.md").stat().st_mode & 0o777 == 0o640


def test_rollback_failure_preserves_backups_for_recovery(api, inputs, monkeypatch):
    run = prepared(api, inputs)
    original = (run.formal_skill / "SKILL.md").read_bytes()
    (run.candidate / "SKILL.md").write_text("New router.\n")
    (run.candidate / "references/writing/logic.md").write_text("New logic.\n")
    real_replace = api.os.replace

    def fail_write_and_rollback(source, destination):
        if Path(destination) == run.formal_skill / "references/writing/logic.md" or "backup" in Path(source).parts:
            raise OSError("disk failure")
        return real_replace(source, destination)

    monkeypatch.setattr(api.os, "replace", fail_write_and_rollback)
    with pytest.raises(api.WorkspaceError, match="recovery"):
        api.apply_candidate(run)
    backups = list(run.formal_skill.parent.glob(".formal.apply-*/backup/SKILL.md"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == original
