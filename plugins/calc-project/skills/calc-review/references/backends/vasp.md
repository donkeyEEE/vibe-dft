# VASP Read-only Checks

Compare the exact prepared files with the current Spec's calculation type and
approved evidence. Check nonempty `INCAR`, `POSCAR`, `KPOINTS`, `POTCAR`,
`cluster-env.sh`, and `run.pbs`; POSCAR/POTCAR species order; species-indexed
DFT+U and magnetic arrays; `ENCUT`, k-point definition, smearing,
`ISPIN`/`MAGMOM`, `LORBIT`, `LWAVE`, and `LCHARG`; and the selected executable.
For SOC, also check `LSORBIT`, `SAXIS`, symmetry, spinor `NBANDS`, and the
approved non-collinear executable.

Establish that POTCAR/KPOINTS generation preserves the approved species and
k-point meaning; require a particular tool route only when it is scientifically
or operationally non-equivalent to alternatives. Check named upstream
current-Run handoffs and expected products. For band and Wannier pre-run stages,
inspect the exact server-side `CHGCAR`/`WAVECAR` source and immutable prepared
handoff. For directional MAE, establish a comparable approved pair, the same
named SCF charge source, and the Spec's energy convention. Distinguish a missing
scientific choice from prepared-file and handoff defects.
