#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_fermi_energy(doscar="DOSCAR"):
    with open(doscar, "r", encoding="utf-8") as handle:
        lines = handle.readlines()
    return float(lines[5].split()[3])


def read_wannier_band(file_name, fermi_energy):
    with open(file_name, "r", encoding="utf-8") as handle:
        blocks = handle.read().split("\n  \n")[:-1]
    bands = []
    kpoints = np.array([float(line.split()[0]) for line in blocks[0].splitlines()])
    for block in blocks:
        band = np.array([float(line.split()[1]) - fermi_energy for line in block.splitlines()])
        bands.append(band)
    return kpoints, bands


def read_vest_band(file_name):
    rows = []
    for line in open(file_name, encoding="utf-8"):
        fields = line.split()
        try:
            row = [float(value) for value in fields]
        except ValueError:
            continue
        if len(row) >= 2:
            rows.append(row)
    if not rows:
        raise ValueError(f"no numeric VEST band rows found in {file_name}")
    width = len(rows[0])
    rows = [row for row in rows if len(row) == width]
    data = np.array(rows, dtype=float)
    return [np.column_stack((data[:, 0], data[:, index])) for index in range(1, data.shape[1])]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--emin", type=float, required=True)
    parser.add_argument("--emax", type=float, required=True)
    parser.add_argument("--doscar", default="DOSCAR")
    parser.add_argument("--vest-band", default="bandstructure_down.dat")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.emin >= args.emax:
        raise SystemExit("--emin must be smaller than --emax")

    fermi_energy = read_fermi_energy(args.doscar)
    wannier_band_file = "wannier90.2_band.dat"

    plt.figure(figsize=(4, 6))
    wannier_k, wannier_bands = read_wannier_band(wannier_band_file, fermi_energy)
    for index, band in enumerate(wannier_bands):
        plt.plot(wannier_k, band, color="blue", linewidth=1,
                 label="Wannier90" if index == 0 else None)

    for index, band in enumerate(read_vest_band(args.vest_band)):
        plt.plot(band[:, 0], band[:, 1], linestyle="--", color="red", linewidth=1,
                 label="VASP (VEST)" if index == 0 else None)

    plt.ylim(args.emin, args.emax)
    plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
    plt.xlabel("k-point")
    plt.ylabel("Energy (eV)")
    plt.title("Wannier fit: spin down")
    plt.legend(loc="best")
    plt.grid()
    plt.tight_layout()
    plt.savefig(args.output, format="png", dpi=300)
    plt.close()
