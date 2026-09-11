from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_setup_configuration_pointer(plugin_root):
    text = (plugin_root / "skills/calc-setup/references/project-structure.md").read_text()
    for field in (
        "Calculation Configuration",
        "Data root:",
        "Tracker adapter:",
        "RQ location:",
    ):
        assert field in text
    assert "01-rqs/" in text


def _profile(path: Path) -> Path:
    profile = path / "software-profiles.md"
    profile.write_text(
        """# Software profiles

This unrelated paragraph must survive verification.

<!-- cluster-profile-status:start -->
old evidence
<!-- cluster-profile-status:end -->
""",
        encoding="utf-8",
    )
    return profile


def _fake_ssh(path: Path) -> tuple[Path, Path]:
    bin_dir = path / "bin"
    bin_dir.mkdir(exist_ok=True)
    argv_file = path / "ssh.argv"
    ssh = bin_dir / "ssh"
    ssh.write_text(
        """#!/bin/sh
printf '%s\\n' "$@" > "$FAKE_SSH_ARGV"
printf '%s\\n' "$FAKE_SSH_OUTPUT"
exit "$FAKE_SSH_STATUS"
""",
        encoding="utf-8",
    )
    ssh.chmod(0o755)
    return bin_dir, argv_file


def _run_verifier(
    plugin_root: Path,
    tmp_path: Path,
    profile: Path,
    *,
    status: int,
    output: str,
    label: str = "VASP standard",
    command: str = "test -x /reviewed/vasp_std",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    bin_dir, argv_file = _fake_ssh(tmp_path)
    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}{os.pathsep}{env['PATH']}",
        FAKE_SSH_ARGV=str(argv_file),
        FAKE_SSH_STATUS=str(status),
        FAKE_SSH_OUTPUT=output,
    )
    script = plugin_root / "skills/calc-setup/scripts/verify_cluster_profile.sh"
    result = subprocess.run(
        [
            "bash",
            str(script),
            str(profile),
            "cluster.example",
            label,
            command,
        ],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    return result, argv_file


def test_verifier_records_supplied_successful_probe(plugin_root, tmp_path):
    profile = _profile(tmp_path)

    result, argv_file = _run_verifier(
        plugin_root, tmp_path, profile, status=0, output="probe available"
    )

    assert result.returncode == 0
    assert argv_file.read_text(encoding="utf-8").splitlines() == [
        "--",
        "cluster.example",
        "test -x /reviewed/vasp_std",
    ]
    text = profile.read_text(encoding="utf-8")
    assert "This unrelated paragraph must survive verification." in text
    assert "VASP standard" in text
    assert "test -x /reviewed/vasp_std" in text
    assert "probe available" in text
    assert "| verified |" in text
    assert "old evidence" not in text


def test_verifier_records_ssh_failure_as_unavailable(plugin_root, tmp_path):
    profile = _profile(tmp_path)

    result, argv_file = _run_verifier(
        plugin_root, tmp_path, profile, status=255, output="connection refused"
    )

    assert result.returncode == 1
    assert argv_file.exists()
    text = profile.read_text(encoding="utf-8")
    assert "This unrelated paragraph must survive verification." in text
    assert "connection refused" in text
    assert "| unavailable |" in text
    assert "| verified |" not in text


def test_verifier_retains_other_components_and_replaces_matching_component(
    plugin_root, tmp_path
):
    profile = _profile(tmp_path)

    first, _ = _run_verifier(
        plugin_root,
        tmp_path,
        profile,
        status=0,
        output="vasp first",
        label="VASP standard",
        command="test -x /reviewed/vasp_std",
    )
    second, _ = _run_verifier(
        plugin_root,
        tmp_path,
        profile,
        status=0,
        output="wannier available",
        label="Wannier90",
        command="test -x /reviewed/wannier90.x",
    )
    repeated, _ = _run_verifier(
        plugin_root,
        tmp_path,
        profile,
        status=255,
        output="vasp moved",
        label="VASP standard",
        command="test -x /new/vasp_std",
    )

    assert [first.returncode, second.returncode, repeated.returncode] == [0, 0, 1]
    text = profile.read_text(encoding="utf-8")
    assert text.count("| VASP standard |") == 1
    assert "test -x /new/vasp_std" in text
    assert "vasp moved" in text
    assert "vasp first" not in text
    assert text.count("| Wannier90 |") == 1
    assert "wannier available" in text


def test_verifier_rejects_reversed_markers_without_modifying_profile(
    plugin_root, tmp_path
):
    profile = tmp_path / "software-profiles.md"
    original = """# Profile
<!-- cluster-profile-status:end -->
Following text must survive.
<!-- cluster-profile-status:start -->
"""
    profile.write_text(original, encoding="utf-8")

    result, argv_file = _run_verifier(
        plugin_root, tmp_path, profile, status=0, output="unexpected"
    )

    assert result.returncode != 0
    assert not argv_file.exists()
    assert profile.read_text(encoding="utf-8") == original


def test_verifier_marks_truncated_output_summary(plugin_root, tmp_path):
    profile = _profile(tmp_path)
    long_output = "begin-" + ("x" * 400) + "-tail"

    result, _ = _run_verifier(
        plugin_root, tmp_path, profile, status=0, output=long_output
    )

    assert result.returncode == 0
    text = profile.read_text(encoding="utf-8")
    assert "begin-" in text
    assert "[truncated]" in text
    assert "-tail" not in text


def test_verifier_rejects_invalid_invocations_without_ssh(plugin_root, tmp_path):
    profile = _profile(tmp_path)
    bin_dir, argv_file = _fake_ssh(tmp_path)
    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}{os.pathsep}{env['PATH']}",
        FAKE_SSH_ARGV=str(argv_file),
        FAKE_SSH_STATUS="0",
        FAKE_SSH_OUTPUT="unexpected",
    )
    script = plugin_root / "skills/calc-setup/scripts/verify_cluster_profile.sh"

    cases = [
        [],
        [str(tmp_path / "missing.md"), "cluster.example", "label", "true"],
        [str(profile), "-oProxyCommand=bad", "label", "true"],
    ]
    for args in cases:
        result = subprocess.run(
            ["bash", str(script), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        assert result.returncode != 0

    assert not argv_file.exists()
