# VASP Read-only Checks

Compare the exact prepared files with the current Spec's calculation type and
approved evidence. Check nonempty `INCAR`, `POSCAR`, `KPOINTS`, `POTCAR`,
`cluster-env.sh`, and `run.pbs`; POSCAR/POTCAR species order; species-indexed
DFT+U and magnetic arrays; `ENCUT`, k-point definition, smearing,
`ISPIN`/`MAGMOM`, `LORBIT`, `LWAVE`, and `LCHARG`; and the selected executable.
For SOC, also check `LSORBIT`, `SAXIS`, symmetry, spinor `NBANDS`, and the
approved non-collinear executable.

Require preparation-time POTCAR/KPOINTS mechanics, stage-specific VASPKIT
working directory and menu route, named upstream current-Run handoffs, and all
expected products to agree with the task. For band and Wannier pre-run stages,
inspect the exact server-side `CHGCAR`/`WAVECAR` source and immutable prepared
handoff. For directional MAE, require a comparable approved pair, the same
named SCF charge source, and the Spec's energy convention. A missing choice or
change in physical commitment is `block` owned by `$calc-to-spec`; a prepared
file or handoff defect is `block` owned by `$calc-execute`.
