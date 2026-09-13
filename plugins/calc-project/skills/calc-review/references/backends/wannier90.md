# Wannier90 Read-only Checks

For each spin, compare the prepared projections, `NUM_WANN`, outer window,
frozen window, and their evidence with the current Spec. Require distinct
approved spin values; never silently share, shrink, or expand a window. Count
frozen states at every k point. A count exceeding `NUM_WANN` requires a change
to the scientific subspace or window.

Inspect the exact accepted `.amn`, `.mmn`, `.eig`, and `.win` sources, both
spin-range files, reformatted spin bands, DOSCAR, rendered environment and
window inputs, expected WOUT/HR/centres products, and planned fit plots.
Bandrange or a broad pre-run window does not establish an adequate physical
subspace. Distinguish a scientifically missing or changed subspace/window from
a snapshot or handoff defect.
