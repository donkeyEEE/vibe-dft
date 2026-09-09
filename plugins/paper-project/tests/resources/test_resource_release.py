from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile

import pytest


PLUGIN = Path(__file__).resolve().parents[2]
BUILD = PLUGIN / "scripts" / "build_marketplace_release.py"
PREFIX = "paper-project-marketplace/plugins/paper-project/"
PRIVATE_DIRECTORY_NAMES = {"runs", "sources"}
PRIVATE_FILE_NAMES = {
    "build-report.json",
    "dataset.json",
    "final-report.md",
    "review-template.json",
    "reviewed-cases.json",
    "source-packets.json",
}


@pytest.fixture
def release_files(tmp_path: Path) -> set[str]:
    subprocess.run(
        [
            sys.executable,
            str(BUILD),
            "--plugin-root",
            str(PLUGIN),
            "--output-dir",
            str(tmp_path),
            "--skip-plugin-validation",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    archive = next(tmp_path.glob("*.tar.gz"))
    with tarfile.open(archive) as package:
        return set(package.getnames())


def test_release_contains_resources_without_retired_knowledge(
    release_files: set[str],
) -> None:
    """Catch release packaging that omits live resources or ships retired data."""
    assert PREFIX + "resources/paper-writing/README.md" in release_files
    assert (
        PREFIX
        + "skills/prl-polishing/references/paper-writing/write-reader-question-sequence.md"
        in release_files
    )
    assert PREFIX + "skills/cangjie-skill/SKILL.md" not in release_files
    for relative in (
        "skills/zo2notes/scripts/runtime_config.py",
        "skills/zo2notes/scripts/attachment_paths.py",
        "skills/zo2notes/scripts/zotero.py",
        "skills/zo2notes/references/configuration.md",
        "skills/zo2notes/references/troubleshooting.md",
    ):
        assert PREFIX + relative in release_files
    assert (
        PREFIX + "skills/zo2notes/scripts/zotero_wsl_bridge.py" not in release_files
    )
    assert not any(name.startswith(PREFIX + "knowledge/") for name in release_files)
    for retired_skill in ("prl-shared", "paper2ppt", "ppt-master"):
        assert not any(
            name.startswith(PREFIX + f"skills/{retired_skill}/")
            for name in release_files
        )
    assert PREFIX + "scripts/ppt_master_provenance.json" not in release_files
    assert PREFIX + "templates/ppt-master-openai.yaml" not in release_files


def test_pr_intro_runtime_files_ship_without_local_eval_data(
    release_files: set[str],
) -> None:
    required = (
        "SKILL.md",
        "agents/openai.yaml",
        "evals/README.md",
        "evals/schema.json",
        "references/maintenance/optimization-protocol.md",
        "references/maintenance/scoring-rubric.md",
        "references/writing/pr-introduction-logic.md",
        "references/writing/source-boundaries.md",
        "scripts/build_eval_dataset.py",
        "scripts/eval_model.py",
        "scripts/prepare_optimization_run.py",
    )
    skill_prefix = PREFIX + "skills/pr-intro/"

    for relative in required:
        assert skill_prefix + relative in release_files

    release_paths = (PurePosixPath(name) for name in release_files)
    for path in release_paths:
        assert PRIVATE_DIRECTORY_NAMES.isdisjoint(path.parts)
        assert path.name not in PRIVATE_FILE_NAMES
        assert "tests" not in path.parts
