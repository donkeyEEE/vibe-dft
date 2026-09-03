#!/usr/bin/env python3
"""Validate the formal discovery boundary of research-knowledge."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


PHYSICS_CATEGORIES = ("concepts", "phenomena", "theories-and-models")


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    required = (
        root / "CONSUMER_CONTRACT.md",
        root / "cards/INDEX.md",
        root / "cards/physics/PHYSICS_INDEX.md",
        root / "templates/INDEX.md",
    )
    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path}")

    if errors:
        return errors

    card_index = (root / "cards/INDEX.md").read_text(encoding="utf-8")
    physics_index = (root / "cards/physics/PHYSICS_INDEX.md").read_text(
        encoding="utf-8"
    )
    template_index = (root / "templates/INDEX.md").read_text(encoding="utf-8")

    for path, text in (
        (root / "cards/INDEX.md", card_index),
        (root / "cards/physics/PHYSICS_INDEX.md", physics_index),
        (root / "templates/INDEX.md", template_index),
    ):
        if "candidates/" in text:
            errors.append(f"formal index contains forbidden candidates/ path: {path}")

    for card in sorted((root / "cards/atoms").glob("*.md")):
        if f"`{card.stem}`" not in card_index:
            errors.append(f"unindexed formal card: {card}")

    physics_root = root / "cards/physics"
    for category in PHYSICS_CATEGORIES:
        for card in sorted((physics_root / category).glob("phys-*.md")):
            matches = [line for line in physics_index.splitlines() if card.name in line]
            if len(matches) != 1:
                errors.append(f"physics card must have one index row: {card}")

    template_root = root / "templates/computation"
    for template in sorted(template_root.rglob("*.template")):
        relative = template.relative_to(template_root).as_posix()
        if f"`{relative}`" not in template_index:
            errors.append(f"unindexed formal template: {template}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate formal research-knowledge indexes and resources."
    )
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()

    errors = validate_repository(args.repository.resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"valid research knowledge repository: {args.repository.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
