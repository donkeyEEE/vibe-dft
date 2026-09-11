#!/usr/bin/env python3
"""Plot VAMPIRE output:temperature and output:mean-magnetisation-length."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


TEMPERATURE_NAMES = {"temperature", "output:temperature"}
MAGNETISATION_NAMES = {
    "mean-magnetisation-length",
    "output:mean-magnetisation-length",
}


def normalise(token: str) -> str:
    return token.strip().lstrip("#").lower()


def read_series(path: Path) -> tuple[np.ndarray, np.ndarray]:
    temperature_column: int | None = None
    magnetisation_column: int | None = None
    temperatures: list[float] = []
    magnetisations: list[float] = []

    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        fields = raw_line.split()
        names = [normalise(field) for field in fields]
        if any(name in TEMPERATURE_NAMES for name in names) and any(
            name in MAGNETISATION_NAMES for name in names
        ):
            temperature_column = next(index for index, name in enumerate(names) if name in TEMPERATURE_NAMES)
            magnetisation_column = next(index for index, name in enumerate(names) if name in MAGNETISATION_NAMES)
            continue
        if temperature_column is None or magnetisation_column is None:
            continue
        required_columns = max(temperature_column, magnetisation_column)
        if len(fields) <= required_columns:
            continue
        try:
            temperatures.append(float(fields[temperature_column]))
            magnetisations.append(float(fields[magnetisation_column]))
        except ValueError:
            continue

    if temperature_column is None or magnetisation_column is None:
        raise ValueError("missing output:temperature or output:mean-magnetisation-length header")
    if not temperatures:
        raise ValueError("no numeric VAMPIRE temperature/magnetisation samples found")
    return np.array(temperatures), np.array(magnetisations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="output")
    parser.add_argument("--output", default="M_vs_T.png")
    args = parser.parse_args()

    temperatures, magnetisations = read_series(Path(args.input))
    plt.figure()
    plt.plot(temperatures, magnetisations, marker="o")
    plt.xlabel("Temperature (K)")
    plt.ylabel("<|m|> (average magnetisation length)")
    plt.title("Magnetisation vs Temperature")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.output, dpi=300)
    print(f"{args.output} generated from {args.input}")


if __name__ == "__main__":
    main()
