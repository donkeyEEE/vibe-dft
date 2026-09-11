# Wannier90 Read-only Checks

For each spin, compare the prepared projections, `NUM_WANN`, outer window,
frozen window, and their evidence with the current Spec. Require distinct
approved spin values; never silently share, shrink, or expand a window. Count
frozen states at every k point and block when the count exceeds `NUM_WANN`.

Inspect the exact accepted `.amn`, `.mmn`, `.eig`, and `.win` sources, both
spin-range files, reformatted spin bands, DOSCAR, rendered environment and
window inputs, expected WOUT/HR/centres products, and planned fit plots.
Bandrange or a broad pre-run window does not establish an adequate physical
subspace. A missing or changed subspace/window is `block` owned by
`$calc-to-spec`; a snapshot or handoff mismatch is `block` owned by
`$calc-execute`.
