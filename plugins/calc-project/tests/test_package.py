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


def test_runtime_package(plugin_root, tmp_path):
    builder = _load_builder()
    package = builder.build_package(plugin_root, tmp_path / "calc-project.tar")
    with tarfile.open(package) as archive:
        names = {item.name for item in archive.getmembers() if item.isfile()}
    expected = {
        path.relative_to(plugin_root).as_posix()
        for path in builder.runtime_files(plugin_root)
    }
    assert names == expected
    assert ".codex-plugin/plugin.json" in names
    assert "resources/progress-tracker.md" in names
    assert "resources/README.md" in names
    assert "skills/calc-execute/assets/templates/common/run.sh.template" in names
    assert REQUIRED_DT005_ASSETS <= set(names)
    assert not any(
        set(Path(name).parts)
        & {".git", ".worktrees", ".scratch", "tests", "__pycache__"}
        for name in names
    )


def test_runtime_inventory_is_sorted_and_independently_contains_dt005_assets(
    plugin_root,
):
    builder = _load_builder()

    names = _runtime_names(builder, plugin_root)

    assert names == sorted(names)
    assert len(names) == 86
    assert REQUIRED_DT005_ASSETS <= set(names)


def test_package_builder_requires_calculation_monitor_runtime(plugin_root):
    builder = _load_builder()

    assert REQUIRED_DT005_ASSETS <= set(builder.REQUIRED_DT005_ASSETS)


@pytest.mark.parametrize(
    "relative",
    (
        ".codex-plugin/plugin.json",
        "skills/calc-review/SKILL.md",
        "skills/calc-review/agents/openai.yaml",
    ),
)
def test_missing_required_metadata_is_rejected(plugin_root, tmp_path, relative):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    (copy / relative).unlink()

    with pytest.raises(ValueError, match="required"):
        builder.runtime_files(copy)


def test_removed_helper_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    (copy / "skills/calc-execute/scripts/fingerprint_run.py").unlink()

    with pytest.raises(ValueError, match="fingerprint_run.py"):
        builder.runtime_files(copy)


def test_omitted_template_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    (copy / "skills/calc-execute/assets/templates/common/run.sh.template").unlink()

    with pytest.raises(ValueError, match="run.sh.template"):
        builder.runtime_files(copy)


@pytest.mark.parametrize("metadata", ("manifest", "agent"))
def test_malformed_metadata_is_rejected(plugin_root, tmp_path, metadata):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    path = (
        copy / ".codex-plugin/plugin.json"
        if metadata == "manifest"
        else copy / "skills/calc-rq/agents/openai.yaml"
    )
    path.write_text("{not valid metadata", encoding="utf-8")

    with pytest.raises(ValueError, match="metadata"):
        builder.runtime_files(copy)


def test_ninth_skill_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    shutil.copytree(copy / "skills/ask-lyz", copy / "skills/ninth")

    with pytest.raises(ValueError, match="exactly"):
        builder.runtime_files(copy)


def test_missing_progress_tracker_contract_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    (copy / "resources/progress-tracker.md").unlink()

    with pytest.raises(ValueError, match="required shared resource"):
        builder.runtime_files(copy)


@pytest.mark.parametrize(
    ("relative", "kind"),
    (
        ("README.md", "file"),
        ("unknown-resources", "directory"),
        (".codex-plugin/extra.json", "file"),
        ("skills/calc-rq/NOTES.md", "file"),
    ),
)
def test_unknown_runtime_top_level_entry_is_rejected(
    plugin_root, tmp_path, relative, kind
):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    path = copy / relative
    if kind == "directory":
        path.mkdir()
    else:
        path.write_text("unknown\n", encoding="utf-8")

    with pytest.raises(ValueError, match="unknown"):
        builder.runtime_files(copy)


