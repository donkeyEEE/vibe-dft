from pathlib import Path
import subprocess
import sys
import tarfile


PLUGIN = Path(__file__).resolve().parents[2]
BUILD = PLUGIN / "scripts" / "build_marketplace_release.py"


def test_release_contains_resources_without_retired_knowledge(tmp_path: Path) -> None:
    """Catch release packaging that omits live resources or ships retired data."""
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
        names = set(package.getnames())
    prefix = "paper-project-marketplace/plugins/paper-project/"
    assert prefix + "resources/paper-writing/README.md" in names
    assert prefix + "skills/prl-polishing/references/paper-writing/write-reader-question-sequence.md" in names
    assert prefix + "skills/cangjie-skill/SKILL.md" in names
    assert not any(name.startswith(prefix + "knowledge/") for name in names)
    assert not any(name.startswith(prefix + "skills/prl-shared/") for name in names)
