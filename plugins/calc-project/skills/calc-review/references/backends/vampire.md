# VAMPIRE Read-only Checks

Require an exact, named TB2J current-Run source for `vampire.UCF`,
`vampire.mat`, and `input`. Compare closed source checksums with the immutable
prepared copies. The prepared model must preserve the Spec-approved TB2J
settings. Compare postprocessing-only edits with the changes approved by the
Spec instead of treating one historical edit pattern as universal. Distinguish
an unapproved physical-model change from a mechanical rendering difference.

Inspect the rendered environment, VAMPIRE command, exact named output columns,
plot-helper input, expected `M_vs_T.png`, and lightweight packaging plan. The
plan must exclude model files, Wannier Hamiltonians, HDF5, `WAVECAR`, `CHGCAR`,
`CHG`, and `vasprun.xml`. Report any source, prepared-copy, packaging, or
physical-model discrepancy precisely.
