from __future__ import annotations

import os
import subprocess
from pathlib import Path




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



def test_setup_configuration_and_verifier_evidence_preserve_other_components(plugin_root, tmp_path):
    structure = (plugin_root / "skills/calc-setup/references/project-structure.md").read_text()
    for field in ("Calculation Configuration", "Data root:", "Tracker adapter:", "RQ location:", "01-rqs/"):
        assert field in structure

    for status, output in ((0, "probe available"), (255, "connection refused")):
        directory = tmp_path / str(status)
        directory.mkdir()
        profile = _profile(directory)
        result, argv_file = _run_verifier(plugin_root, directory, profile, status=status, output=output)
        assert result.returncode == (0 if status == 0 else 1)
        assert argv_file.read_text().splitlines() == [
            "--", "cluster.example", "test -x /reviewed/vasp_std",
        ]
        text = profile.read_text()
        assert "This unrelated paragraph must survive verification." in text
        assert "VASP standard" in text and "test -x /reviewed/vasp_std" in text
        assert output in text
        assert ("| verified |" in text) is (status == 0)
        assert ("| unavailable |" in text) is (status != 0)
        assert "old evidence" not in text

    profile = _profile(tmp_path)
    results = []
    for label, command, status, output in (
        ("VASP standard", "test -x /reviewed/vasp_std", 0, "vasp first"),
        ("Wannier90", "test -x /reviewed/wannier90.x", 0, "wannier available"),
        ("VASP standard", "test -x /new/vasp_std", 255, "vasp moved"),
    ):
        result, _ = _run_verifier(
            plugin_root, tmp_path, profile, label=label, command=command, status=status, output=output,
        )
        results.append(result.returncode)
    assert results == [0, 0, 1]
    text = profile.read_text()
    assert text.count("| VASP standard |") == 1
    assert "test -x /new/vasp_std" in text and "vasp moved" in text
    assert "vasp first" not in text
    assert text.count("| Wannier90 |") == 1 and "wannier available" in text

    result, _ = _run_verifier(
        plugin_root, tmp_path, profile, status=0, output="begin-" + "x" * 400 + "-tail",
    )
    assert result.returncode == 0
    text = profile.read_text()
    assert "begin-" in text and "[truncated]" in text and "-tail" not in text


def test_setup_verifier_rejects_invalid_requests_without_ssh_or_profile_changes(plugin_root, tmp_path):
    profile = tmp_path / "software-profiles.md"
    original = """# Profile
<!-- cluster-profile-status:end -->
Following text must survive.
<!-- cluster-profile-status:start -->
"""
    profile.write_text(original)
    result, argv_file = _run_verifier(plugin_root, tmp_path, profile, status=0, output="unexpected")
    assert result.returncode != 0
    assert not argv_file.exists()
    assert profile.read_text() == original

    profile = _profile(tmp_path)
    original = profile.read_bytes()
    bin_dir, argv_file = _fake_ssh(tmp_path)
    env = os.environ.copy()
    env.update(
        PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", FAKE_SSH_ARGV=str(argv_file),
        FAKE_SSH_STATUS="0", FAKE_SSH_OUTPUT="unexpected",
    )
    script = plugin_root / "skills/calc-setup/scripts/verify_cluster_profile.sh"
    for args in (
        [], [str(tmp_path / "missing.md"), "cluster.example", "label", "true"],
        [str(profile), "-oProxyCommand=bad", "label", "true"],
    ):
        result = subprocess.run(["bash", str(script), *args], text=True, capture_output=True, env=env)
        assert result.returncode != 0
        assert not argv_file.exists()
        assert profile.read_bytes() == original
