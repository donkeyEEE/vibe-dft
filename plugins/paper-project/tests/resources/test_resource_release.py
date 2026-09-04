import json
from pathlib import Path
import shutil
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
    assert prefix + "skill-lifecycle.json" in names
    assert prefix + "resources/paper-writing/README.md" in names
    assert prefix + "skills/prl-polishing/references/paper-writing/write-reader-question-sequence.md" in names
    assert prefix + "skills/cangjie-skill/SKILL.md" in names
    for relative in (
        "skills/zo2notes/scripts/runtime_config.py",
        "skills/zo2notes/scripts/attachment_paths.py",
        "skills/zo2notes/scripts/zotero.py",
        "skills/zo2notes/references/configuration.md",
        "skills/zo2notes/references/troubleshooting.md",
    ):
        assert prefix + relative in names
    assert prefix + "skills/zo2notes/scripts/zotero_wsl_bridge.py" not in names
    assert not any(name.startswith(prefix + "knowledge/") for name in names)
    assert not any(name.startswith(prefix + "skills/prl-shared/") for name in names)


def test_release_skill_roster_comes_from_lifecycle_registry(tmp_path: Path) -> None:
    plugin_copy = tmp_path / "paper-project"
    shutil.copytree(PLUGIN, plugin_copy)
    registry_path = plugin_copy / "skill-lifecycle.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["skills"].pop("zo2notes")
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(BUILD),
            "--plugin-root",
            str(plugin_copy),
            "--output-dir",
            str(tmp_path / "release"),
            "--skip-plugin-validation",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Unexpected skill roster" in result.stderr


def test_release_rejects_development_skills(tmp_path: Path) -> None:
    plugin_copy = tmp_path / "paper-project"
    shutil.copytree(PLUGIN, plugin_copy)
    registry_path = plugin_copy / "skill-lifecycle.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["skills"]["zo2notes"] = "development"
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(BUILD),
            "--plugin-root",
            str(plugin_copy),
            "--output-dir",
            str(tmp_path / "release"),
            "--skip-plugin-validation",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Development skills cannot be released: ['zo2notes']" in result.stderr


def test_release_rejects_unknown_lifecycle_state(tmp_path: Path) -> None:
    plugin_copy = tmp_path / "paper-project"
    shutil.copytree(PLUGIN, plugin_copy)
    registry_path = plugin_copy / "skill-lifecycle.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["skills"]["zo2notes"] = "retired"
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(BUILD),
            "--plugin-root",
            str(plugin_copy),
            "--output-dir",
            str(tmp_path / "release"),
            "--skip-plugin-validation",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Invalid skill lifecycle state" in result.stderr


def test_release_rejects_lifecycle_policy_mismatch(tmp_path: Path) -> None:
    plugin_copy = tmp_path / "paper-project"
    shutil.copytree(PLUGIN, plugin_copy)
    registry_path = plugin_copy / "skill-lifecycle.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["skills"]["cangjie-skill"] = "published"
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(BUILD),
            "--plugin-root",
            str(plugin_copy),
            "--output-dir",
            str(tmp_path / "release"),
            "--skip-plugin-validation",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "Lifecycle state does not match invocation policy" in result.stderr
