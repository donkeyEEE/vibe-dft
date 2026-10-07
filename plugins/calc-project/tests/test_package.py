from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import shutil
import stat
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest


REQUIRED_DT005_ASSETS = {
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
    "skills/calc-execute/references/calculation-troubleshooting.md",
    "skills/calc-execute/scripts/probe-run-environment.sh",
    "skills/calc-execute/scripts/sync/sync_calc_data.py",
    "skills/calc-execute/scripts/vasp/compare_incar_parameters.sh",
    "skills/calc-execute/scripts/vasp/plot_vasp_band.py",
    "skills/calc-execute/scripts/wannier90/vest2.py",
    "skills/calc-execute/scripts/wannier90/plot_wannier_fit_up.py",
    "skills/calc-execute/scripts/wannier90/plot_wannier_fit_dn.py",
    "skills/calc-execute/scripts/vampire/plot.py",
    "skills/calc-execute/scripts/vampire/pack_magnetic_results.sh",
}


def _load_builder():
    script = Path(__file__).with_name("build_acceptance_package.py")
    spec = importlib.util.spec_from_file_location("package_builder", script)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    return builder


def _copy_plugin(plugin_root: Path, tmp_path: Path) -> Path:
    copy = tmp_path / "calc-project"
    shutil.copytree(
        plugin_root,
        copy,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
    )
    return copy


