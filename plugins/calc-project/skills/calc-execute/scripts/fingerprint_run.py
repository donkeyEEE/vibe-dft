#!/usr/bin/env python3
"""Fingerprint every regular file in one Run's inputs directory."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path


def _files_below(inputs: Path) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    try:
        for directory, dirnames, filenames in os.walk(
            inputs, followlinks=False, onerror=raise_walk_error
        ):
            root = Path(directory)
            for name in dirnames:
                candidate = root / name
                if candidate.is_symlink():
                    raise ValueError(f"symbolic link in inputs: {candidate.relative_to(inputs)}")
            for name in filenames:
                candidate = root / name
                relative = candidate.relative_to(inputs).as_posix()
                if candidate.is_symlink():
                    raise ValueError(f"symbolic link in inputs: {relative}")
                if not candidate.is_file():
                    raise ValueError(f"non-regular file in inputs: {relative}")
                files.append((relative, candidate))
    except OSError as error:
        raise ValueError(f"cannot inspect inputs: {error}") from error
    return sorted(files, key=lambda item: item[0])


def _file_digest(path: Path) -> bytes:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise ValueError(f"cannot read input file {path}: {error}") from error
    return digest.digest()


def fingerprint_inputs(inputs: Path) -> str:
    """Return a deterministic digest of all relative file names and bytes."""
    inputs = Path(inputs)
    if inputs.is_symlink() or not inputs.is_dir():
        raise ValueError(f"inputs directory does not exist or is a link: {inputs}")

    snapshot = hashlib.sha256()
    for relative, path in _files_below(inputs):
        relative_bytes = os.fsencode(relative)
        snapshot.update(len(relative_bytes).to_bytes(8, "big"))
        snapshot.update(relative_bytes)
        snapshot.update(_file_digest(path))
    return snapshot.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs_dir", type=Path)
    args = parser.parse_args()
    try:
        print(fingerprint_inputs(args.inputs_dir))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
