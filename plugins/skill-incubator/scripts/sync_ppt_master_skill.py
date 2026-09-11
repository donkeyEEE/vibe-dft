#!/usr/bin/env python3
"""Synchronize a verified upstream PPT Master skill snapshot into Skill Incubator."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXPECTED_REPOSITORY = "https://github.com/hugohe3/ppt-master"
LOCAL_OVERLAY_PATH = "agents/openai.yaml"
LOCAL_OVERLAY_TEMPLATE = "ppt-master-openai.yaml"


def parse_args() -> argparse.Namespace:
    plugin_root = Path(__file__).resolve().parents[1]
    repository_root = plugin_root.parent
    parser = argparse.ArgumentParser(
        description="Vendor the upstream PPT Master skill into Skill Incubator."
    )
    parser.add_argument(
        "--upstream-root",
        type=Path,
        default=repository_root / "reference/ppt-master",
        help="Local upstream checkout containing skills/ppt-master.",
    )
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=plugin_root,
        help="Paper Project plugin root containing .codex-plugin/plugin.json.",
    )
    parser.add_argument(
        "--upstream-url",
        help="Override the upstream origin URL recorded in provenance.",
    )
    parser.add_argument(
        "--source-commit",
        help="Override the upstream Git commit recorded in provenance.",
    )
    return parser.parse_args()


def run_git(upstream_root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(upstream_root), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate_plugin_root(plugin_root: Path) -> None:
    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    if not manifest_path.is_file():
        raise ValueError(f"Plugin manifest is missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != "skill-incubator":
        raise ValueError("Plugin manifest name must be skill-incubator")
    skills_root = (plugin_root / "skills").resolve()
    destination = (skills_root / "ppt-master").resolve()
    if destination.parent != skills_root:
        raise ValueError("PPT Master destination must be inside the plugin skills directory")


def skill_version(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8")
    required = (
        "name: ppt-master",
        'copyright: "Copyright (c) 2025-2026 Hugo He"',
        'license: "MIT"',
        'official_repository: "https://github.com/hugohe3/ppt-master"',
    )
    missing = [entry for entry in required if entry not in text]
    if missing:
        raise ValueError(f"Upstream PPT Master metadata is incomplete: {missing}")
    match = re.search(r'(?m)^  version:\s*["\']([^"\']+)["\']\s*$', text)
    if not match:
        raise ValueError("Upstream PPT Master skill version is missing")
    return match.group(1)


def validate_source(source: Path) -> str:
    required = (
        source / "SKILL.md",
        source / "LICENSE",
        source / "scripts/attribution_guard.py",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise ValueError(f"Upstream PPT Master skill is incomplete: {missing}")
    license_text = (source / "LICENSE").read_text(encoding="utf-8")
    if "MIT License" not in license_text or "Copyright (c) 2025-2026 Hugo He" not in license_text:
        raise ValueError("Upstream PPT Master MIT attribution is incomplete")
    symlinks = [path for path in source.rglob("*") if path.is_symlink()]
    if symlinks:
        raise ValueError(f"Upstream PPT Master skill contains symlinks: {symlinks[:5]}")
    return skill_version(source / "SKILL.md")


def ignore_snapshot_files(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        path = Path(directory) / name
        if name in EXCLUDED_DIRS or path.suffix.lower() in EXCLUDED_SUFFIXES:
            ignored.add(name)
    return ignored


def file_manifest(snapshot: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(snapshot.rglob("*")):
        if path.is_file():
            relative = path.relative_to(snapshot).as_posix()
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def run_attribution_guard(snapshot: Path) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/attribution_guard.py"],
        cwd=snapshot,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"PPT Master attribution guard failed: {detail}")


def synchronize(
    upstream_root: Path,
    plugin_root: Path,
    *,
    upstream_url: str | None = None,
    source_commit: str | None = None,
) -> tuple[Path, Path]:
    upstream_root = upstream_root.resolve()
    plugin_root = plugin_root.resolve()
    validate_plugin_root(plugin_root)
    source = upstream_root / "skills/ppt-master"
    version = validate_source(source)
    repository = upstream_url or run_git(upstream_root, "remote", "get-url", "origin")
    commit = source_commit or run_git(upstream_root, "rev-parse", "HEAD")
    if repository.rstrip("/").removesuffix(".git") != EXPECTED_REPOSITORY.rstrip("/"):
        raise ValueError(f"Unexpected PPT Master upstream repository: {repository}")

    skills_root = plugin_root / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    destination = skills_root / "ppt-master"
    provenance_path = plugin_root / "scripts/ppt_master_provenance.json"
    provenance_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ppt-master-sync-", dir=skills_root) as temp_dir:
        candidate = Path(temp_dir) / "ppt-master"
        shutil.copytree(source, candidate, ignore=ignore_snapshot_files)
        run_attribution_guard(candidate)
        files = file_manifest(candidate)
        overlay_template = plugin_root / "templates" / LOCAL_OVERLAY_TEMPLATE
        if not overlay_template.is_file():
            raise ValueError(f"PPT Master UI overlay is missing: {overlay_template}")
        overlay_destination = candidate / LOCAL_OVERLAY_PATH
        overlay_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(overlay_template, overlay_destination)
        provenance = {
            "schema_version": 1,
            "upstream": {
                "repository": EXPECTED_REPOSITORY,
                "commit": commit,
                "skill_version": version,
            },
            "snapshot_path": "skills/ppt-master",
            "local_overlays": [LOCAL_OVERLAY_PATH],
            "file_count": len(files),
            "files": files,
        }
        provenance_text = json.dumps(
            provenance, ensure_ascii=False, indent=2, sort_keys=True
        ) + "\n"

        backup = Path(temp_dir) / "previous-ppt-master"
        if destination.exists():
            destination.replace(backup)
        try:
            candidate.replace(destination)
            temporary_provenance = provenance_path.with_suffix(".json.tmp")
            temporary_provenance.write_text(provenance_text, encoding="utf-8")
            temporary_provenance.replace(provenance_path)
        except BaseException:
            if destination.exists():
                shutil.rmtree(destination)
            if backup.exists():
                backup.replace(destination)
            raise

    return destination, provenance_path


def main() -> int:
    args = parse_args()
    try:
        destination, provenance = synchronize(
            args.upstream_root,
            args.plugin_root,
            upstream_url=args.upstream_url,
            source_commit=args.source_commit,
        )
    except (OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"PPT Master snapshot: {destination}")
    print(f"Provenance: {provenance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