def _runtime_names(builder, plugin_root: Path) -> list[str]:
    return [
        path.relative_to(plugin_root).as_posix()
        for path in builder.runtime_files(plugin_root)
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_runtime_package_inventory_round_trip_cli_and_workflow_metadata(plugin_root, tmp_path):
    builder = _load_builder()
    sources = builder.runtime_files(plugin_root)
    names = _runtime_names(builder, plugin_root)
    assert names == sorted(names)
    assert len(names) == 96
    assert REQUIRED_DT005_ASSETS <= set(names)
    assert REQUIRED_DT005_ASSETS <= set(builder.REQUIRED_DT005_ASSETS)
    assert {
        ".codex-plugin/plugin.json", "resources/README.md", "resources/project-context.md",
        "resources/progress-tracker.md", "resources/progress-tracker-maintenance.md",
        "skills/calc-issue/SKILL.md", "skills/calc-issue/agents/openai.yaml",
        "skills/calc-issue/references/issue-record.md",
        "skills/domain-research/SKILL.md", "skills/domain-research/agents/openai.yaml",
        "skills/domain-research/references/research-context.md",
        "skills/domain-research/references/research-writing.md",
        "skills/domain-research/references/research-reasoning.md",
    } <= set(names)
    assert not any(
        set(Path(name).parts) & {".git", ".worktrees", ".scratch", "tests", "__pycache__"}
        for name in names
    )
    package = builder.build_package(plugin_root, tmp_path / "calc-project.tar")
    with tarfile.open(package) as archive:
        assert {item.name for item in archive.getmembers() if item.isfile()} == set(names)
    extracted = builder.safe_extract(package, tmp_path / "external/calc-project")
    for source in sources:
        relative = source.relative_to(plugin_root)
        installed = extracted / relative
        assert _sha256(installed) == _sha256(source), relative
        assert stat.S_IMODE(installed.stat().st_mode) == stat.S_IMODE(source.stat().st_mode), relative

    output = tmp_path / "cli/calc-project.tar"
    output.parent.mkdir()
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("build_acceptance_package.py")),
         "--plugin-root", str(plugin_root), "--output", str(output)],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()) == output.resolve()
    assert output.is_file()

    manifest = json.loads(
        (plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    expected = (
        "ask-lyz",
        "calc-setup",
        "calc-rq",
        "domain-research",
        "calc-to-spec",
        "calc-execute",
        "calc-issue",
        "calc-report",
        "calc-review",
        "show-cot",
    )

    assert manifest["skills"] == "./skills/"
    assert len(manifest["interface"]["defaultPrompt"]) == len(expected)
    assert all(
        f"${name}" in prompt
        for name, prompt in zip(
            expected, manifest["interface"]["defaultPrompt"], strict=True
        )
    )

    rq = (plugin_root / "skills/calc-rq/SKILL.md").read_text(encoding="utf-8")

    assert "调用 `$dev-engineering:grill-with-docs`" in rq
    assert "[RQ 模板](references/rq-template.md)" in rq
    assert "]($" not in rq

    skills = plugin_root / "skills"
    router = (skills / "ask-lyz/SKILL.md").read_text(encoding="utf-8")
    rq = (skills / "calc-rq/SKILL.md").read_text(encoding="utf-8")
    spec = (skills / "calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    execute = (skills / "calc-execute/SKILL.md").read_text(encoding="utf-8")
    router_flat = " ".join(router.split())
    execute_flat = " ".join(execute.split())

    assert "推荐相应技能，不自动调用它" in router_flat
    assert "直接进入 `$calc-to-spec`" in rq
    assert "直接进入 `$calc-execute`" in spec
    assert "先加载 `$calc-setup`" in execute_flat
    assert "RQ 变更交 `$calc-rq`" in execute_flat
    assert "does not invoke the sibling automatically" not in spec
    assert "not authorization to\ninvoke a sibling automatically" not in rq

    readme = (plugin_root.parents[1] / "README.md").read_text(encoding="utf-8")
    readme_flat = " ".join(readme.split())

    assert "Run 目录保存不可变 `inputs/`" not in readme_flat
    assert "每次验证与评审固定当时的输入快照" in readme_flat
    assert "符合条件的当前 Run 可原地纠正" in readme_flat


def test_runtime_package_rejects_invalid_sources_and_preserves_existing_outputs(plugin_root, tmp_path):
    builder = _load_builder()
    missing = (
        (".codex-plugin/plugin.json", "required"),
        ("skills/calc-review/SKILL.md", "required"),
        ("skills/calc-review/agents/openai.yaml", "required"),
        ("skills/calc-issue/SKILL.md", "required"),
        ("skills/calc-issue/agents/openai.yaml", "required"),
        ("skills/calc-execute/scripts/fingerprint_run.py", "fingerprint_run.py"),
        ("skills/calc-execute/assets/templates/common/run.sh.template", "run.sh.template"),
        ("resources/progress-tracker.md", "required shared resource"),
    )
    cases = [("missing", path, error) for path, error in missing] + [
        ("malformed", ".codex-plugin/plugin.json", "metadata"),
        ("malformed", "skills/calc-rq/agents/openai.yaml", "metadata"),
        ("skill", "skills/ninth", "exactly"),
        ("file", "README.md", "unknown"),
        ("directory", "unknown-resources", "unknown"),
        ("file", ".codex-plugin/extra.json", "unknown"),
        ("file", "skills/calc-rq/NOTES.md", "unknown"),
        ("symlink", "skills/calc-execute/scripts/fingerprint-link.py", "symlink"),
        ("stale", "skills/calc-rq/SKILL.md", "absolute resource"),
        ("file", "skills/calc-execute/assets/templates/vasp/CHGCAR", "scientific output"),
    ]
    for index, (kind, relative, error) in enumerate(cases):
        copy = _copy_plugin(plugin_root, tmp_path / str(index))
        path = copy / relative
        if kind == "missing":
            path.unlink()
        elif kind == "skill":
            shutil.copytree(copy / "skills/ask-lyz", path)
        elif kind == "directory":
            path.mkdir()
        elif kind == "symlink":
            path.symlink_to("fingerprint_run.py")
        elif kind == "stale":
            path.write_text(path.read_text() + "\nStale: /home/old/yz-skills/plugins/calc-project/resources/template.md\n")
        else:
            path.write_text("{not valid metadata" if kind == "malformed" else "unknown\n")
        with pytest.raises(ValueError, match=error):
            builder.runtime_files(copy)

    link = tmp_path / "linked-plugin"
    link.symlink_to(plugin_root, target_is_directory=True)
    with pytest.raises(ValueError, match="not a real directory"):
        builder.build_package(link, tmp_path / "from-link.tar")
    for dangling in (False, True):
        output = tmp_path / f"existing-{dangling}.tar"
        target = tmp_path / "absent-archive-target.tar"
        if dangling:
            output.symlink_to(target)
        else:
            output.write_bytes(b"preserve me")
        with pytest.raises(FileExistsError):
            builder.build_package(plugin_root, output)
        if dangling:
            assert output.is_symlink() and output.readlink() == target
            assert not target.exists()
        else:
            assert output.read_bytes() == b"preserve me"


def test_safe_extraction_rejects_unsafe_members_and_preserves_destinations(tmp_path):
    builder = _load_builder()
    for kind in ("absolute", "traversal", "symlink", "hardlink", "late-traversal"):
        package = tmp_path / f"{kind}.tar"
        with tarfile.open(package, "w") as archive:
            if kind == "late-traversal":
                safe = tarfile.TarInfo("safe.txt")
                safe.size = 1
                archive.addfile(safe, io.BytesIO(b"x"))
            name = {"absolute": "/absolute.txt", "late-traversal": "safe/../../outside.txt"}.get(kind, "../outside.txt")
            item = tarfile.TarInfo(name)
            if kind in {"symlink", "hardlink"}:
                item.name = "inside.txt"
                item.type = tarfile.SYMTYPE if kind == "symlink" else tarfile.LNKTYPE
                item.linkname = "../outside.txt"
                archive.addfile(item)
            else:
                item.size = 1
                archive.addfile(item, io.BytesIO(b"x"))
        destination = tmp_path / f"extract-{kind}"
        with pytest.raises(ValueError, match="unsafe archive member"):
            builder.safe_extract(package, destination)
        assert not destination.exists()
        assert not (tmp_path / "outside.txt").exists()

    package = tmp_path / "safe.tar"
    with tarfile.open(package, "w") as archive:
        item = tarfile.TarInfo("file.txt")
        item.size = 4
        archive.addfile(item, io.BytesIO(b"new\n"))
    for dangling in (False, True):
        destination = tmp_path / f"existing-{dangling}"
        target = tmp_path / "absent-extraction-target"
        if dangling:
            destination.symlink_to(target, target_is_directory=True)
        else:
            destination.mkdir()
            sentinel = destination / "sentinel.txt"
            sentinel.write_bytes(b"preserve me")
        with pytest.raises(FileExistsError):
            builder.safe_extract(package, destination)
        if dangling:
            assert destination.is_symlink() and destination.readlink() == target
            assert not target.exists()
        else:
            assert sentinel.read_bytes() == b"preserve me"
            assert not (destination / "file.txt").exists()
