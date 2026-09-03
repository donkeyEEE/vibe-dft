# Spin-resolved Wannier-window selection

Use this reference before selecting or reviewing final spin-resolved Wannier90
outer and frozen windows. A VASP-to-Wannier pre-run may supply a broad outer
window, but it does not determine the final physical subspace.

## Required task record

For each spin channel, record:

- outer and frozen window bounds and their selection evidence, such as
  bandrange;
- `NUM_WANN`, the maximum frozen-state count per k point, and the projection
  set;
- WOUT diagnostics and spin-resolved VASP-versus-Wannier fit plots;
- superseded window attempts and the reason they were replaced.

Flag a frozen window that contains more states at any k point than `NUM_WANN`.
Do not silently shrink, expand, or share a window between spin channels.

## Interpretation boundary

Bandrange does not replace inspection of projections, WOUT diagnostics, and
fit plots. A successful Wannier90 run, or a broad pre-run window alone, does
not prove that the selected subspace is physically adequate. The user confirms
the target subspace, projections, and final windows.