def test_symlink_is_rejected_even_when_it_points_inside_plugin(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    link = copy / "skills/calc-execute/scripts/fingerprint-link.py"
    link.symlink_to("fingerprint_run.py")

    with pytest.raises(ValueError, match="symlink"):
        builder.runtime_files(copy)


def test_build_rejects_a_symlinked_plugin_root(plugin_root, tmp_path):
    builder = _load_builder()
    link = tmp_path / "linked-plugin"
    link.symlink_to(plugin_root, target_is_directory=True)

    with pytest.raises(ValueError, match="symlink"):
        builder.build_package(link, tmp_path / "calc-project.tar")


def test_stale_absolute_resource_path_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    skill = copy / "skills/calc-rq/SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8")
        + "\nStale: /home/old/yz-skills/plugins/calc-project/resources/template.md\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="absolute resource"):
        builder.runtime_files(copy)


def test_accidental_scientific_output_is_rejected(plugin_root, tmp_path):
    builder = _load_builder()
    copy = _copy_plugin(plugin_root, tmp_path)
    output = copy / "skills/calc-execute/assets/templates/vasp/CHGCAR"
    output.write_bytes(b"synthetic scientific output\n")

    with pytest.raises(ValueError, match="scientific output"):
        builder.runtime_files(copy)


def test_build_refuses_to_replace_an_existing_archive(plugin_root, tmp_path):
    builder = _load_builder()
    output = tmp_path / "calc-project.tar"
    output.write_bytes(b"preserve me")

    with pytest.raises(FileExistsError):
        builder.build_package(plugin_root, output)
    assert output.read_bytes() == b"preserve me"


def test_build_refuses_dangling_output_symlink_without_creating_target(
    plugin_root, tmp_path
):
    builder = _load_builder()
    target = tmp_path / "absent-archive-target.tar"
    output = tmp_path / "calc-project.tar"
    output.symlink_to(target)

    with pytest.raises(FileExistsError):
        builder.build_package(plugin_root, output)
    assert output.is_symlink()
    assert output.readlink() == target
    assert not target.exists()


def test_safe_extraction_preserves_every_file_byte_and_permission(plugin_root, tmp_path):
    builder = _load_builder()
    package = builder.build_package(plugin_root, tmp_path / "calc-project.tar")
    extracted = builder.safe_extract(package, tmp_path / "external/calc-project")

    for source in builder.runtime_files(plugin_root):
        relative = source.relative_to(plugin_root)
        installed = extracted / relative
        assert _sha256(installed) == _sha256(source), relative
        assert stat.S_IMODE(installed.stat().st_mode) == stat.S_IMODE(
            source.stat().st_mode
        ), relative


@pytest.mark.parametrize("member_kind", ("absolute", "traversal", "symlink", "hardlink"))
def test_safe_extraction_rejects_malicious_members(tmp_path, member_kind):
    builder = _load_builder()
    package = tmp_path / f"{member_kind}.tar"
    with tarfile.open(package, "w") as archive:
        item = tarfile.TarInfo(
            "/absolute.txt" if member_kind == "absolute" else "../outside.txt"
        )
        if member_kind in {"symlink", "hardlink"}:
            item.name = "inside.txt"
            item.type = tarfile.SYMTYPE if member_kind == "symlink" else tarfile.LNKTYPE
            item.linkname = "../outside.txt"
            archive.addfile(item)
        else:
            body = b"malicious\n"
            item.size = len(body)
            archive.addfile(item, io.BytesIO(body))

    with pytest.raises(ValueError, match="unsafe archive member"):
        builder.safe_extract(package, tmp_path / "extract")
    assert not (tmp_path / "outside.txt").exists()


def test_safe_extraction_validates_all_members_before_creating_destination(tmp_path):
    builder = _load_builder()
    package = tmp_path / "late-traversal.tar"
    with tarfile.open(package, "w") as archive:
        body = b"must not be written\n"
        safe = tarfile.TarInfo("safe.txt")
        safe.size = len(body)
        archive.addfile(safe, io.BytesIO(body))
        unsafe = tarfile.TarInfo("safe/../../outside.txt")
        unsafe.size = len(body)
        archive.addfile(unsafe, io.BytesIO(body))

    destination = tmp_path / "extract"
    with pytest.raises(ValueError, match="unsafe archive member"):
        builder.safe_extract(package, destination)
    assert not destination.exists()
    assert not (tmp_path / "outside.txt").exists()


