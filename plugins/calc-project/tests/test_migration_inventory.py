from __future__ import annotations

import json
import subprocess
from pathlib import Path


BASELINE = "3e5cadc7f8343aedc462bc3df5ae4d123ee8ad58"
PREFIX = "plugins/calc-project/"


def _records(plugin_root: Path):
    fixture = plugin_root / "tests" / "fixtures" / "migration_inventory.json"
    return json.loads(fixture.read_text(encoding="utf-8"))


def _baseline_sources(plugin_root: Path) -> set[str]:
    output = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            BASELINE,
            "--",
            ":(top)plugins/calc-project",
        ],
        cwd=plugin_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return {path.removeprefix(PREFIX) for path in output}


def test_inventory_accounts_for_every_baseline_source_once(plugin_root):
    records = _records(plugin_root)
    sources = [record["source"] for record in records]

    assert len(records) == 65
    assert len(sources) == len(set(sources))
    assert set(sources) == _baseline_sources(plugin_root)
    assert all(set(record) == {"source", "targets", "reason"} for record in records)
    assert all(record["targets"] or record["reason"] for record in records)
    assert all(not (record["targets"] and record["reason"]) for record in records)


def test_every_retained_source_has_concrete_existing_targets(plugin_root):
    missing = []
    for record in _records(plugin_root):
        for target in record["targets"]:
            if not (plugin_root / target).is_file():
                missing.append((record["source"], target))

    assert missing == []
