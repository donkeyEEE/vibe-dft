#!/usr/bin/env python3
"""Validate the formal discovery boundary of paper-project knowledge."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    required = (
        root / "CONSUMER_CONTRACT.md",
        root / "cards/INDEX.md",
    )
    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path}")

    if errors:
        return errors

    card_index = (root / "cards/INDEX.md").read_text(encoding="utf-8")
    for path, text in ((root / "cards/INDEX.md", card_index),):
        if "candidates/" in text:
            errors.append(f"formal index contains forbidden candidates/ path: {path}")

    for card in sorted((root / "cards/atoms").glob("*.md")):
        if f"`{card.stem}`" not in card_index:
            errors.append(f"unindexed formal card: {card}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate formal paper-project knowledge indexes and cards."
    )
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()

    errors = validate_repository(args.repository.resolve())
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"valid paper-project knowledge directory: {args.repository.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
