from __future__ import annotations

import subprocess
import sys
import tarfile
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
BUILD = PLUGIN / "scripts" / "build_marketplace_release.py"


def test_release_contains_all_incubating_skills(tmp_path: Path) -> None:
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

    prefix = "skill-incubator-marketplace/plugins/skill-incubator/"
    assert prefix + "skills/paper2ppt/SKILL.md" in names
    assert prefix + "skills/ppt-master/SKILL.md" in names
    assert prefix + "skills/cangjie-skill/SKILL.md" in names
    assert prefix + "skills/nature-response/SKILL.md" in names
    assert prefix + "skills/scholar-evaluation/SKILL.md" in names
    assert prefix + "skills/scientific-critical-thinking/SKILL.md" in names
    assert prefix + "skills/prl-polishing/SKILL.md" in names
    assert prefix + "skills/prl-polishing/manifest.yaml" in names
    assert prefix + "skills/prl-polishing/static/core/interaction-protocol.md" in names
    assert prefix + "skills/prl-polishing/scripts/writing_workspace.py" in names
    assert (
        prefix
        + "skills/prl-polishing/references/paper-writing/write-prl-model-to-validation-pairing.md"
        in names
    )
    assert prefix + "skills/ppt-master/LICENSE" in names
    assert prefix + "scripts/ppt_master_provenance.json" in names
    assert prefix + "templates/ppt-master-openai.yaml" in names
    assert not any("/tests/" in name for name in names)


def test_ppt_master_maintenance_assets_belong_to_incubator() -> None:
    required = [
        PLUGIN / "scripts" / "sync_ppt_master_skill.py",
        PLUGIN / "scripts" / "ppt_master_provenance.json",
        PLUGIN / "templates" / "ppt-master-openai.yaml",
    ]
    assert all(path.is_file() for path in required)

    paper = PLUGIN.parent / "paper-project"
    assert not (paper / "scripts" / "sync_ppt_master_skill.py").exists()
    assert not (paper / "scripts" / "ppt_master_provenance.json").exists()
    assert not (paper / "templates" / "ppt-master-openai.yaml").exists()
