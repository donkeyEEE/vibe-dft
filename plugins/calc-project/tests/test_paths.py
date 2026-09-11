from __future__ import annotations

import re
from pathlib import Path

import pytest


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("https://", "http://", "mailto:")

EXACT_RUNTIME_PATHS = {
    "skills/calc-setup/SKILL.md": (
        "scripts/verify_cluster_profile.sh",
    ),
    "skills/calc-execute/SKILL.md": (
        "assets/templates/common/run.sh.template",
        "assets/templates/vasp/cluster-env.sh.template",
        "assets/templates/vasp/scf/run.pbs.template",
        "assets/templates/vasp/band/run.pbs.template",
        "assets/templates/vasp/wannier-prerun/cluster-env.sh.template",
        "assets/templates/vasp/wannier-prerun/run.pbs.template",
        "assets/templates/wannier90/cluster-env.sh.template",
        "assets/templates/wannier90/run.pbs.template",
        "assets/templates/wannier90/wannier-run.env.template",
        "assets/templates/tb2j/cluster-env.sh.template",
        "assets/templates/tb2j/run.pbs.template",
        "assets/templates/vampire/cluster-env.sh.template",
        "assets/templates/vampire/run.pbs.template",
        "scripts/fingerprint_run.py",
        "scripts/probe-run-environment.sh",
        "scripts/sync/sync_calc_data.py",
        "scripts/vasp/compare_incar_parameters.sh",
        "scripts/vasp/plot_vasp_band.py",
        "scripts/wannier90/vest2.py",
        "scripts/wannier90/plot_wannier_fit_up.py",
        "scripts/wannier90/plot_wannier_fit_dn.py",
        "scripts/vampire/plot.py",
        "scripts/vampire/pack_magnetic_results.sh",
    ),
}


def _outside_fences(text: str):
    fenced = False
    marker = None
    for line in text.splitlines():
        stripped = line.lstrip()
        opening = stripped[:3]
        if opening in {"```", "~~~"}:
            if not fenced:
                fenced = True
                marker = opening
            elif opening == marker:
                fenced = False
                marker = None
            continue
        if not fenced:
            yield line


def _local_link_targets(markdown: Path):
    for line in _outside_fences(markdown.read_text(encoding="utf-8")):
        for raw_target in MARKDOWN_LINK.findall(line):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            path_part = target.split("#", 1)[0]
            if path_part and not path_part.startswith(EXTERNAL_PREFIXES):
                yield path_part


def assert_packaged_path(plugin_root: Path, source: Path, relative: str) -> None:
    candidate = source.parent / relative
    resolved_root = plugin_root.resolve()
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        raise AssertionError(f"broken or escaping packaged path: {source}: {relative}") from error


def assert_runtime_paths(plugin_root: Path, source: Path, paths: tuple[str, ...]) -> None:
    """Check exact packaged paths declared by an owning-skill contract test."""
    for relative in paths:
        assert_packaged_path(plugin_root, source, relative)


def test_markdown_links_resolve_inside_the_package(plugin_root):
    for markdown in plugin_root.rglob("*.md"):
        if "tests" in markdown.relative_to(plugin_root).parts:
            continue
        for target in _local_link_targets(markdown):
            assert_packaged_path(plugin_root, markdown, target)


def test_exact_asset_and_helper_references_resolve(plugin_root):
    for source_path, paths in EXACT_RUNTIME_PATHS.items():
        source = plugin_root / source_path
        assert source.is_file()
        assert_runtime_paths(plugin_root, source, paths)


def test_broken_relative_link_is_rejected(tmp_path):
    plugin = tmp_path / "calc-project"
    source = plugin / "skills" / "demo" / "SKILL.md"
    source.parent.mkdir(parents=True)
    source.write_text("[missing](references/missing.md)\n", encoding="utf-8")

    with pytest.raises(AssertionError, match="broken or escaping"):
        assert_packaged_path(plugin, source, next(_local_link_targets(source)))


def test_escaping_symlink_is_rejected(tmp_path):
    plugin = tmp_path / "calc-project"
    source = plugin / "skills" / "demo" / "SKILL.md"
    outside = tmp_path / "outside.md"
    source.parent.mkdir(parents=True)
    outside.write_text("outside\n", encoding="utf-8")
    (source.parent / "escape.md").symlink_to(outside)
    source.write_text("[escape](escape.md)\n", encoding="utf-8")

    with pytest.raises(AssertionError, match="broken or escaping"):
        assert_packaged_path(plugin, source, next(_local_link_targets(source)))
