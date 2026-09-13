#!/usr/bin/env python3
"""Build and safely unpack the Calc Project runtime acceptance archive."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import tarfile
from pathlib import Path, PurePosixPath

import yaml


SKILL_NAMES = (
    "ask-lyz",
    "calc-setup",
    "calc-rq",
    "calc-to-spec",
    "calc-execute",
    "calc-review",
)

REQUIRED_DT005_ASSETS = (
    "skills/calc-setup/scripts/verify_cluster_profile.sh",
    "skills/calc-execute/assets/templates/common/run.sh.template",
    "skills/calc-execute/assets/templates/vasp/cluster-env.sh.template",
    "skills/calc-execute/assets/templates/vasp/scf/run.pbs.template",
    "skills/calc-execute/assets/templates/vasp/band/run.pbs.template",
    "skills/calc-execute/assets/templates/vasp/wannier-prerun/cluster-env.sh.template",
    "skills/calc-execute/assets/templates/vasp/wannier-prerun/run.pbs.template",
    "skills/calc-execute/assets/templates/wannier90/cluster-env.sh.template",
    "skills/calc-execute/assets/templates/wannier90/run.pbs.template",
    "skills/calc-execute/assets/templates/wannier90/wannier-run.env.template",
    "skills/calc-execute/assets/templates/tb2j/cluster-env.sh.template",
    "skills/calc-execute/assets/templates/tb2j/run.pbs.template",
    "skills/calc-execute/assets/templates/vampire/cluster-env.sh.template",
    "skills/calc-execute/assets/templates/vampire/run.pbs.template",
    "skills/calc-execute/scripts/fingerprint_run.py",
    "skills/calc-execute/scripts/calculation-monitor.py",
    "skills/calc-execute/references/remote-completion.md",
    "skills/calc-execute/scripts/probe-run-environment.sh",
    "skills/calc-execute/scripts/sync/sync_calc_data.py",
    "skills/calc-execute/scripts/vasp/compare_incar_parameters.sh",
    "skills/calc-execute/scripts/vasp/plot_vasp_band.py",
    "skills/calc-execute/scripts/wannier90/vest2.py",
    "skills/calc-execute/scripts/wannier90/plot_wannier_fit_up.py",
    "skills/calc-execute/scripts/wannier90/plot_wannier_fit_dn.py",
    "skills/calc-execute/scripts/vampire/plot.py",
    "skills/calc-execute/scripts/vampire/pack_magnetic_results.sh",
)

_PLUGIN_ENTRIES = {
    ".codex-plugin",
    "skills",
    "tests",
    "conftest.py",
    "__pycache__",
    ".pytest_cache",
}
_SKILL_ENTRIES = {
    "SKILL.md",
    "agents",
    "references",
    "assets",
    "scripts",
    "tests",
    "__pycache__",
    ".pytest_cache",
}
_RUNTIME_DIRECTORIES = ("references", "assets", "scripts")
_EXCLUDED_PARTS = {"tests", "fixtures", "__pycache__", ".pytest_cache"}
_SCIENTIFIC_OUTPUT_NAMES = {
    "AECCAR0",
    "AECCAR1",
    "AECCAR2",
    "CHG",
    "CHGCAR",
    "CONTCAR",
    "DOSCAR",
    "EIGENVAL",
    "ELFCAR",
    "IBZKPT",
    "LOCPOT",
    "OSZICAR",
    "OUTCAR",
    "PARCHG",
    "PROCAR",
    "WAVECAR",
    "XDATCAR",
    "vasprun.xml",
}
_SCIENTIFIC_OUTPUT_SUFFIXES = {".h5", ".hdf", ".hdf5", ".npy", ".npz"}
_ABSOLUTE_PLUGIN_RESOURCE = re.compile(
    rb"(?:[A-Za-z]:[\\/]|/)[^\s`\"'()<>\[\]]*calc-project[\\/]"
    rb"(?:\.codex-plugin|resources|scripts|skills)[\\/]"
)


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _reject_symlinks(plugin_root: Path) -> None:
    if plugin_root.is_symlink():
        raise ValueError(f"symlink is not permitted: {plugin_root}")
    for path in plugin_root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symlink is not permitted: {_relative(path, plugin_root)}")


def _validate_exact_entries(root: Path, allowed: set[str], label: str) -> None:
    actual = {path.name for path in root.iterdir()}
    unknown = sorted(actual - allowed)
    if unknown:
        raise ValueError(f"unknown {label} top-level entries: {', '.join(unknown)}")


def _load_json_metadata(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"malformed metadata: {path}") from error
    if not isinstance(data, dict):
        raise ValueError(f"malformed metadata: {path}")
    return data


def _load_yaml_metadata(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValueError(f"malformed metadata: {path}") from error
    if not isinstance(data, dict):
        raise ValueError(f"malformed metadata: {path}")
    return data


def _validate_metadata(plugin_root: Path) -> None:
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = _load_json_metadata(manifest_path)
    interface = manifest.get("interface")
    prompts = interface.get("defaultPrompt") if isinstance(interface, dict) else None
    if (
        manifest.get("name") != "calc-project"
        or manifest.get("skills") != "./skills/"
        or not isinstance(prompts, list)
        or len(prompts) != len(SKILL_NAMES)
        or any(
            not isinstance(prompt, str) or f"${name}" not in prompt
            for name, prompt in zip(SKILL_NAMES, prompts, strict=True)
        )
    ):
        raise ValueError(f"malformed metadata: {manifest_path}")

    for name in SKILL_NAMES:
        metadata_path = plugin_root / "skills" / name / "agents" / "openai.yaml"
        metadata = _load_yaml_metadata(metadata_path)
        policy = metadata.get("policy")
        skill_interface = metadata.get("interface")
        if (
            not isinstance(policy, dict)
            or policy.get("allow_implicit_invocation") is not False
            or not isinstance(skill_interface, dict)
            or any(
                not isinstance(skill_interface.get(field), str)
                or not skill_interface[field].strip()
                for field in ("display_name", "short_description", "default_prompt")
            )
            or f"${name}" not in skill_interface["default_prompt"]
        ):
            raise ValueError(f"malformed metadata: {metadata_path}")


def _validate_runtime_file(path: Path, plugin_root: Path) -> None:
    relative = path.relative_to(plugin_root)
    if (
        path.name in _SCIENTIFIC_OUTPUT_NAMES
        or path.suffix.lower() in _SCIENTIFIC_OUTPUT_SUFFIXES
        or {"outputs", "logs"}.intersection(relative.parts)
    ):
        raise ValueError(f"scientific output is not permitted: {relative.as_posix()}")
    try:
        body = path.read_bytes()
    except OSError as error:
        raise ValueError(f"cannot read runtime file: {relative.as_posix()}") from error
    if _ABSOLUTE_PLUGIN_RESOURCE.search(body):
        raise ValueError(
            f"absolute resource path is not permitted: {relative.as_posix()}"
        )


def runtime_files(plugin_root: Path) -> list[Path]:
    """Return the sorted, validated files in the Calc Project runtime package."""
    original_root = Path(plugin_root)
    if original_root.is_symlink() or not original_root.is_dir():
        raise ValueError(f"required plugin root is not a real directory: {original_root}")
    plugin_root = original_root.resolve()
    _reject_symlinks(plugin_root)
    _validate_exact_entries(plugin_root, _PLUGIN_ENTRIES, "plugin")

    manifest_root = plugin_root / ".codex-plugin"
    if not manifest_root.is_dir():
        raise ValueError(f"required manifest directory is missing: {manifest_root}")
    _validate_exact_entries(manifest_root, {"plugin.json"}, "manifest")
    manifest = manifest_root / "plugin.json"
    skills_root = plugin_root / "skills"
    required_metadata = [manifest]
    if not skills_root.is_dir():
        raise ValueError(f"required skills directory is missing: {skills_root}")
    skill_entries = {
        path.name
        for path in skills_root.iterdir()
        if path.name not in {"__pycache__", ".pytest_cache"}
    }
    if skill_entries != set(SKILL_NAMES) or any(
        not (skills_root / name).is_dir() for name in SKILL_NAMES
    ):
        raise ValueError(
            "skills directory must contain exactly: " + ", ".join(SKILL_NAMES)
        )

    files: list[Path] = [manifest]
    for name in SKILL_NAMES:
        skill_root = skills_root / name
        _validate_exact_entries(skill_root, _SKILL_ENTRIES, f"skill {name}")
        skill_file = skill_root / "SKILL.md"
        metadata_file = skill_root / "agents" / "openai.yaml"
        required_metadata.extend((skill_file, metadata_file))
        files.extend((skill_file, metadata_file))

        agents_root = skill_root / "agents"
        if agents_root.is_dir():
            _validate_exact_entries(
                agents_root, {"openai.yaml", "__pycache__"}, f"skill {name} agents"
            )
        for directory in _RUNTIME_DIRECTORIES:
            root = skill_root / directory
            if not root.exists():
                continue
            if not root.is_dir():
                raise ValueError(f"unknown skill {name} runtime entry type: {directory}")
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file()
                and not _EXCLUDED_PARTS.intersection(path.relative_to(root).parts)
            )

    missing_metadata = [path for path in required_metadata if not path.is_file()]
    if missing_metadata:
        names = ", ".join(_relative(path, plugin_root) for path in missing_metadata)
        raise ValueError(f"required runtime metadata is missing: {names}")

    missing_assets = [
        relative
        for relative in REQUIRED_DT005_ASSETS
        if not (plugin_root / relative).is_file()
    ]
    if missing_assets:
        raise ValueError(f"required runtime asset is missing: {', '.join(missing_assets)}")

    _validate_metadata(plugin_root)
    unique_files = sorted(set(files), key=lambda path: _relative(path, plugin_root))
    for path in unique_files:
        _validate_runtime_file(path, plugin_root)
    return unique_files


def build_package(plugin_root: Path, output: Path) -> Path:
    """Write a new tar archive containing only validated runtime files."""
    plugin_root = Path(plugin_root)
    output = Path(output)
    if output.is_symlink() or output.exists():
        raise FileExistsError(output)
    output = output.resolve()
    files = runtime_files(plugin_root)
    plugin_root = plugin_root.resolve()
    with tarfile.open(output, "x") as archive:
        for path in files:
            info = archive.gettarinfo(str(path), arcname=_relative(path, plugin_root))
            with path.open("rb") as source:
                archive.addfile(info, source)
    return output


def _safe_member_path(member: tarfile.TarInfo) -> PurePosixPath:
    path = PurePosixPath(member.name)
    if (
        not member.name
        or "\\" in member.name
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
        or member.issym()
        or member.islnk()
        or not (member.isfile() or member.isdir())
    ):
        raise ValueError(f"unsafe archive member: {member.name}")
    return path


def safe_extract(package: Path, destination: Path) -> Path:
    """Extract regular archive files after rejecting traversal and link members."""
    package = Path(package).resolve(strict=True)
    destination = Path(destination)
    if destination.is_symlink() or destination.exists():
        raise FileExistsError(destination)
    destination = destination.resolve()

    with tarfile.open(package) as archive:
        members = archive.getmembers()
        paths = [_safe_member_path(member) for member in members]
        names = [path.as_posix() for path in paths]
        if len(names) != len(set(names)):
            raise ValueError("unsafe archive member: duplicate path")

        destination.mkdir(parents=True)
        directories: list[tuple[Path, int]] = []
        for member, relative in zip(members, paths, strict=True):
            target = destination.joinpath(*relative.parts)
            try:
                target.resolve().relative_to(destination)
            except ValueError as error:
                raise ValueError(f"unsafe archive member: {member.name}") from error
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                directories.append((target, member.mode))
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise ValueError(f"unsafe archive member: {member.name}")
            with source, target.open("xb") as installed:
                shutil.copyfileobj(source, installed)
            target.chmod(stat.S_IMODE(member.mode))
        for directory, mode in reversed(directories):
            directory.chmod(stat.S_IMODE(mode))
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    print(build_package(arguments.plugin_root, arguments.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
