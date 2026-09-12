# VASP SCF execution knowledge

Load with `common.md` only while preparing or assessing the SCF task.

- Require `INCAR`, `POSCAR`, `POTCAR`, and a mesh `KPOINTS` in task inputs.
- Confirm `ENCUT`, k-point density, `ISPIN`/`MAGMOM`, smearing, `LORBIT`,
  `LWAVE`, and `LCHARG` against the task declaration.
- The Run is acceptable only after scheduler completion and synchronization
  show non-empty `OUTCAR` and `CHGCAR` under the exact Run.
- Only an accepted current SCF Run may supply the band dependency.
