#!/usr/bin/env python3
"""Build a validated, self-contained Paper Project marketplace release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile


MARKETPLACE_NAME = "paper-project-release"
BUNDLE_DIRNAME = "paper-project-marketplace"
EXCLUDED_DIRS = {
    ".git",
    ".ingest-staging",
    ".pytest_cache",
    "__pycache__",
    "tests",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
SKILL_STATES = {"development", "published", "explicit-only"}
def parse_args() -> argparse.Namespace:
    script_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build a complete local-marketplace archive for Paper Project."
    )
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=script_root,
        help="Plugin root containing .codex-plugin/plugin.json.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_root.parent / "dist",
        help="Directory for the archive and its SHA-256 sidecar.",
    )
    parser.add_argument(
        "--validator",
        type=Path,
        default=Path.home()
        / ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py",
        help="Path to plugin-creator's validate_plugin.py.",
    )
    parser.add_argument(
        "--skip-plugin-validation",
        action="store_true",
        help="Skip external plugin validation; intended only for isolated tests.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an archive for the exact same version if it already exists.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_plugin_manifest(plugin_root: Path) -> dict[str, object]:
    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing plugin manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != "paper-project":
        raise SystemExit("plugin.json name must be paper-project")
    version = manifest.get("version")
    if not isinstance(version, str) or "+codex." not in version:
        raise SystemExit("plugin version must include a +codex.<cachebuster> suffix")
    return manifest


def validate_source(plugin_root: Path, validator: Path, skip: bool) -> None:
    if skip:
        return
    if not validator.is_file():
        raise SystemExit(
            f"Plugin validator not found: {validator}. "
            "Pass --validator or use --skip-plugin-validation explicitly."
        )
    subprocess.run(
        [sys.executable, str(validator), str(plugin_root)],
        check=True,
    )


def ignore_release_files(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        path = Path(directory) / name
        if name in EXCLUDED_DIRS or path.suffix.lower() in EXCLUDED_SUFFIXES:
            ignored.add(name)
    return ignored


def marketplace_document() -> dict[str, object]:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": "Paper Project Release"},
        "plugins": [
            {
                "name": "paper-project",
                "source": {
                    "source": "local",
                    "path": "./plugins/paper-project",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
        ],
    }


def write_bundle_readme(bundle_root: Path, version: str) -> None:
    content = f"""# Paper Project Marketplace Release

Version: `{version}`

Keep this directory at a stable absolute path. For first installation:

```bash
codex plugin marketplace add /absolute/path/to/{BUNDLE_DIRNAME}
codex plugin add paper-project@{MARKETPLACE_NAME}
codex plugin list
```

For an archive-based update, replace the contents at the same stable path and
run `codex plugin add paper-project@{MARKETPLACE_NAME}` again. Do not use
`codex plugin marketplace upgrade` for this local directory; that command
refreshes Git marketplace snapshots. Start a new Codex conversation after an
install, update, or rollback.

