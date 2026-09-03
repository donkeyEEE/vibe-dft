#!/usr/bin/env python3
"""Build the minimal source-material directory consumed by PPT Master."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from tempfile import mkdtemp
from typing import Sequence


@dataclass(frozen=True)
class HandoffResult:
    root: Path
    original_count: int
    image_count: int
    digest: str


class HandoffError(ValueError):
    """Raised when a safe material handoff cannot be created."""


def _require_regular_file(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file():
        raise HandoffError(f"{label} is missing or is not a regular file: {path}")


def _reject_symlink(path: Path, label: str) -> None:
    current = path.absolute()
    for candidate in (current, *current.parents):
        if candidate.is_symlink():
            raise HandoffError(f"{label} must not use a symlink: {path}")


def _read_nonempty_utf8(path: Path, label: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise HandoffError(f"{label} must be UTF-8 Markdown: {path}") from exc
    if not text.strip():
        raise HandoffError(f"{label} must not be empty: {path}")
    return text


def _validate_brief(brief: str) -> None:
    missing_headings = [
        heading
        for heading in ("## Central Message", "## Delivery")
        if heading not in brief
    ]
    if missing_headings:
        raise HandoffError("brief is missing required headings: " + ", ".join(missing_headings))
    if "Include speaker notes" not in brief or "No animations, transitions, audio, or video" not in brief:
        raise HandoffError(
            "brief must require speaker notes and disable motion, transitions, audio, and video"
        )


def _validate_unique_basenames(paths: Sequence[Path], label: str) -> None:
    seen: set[str] = set()
    for path in paths:
        if path.name in seen:
            raise HandoffError(f"duplicate {label} destination basename: {path.name}")
        seen.add(path.name)


def _asset_block(brief: str, basename: str) -> str | None:
    marker = f"`{basename}`"
    lines = brief.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^\s*[-*+]\s+", line) and marker in line:
            indent = len(line) - len(line.lstrip())
            block = [line]
            for following in lines[index + 1 :]:
                if re.match(r"^\s*[-*+]\s+", following):
                    following_indent = len(following) - len(following.lstrip())
                    if following_indent <= indent:
                        break
                block.append(following)
            return "\n".join(block)
    return None


def _validate_documented_images(brief: str, images: Sequence[Path]) -> None:
    for image in images:
        block = _asset_block(brief, image.name)
        has_source = bool(block and re.search(r"(?mi)^\s*[-*+]?\s*Source:\s*\S.+$", block))
        has_preserve = bool(block and re.search(r"(?mi)^\s*[-*+]?\s*Preserve:\s*\S.+$", block))
        if not has_source or not has_preserve:
            raise HandoffError(
                f"image {image.name} must be documented in backticks with non-empty Source and Preserve fields"
            )


def _digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_material_handoff(
    brief_path: Path,
    paper_markdown: Path,
    originals: Sequence[Path],
    images: Sequence[Path],
    output_dir: Path,
) -> HandoffResult:
    """Validate and atomically create one immutable material handoff."""
    brief_path = Path(brief_path)
    paper_markdown = Path(paper_markdown)
    originals = tuple(Path(path) for path in originals)
    images = tuple(Path(path) for path in images)
    output_dir = Path(output_dir).absolute()

    _require_regular_file(brief_path, "brief")
    _require_regular_file(paper_markdown, "paper Markdown")
    for path in originals:
        _require_regular_file(path, "original")
    for path in images:
        _require_regular_file(path, "image")

    _reject_symlink(brief_path, "brief")
    _reject_symlink(paper_markdown, "paper Markdown")
    for path in originals:
        _reject_symlink(path, "original")
    for path in images:
        _reject_symlink(path, "image")

    brief = _read_nonempty_utf8(brief_path, "brief")
    _read_nonempty_utf8(paper_markdown, "paper Markdown")
    _validate_brief(brief)
    if not originals:
        raise HandoffError("at least one original source file is required")
    _validate_unique_basenames(originals, "original")
    _validate_unique_basenames(images, "image")
    _validate_documented_images(brief, images)

    if output_dir.is_symlink():
        raise HandoffError(f"destination must not be a symlink: {output_dir}")
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise HandoffError("destination is non-empty")
    if not output_dir.parent.exists() or not output_dir.parent.is_dir():
        raise HandoffError(f"destination parent does not exist: {output_dir.parent}")

    staging = Path(mkdtemp(prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent))
    try:
        shutil.copyfile(brief_path, staging / "brief.md")
        shutil.copyfile(paper_markdown, staging / "paper.md")
        original_dir = staging / "original"
        original_dir.mkdir()
        for source in originals:
            shutil.copyfile(source, original_dir / source.name)
        if images:
            image_dir = staging / "images"
            image_dir.mkdir()
            for source in images:
                shutil.copyfile(source, image_dir / source.name)
        digest = _digest_tree(staging)

        if output_dir.exists():
            output_dir.rmdir()
        os.replace(staging, output_dir)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return HandoffResult(
        root=output_dir,
        original_count=len(originals),
        image_count=len(images),
        digest=digest,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, type=Path)
    parser.add_argument("--paper-md", required=True, type=Path)
    parser.add_argument("--original", required=True, action="append", type=Path)
    parser.add_argument("--image", action="append", default=[], type=Path)
    parser.add_argument("output_dir", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = build_material_handoff(
            args.brief,
            args.paper_md,
            args.original,
            args.image,
            args.output_dir,
        )
    except HandoffError as exc:
        print(json.dumps({"status": "rejected", "message": str(exc)}, separators=(",", ":")))
        return 2
    print(
        json.dumps(
            {
                "status": "created",
                "root": str(result.root),
                "original_count": result.original_count,
                "image_count": result.image_count,
                "digest": result.digest,
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