def test_safe_extraction_refuses_existing_destination_without_altering_it(tmp_path):
    builder = _load_builder()
    package = tmp_path / "safe.tar"
    with tarfile.open(package, "w") as archive:
        body = b"new\n"
        item = tarfile.TarInfo("file.txt")
        item.size = len(body)
        archive.addfile(item, io.BytesIO(body))
    destination = tmp_path / "extract"
    destination.mkdir()
    sentinel = destination / "sentinel.txt"
    sentinel.write_bytes(b"preserve me")

    with pytest.raises(FileExistsError):
        builder.safe_extract(package, destination)
    assert sentinel.read_bytes() == b"preserve me"
    assert not (destination / "file.txt").exists()


def test_safe_extraction_refuses_dangling_destination_symlink_without_creating_target(
    tmp_path,
):
    builder = _load_builder()
    package = tmp_path / "safe.tar"
    with tarfile.open(package, "w") as archive:
        body = b"new\n"
        item = tarfile.TarInfo("file.txt")
        item.size = len(body)
        archive.addfile(item, io.BytesIO(body))
    target = tmp_path / "absent-extraction-target"
    destination = tmp_path / "extract"
    destination.symlink_to(target, target_is_directory=True)

    with pytest.raises(FileExistsError):
        builder.safe_extract(package, destination)
    assert destination.is_symlink()
    assert destination.readlink() == target
    assert not target.exists()


def test_cli_builds_the_requested_archive(plugin_root, tmp_path):
    output = tmp_path / "cli/calc-project.tar"
    output.parent.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("build_acceptance_package.py")),
            "--plugin-root",
            str(plugin_root),
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert Path(result.stdout.strip()) == output.resolve()
    assert output.is_file()


def test_manifest_and_skill_metadata_describe_exact_explicit_roster(plugin_root):
    manifest = json.loads(
        (plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    expected = (
        "ask-lyz",
        "calc-setup",
        "calc-rq",
        "calc-to-spec",
        "calc-execute",
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


def test_documentation_distinguishes_skill_calls_from_local_file_references(
    plugin_root,
):
    rq = (plugin_root / "skills/calc-rq/SKILL.md").read_text(encoding="utf-8")

    assert "调用 `$dev-engineering:grill-with-docs`" in rq
    assert "[RQ 模板](references/rq-template.md)" in rq
    assert "]($" not in rq


def test_business_skills_handoff_automatically_but_router_only_recommends(plugin_root):
    skills = plugin_root / "skills"
    router = (skills / "ask-lyz/SKILL.md").read_text(encoding="utf-8")
    rq = (skills / "calc-rq/SKILL.md").read_text(encoding="utf-8")
    spec = (skills / "calc-to-spec/SKILL.md").read_text(encoding="utf-8")
    execute = (skills / "calc-execute/SKILL.md").read_text(encoding="utf-8")
    router_flat = " ".join(router.split())
    execute_flat = " ".join(execute.split())

    assert "推荐 sibling，不自动调用它" in router_flat
    assert "直接进入 `$calc-to-spec`" in rq
    assert "直接进入 `$calc-execute`" in spec
    assert "先加载 `$calc-setup`" in execute_flat
    assert "调用 `$calc-rq`" in execute_flat
    assert "does not invoke the sibling automatically" not in spec
    assert "not authorization to\ninvoke a sibling automatically" not in rq


def test_readme_describes_requalifiable_run_inputs(plugin_root):
    readme = (plugin_root.parents[1] / "README.md").read_text(encoding="utf-8")
    readme_flat = " ".join(readme.split())

    assert "Run 目录保存不可变 `inputs/`" not in readme_flat
    assert "每次验证与评审固定当时的输入快照" in readme_flat
    assert "符合条件的当前 Run 可原地纠正" in readme_flat
