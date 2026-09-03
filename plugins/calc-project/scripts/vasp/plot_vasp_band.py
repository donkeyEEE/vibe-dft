"""Plot blank-separated VASPKIT BAND.dat blocks without project-specific settings."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def read_band_blocks(path: Path) -> list[np.ndarray]:
    """Read k-distance/energy blocks separated by blank lines from ``path``."""
    blocks: list[np.ndarray] = []
    current: list[tuple[float, float]] = []
    for raw_line in path.read_text().splitlines():
        fields = raw_line.split()
        if not fields:
            if current:
                blocks.append(np.asarray(current))
                current = []
            continue
        if raw_line.lstrip().startswith("#"):
            continue
        try:
            current.append((float(fields[0]), float(fields[1])))
        except (IndexError, ValueError) as error:
            raise ValueError(f"Expected k-distance and energy in {path}: {raw_line}") from error
    if current:
        blocks.append(np.asarray(current))
    if not blocks:
        raise ValueError(f"No band blocks found in {path}")
    return blocks


def plot_band_blocks(blocks: list[np.ndarray], output: Path, energy_window: tuple[float, float] | None = None) -> None:
    """Plot band blocks relative to the Fermi energy assumed in the input data."""
    figure, axis = plt.subplots(figsize=(6, 6), dpi=300)
    for block in blocks:
        axis.plot(block[:, 0], block[:, 1], color="black", linewidth=0.7)
    axis.axhline(0.0, color="tab:red", linestyle="--", linewidth=0.7)
    axis.set(xlabel="k-path distance", ylabel=r"Energy - $E_F$ (eV)")
    axis.set_xticks([])
    if energy_window is not None:
        axis.set_ylim(*energy_window)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output)
    plt.close(figure)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("BAND.dat"))
    parser.add_argument("--output", type=Path, default=Path("band.png"))
    parser.add_argument("--emin", type=float)
    parser.add_argument("--emax", type=float)
    args = parser.parse_args(argv)
    if (args.emin is None) != (args.emax is None):
        parser.error("--emin and --emax must be supplied together")
    window = None if args.emin is None else (args.emin, args.emax)
    plot_band_blocks(read_band_blocks(args.input), args.output, window)


if __name__ == "__main__":
    main()