See `plugins/paper-project/README.md` for dependencies, update safety, and
rollback instructions. Verify bundled files with `MANIFEST.sha256`.
"""
    (bundle_root / "README.md").write_text(content, encoding="utf-8")


def write_content_manifest(bundle_root: Path) -> None:
    entries: list[str] = []
    for path in sorted(bundle_root.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.sha256":
            relative = path.relative_to(bundle_root).as_posix()
            entries.append(f"{sha256_file(path)}  {relative}")
    (bundle_root / "MANIFEST.sha256").write_text(
        "\n".join(entries) + "\n", encoding="utf-8"
    )


def load_skill_lifecycle(plugin_root: Path) -> dict[str, str]:
    path = plugin_root / "skill-lifecycle.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        raise SystemExit(f"Invalid skill lifecycle registry: {path}")
    skills = data["skills"]
    if not set(skills.values()) <= SKILL_STATES:
        raise SystemExit(f"Invalid skill lifecycle state: {path}")
    return skills


def assert_skill_contract(plugin_root: Path) -> None:
    skills_root = plugin_root / "skills"
    lifecycle = load_skill_lifecycle(plugin_root)
    development_skills = sorted(
        skill_name for skill_name, state in lifecycle.items() if state == "development"
    )
    if development_skills:
        raise SystemExit(
            f"Development skills cannot be released: {development_skills}"
        )
    policy_mismatches: list[str] = []
    for skill_name, state in lifecycle.items():
        interface = skills_root / skill_name / "agents/openai.yaml"
        is_explicit_only = (
            interface.is_file()
            and re.search(
                r"(?m)^\s*allow_implicit_invocation:\s*false\s*$",
                interface.read_text(encoding="utf-8"),
            )
            is not None
        )
        if is_explicit_only != (state == "explicit-only"):
            policy_mismatches.append(skill_name)
    if policy_mismatches:
        raise SystemExit(
            "Lifecycle state does not match invocation policy: "
            f"{sorted(policy_mismatches)}"
        )
    expected_skills = set(lifecycle)
    actual_skills = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if actual_skills != expected_skills:
        missing = sorted(expected_skills - actual_skills)
        unexpected = sorted(actual_skills - expected_skills)
        raise SystemExit(
            f"Unexpected skill roster; missing={missing}, unexpected={unexpected}"
        )

    actual_user_interfaces = {
        skill_name
        for skill_name in actual_skills
        if (skills_root / skill_name / "agents/openai.yaml").is_file()
    }
    if actual_user_interfaces != actual_skills:
        missing = sorted(actual_skills - actual_user_interfaces)
        unexpected = sorted(actual_user_interfaces - actual_skills)
        raise SystemExit(
            f"Unexpected user-interface roster; missing={missing}, unexpected={unexpected}"
        )


def assert_bundle_contract(bundle_root: Path, version: str) -> None:
    marketplace_path = bundle_root / ".agents/plugins/marketplace.json"
    bundled_plugin = bundle_root / "plugins/paper-project"
    required = [
        marketplace_path,
        bundled_plugin / ".codex-plugin/plugin.json",
        bundled_plugin / "skill-lifecycle.json",
        bundled_plugin / "README.md",
        bundled_plugin / "skills/prl-polishing/SKILL.md",
        bundled_plugin / "skills/paper2ppt/SKILL.md",
        bundled_plugin / "skills/ppt-master/SKILL.md",
        bundled_plugin / "skills/ppt-master/LICENSE",
        bundled_plugin / "skills/ppt-master/scripts/attribution_guard.py",
        bundled_plugin / "skills/cangjie-skill/references/legacy/README.md",
        bundled_plugin / "resources/paper-writing/README.md",
        bundled_plugin / "scripts/ppt_master_provenance.json",
        bundled_plugin / "templates/ppt-master-openai.yaml",
        bundle_root / "README.md",
        bundle_root / "MANIFEST.sha256",
    ]
    expected_skills = set(load_skill_lifecycle(bundled_plugin))
    required.extend(
        bundled_plugin / "skills" / skill_name / "SKILL.md"
        for skill_name in sorted(expected_skills)
    )
    required.extend(
        bundled_plugin / "skills" / skill_name / "agents/openai.yaml"
        for skill_name in sorted(expected_skills)
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Release bundle is missing required files: {missing}")

    assert_skill_contract(bundled_plugin)

    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    entry = marketplace["plugins"][0]
    if marketplace["name"] != MARKETPLACE_NAME:
        raise SystemExit("Unexpected marketplace name")
    if entry["source"]["path"] != "./plugins/paper-project":
        raise SystemExit("Marketplace source path is not portable")

    bundled_manifest = json.loads(
        (bundled_plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    if bundled_manifest.get("version") != version:
        raise SystemExit("Bundled plugin version differs from source version")

    forbidden: list[str] = []
    for path in bundle_root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            forbidden.append(str(path.relative_to(bundle_root)))
        elif path.suffix.lower() in EXCLUDED_SUFFIXES:
            forbidden.append(str(path.relative_to(bundle_root)))
    if forbidden:
        raise SystemExit(f"Release bundle contains excluded files: {forbidden[:10]}")


def build_release(args: argparse.Namespace) -> tuple[Path, Path]:
    plugin_root = args.plugin_root.resolve()
    output_dir = args.output_dir.resolve()
    manifest = load_plugin_manifest(plugin_root)
    version = str(manifest["version"])
    validate_source(
        plugin_root,
        args.validator.expanduser().resolve(),
        args.skip_plugin_validation,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"paper-project-marketplace-{version}.tar.gz"
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    existing = [path for path in (archive, checksum) if path.exists()]
    if existing and not args.force:
        raise SystemExit(
            "Refusing to overwrite existing release files: "
            + ", ".join(str(path) for path in existing)
        )
    for path in existing:
        path.unlink()

    with tempfile.TemporaryDirectory(prefix="paper-project-release-") as temp_dir:
        bundle_root = Path(temp_dir) / BUNDLE_DIRNAME
        bundled_plugin = bundle_root / "plugins/paper-project"
        bundled_plugin.parent.mkdir(parents=True)
        shutil.copytree(
            plugin_root,
            bundled_plugin,
            ignore=ignore_release_files,
        )

        marketplace_path = bundle_root / ".agents/plugins/marketplace.json"
        marketplace_path.parent.mkdir(parents=True)
        marketplace_path.write_text(
            json.dumps(marketplace_document(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        write_bundle_readme(bundle_root, version)
        write_content_manifest(bundle_root)
        assert_bundle_contract(bundle_root, version)
        validate_source(
            bundled_plugin,
            args.validator.expanduser().resolve(),
            args.skip_plugin_validation,
        )

        with tarfile.open(archive, "w:gz") as tar:
            tar.add(bundle_root, arcname=BUNDLE_DIRNAME)

    archive_digest = sha256_file(archive)
    checksum.write_text(f"{archive_digest}  {archive.name}\n", encoding="utf-8")
    return archive, checksum


def main() -> int:
    archive, checksum = build_release(parse_args())
    print(f"Release archive: {archive}")
    print(f"SHA-256 file: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
