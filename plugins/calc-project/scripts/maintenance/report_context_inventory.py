#!/usr/bin/env python3
"""Report a reproducible, approximate context inventory for calc-project."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-root", type=Path, required=True)
    return parser.parse_args()


def inventory_files(plugin_root: Path) -> list[dict[str, int | str]]:
    skills = plugin_root / "skills"
    paths = sorted(
        set(skills.glob("**/SKILL.md")) | set(skills.glob("**/references/**/*.md")),
        key=lambda path: path.relative_to(plugin_root).as_posix(),
    )
    records: list[dict[str, int | str]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        records.append(
            {
                "path": path.relative_to(plugin_root).as_posix(),
                "bytes": len(text.encode("utf-8")),
                "lines": len(text.splitlines()),
                "estimated_tokens": math.ceil(len(text) / 4),
            }
        )
    return records


def find_duplicates(plugin_root: Path) -> list[dict[str, object]]:
    occurrences: dict[str, set[str]] = defaultdict(set)
    for record in inventory_files(plugin_root):
        path = plugin_root / str(record["path"])
        for line in path.read_text(encoding="utf-8").splitlines():
            normalized = " ".join(line.split())
            if len(normalized) >= 12 and not normalized.startswith("#"):
                occurrences[normalized].add(str(record["path"]))
    return [
        {"line": line, "paths": sorted(paths)}
        for line, paths in sorted(occurrences.items())
        if len(paths) >= 2
    ]


def main() -> None:
    args = parse_args()
    files = inventory_files(args.plugin_root)
    payload = {
        "files": files,
        "totals": {
            "bytes": sum(int(item["bytes"]) for item in files),
            "lines": sum(int(item["lines"]) for item in files),
            "estimated_tokens": sum(int(item["estimated_tokens"]) for item in files),
            "token_estimate_note": "estimated_tokens is ceil(character_count / 4), not model-token exact.",
        },
        "duplicates": find_duplicates(args.plugin_root),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
