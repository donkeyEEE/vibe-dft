# VAMPIRE Read-only Checks

Require an exact, named TB2J current-Run source for `vampire.UCF`,
`vampire.mat`, and `input`. Compare closed source checksums with the immutable
prepared copies. The prepared model must preserve TB2J settings; the only
allowed input change is replacing `output:material-magnetisation` with both
`output:temperature` and `output:mean-magnetisation-length`. Any other model
or setting change is `block`.

Inspect the rendered environment, VAMPIRE command, exact named output columns,
plot-helper input, expected `M_vs_T.png`, and lightweight packaging plan. The
plan must exclude model files, Wannier Hamiltonians, HDF5, `WAVECAR`, `CHGCAR`,
`CHG`, and `vasprun.xml`. A source or prepared-copy defect is `block` owned by
`$calc-execute`; a requested physical-model change belongs to `$calc-to-spec`.
