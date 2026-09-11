# VASP band execution knowledge

Load with `common.md` and `handoff.md` only while preparing or assessing the
non-self-consistent band task.

- Require `INCAR`, `POSCAR`, `POTCAR`, and line-mode/path `KPOINTS`.
- Compare the band INCAR with the accepted SCF INCAR; permit only declared
  stage differences such as `ICHARG=11` and output-control changes.
- Preserve prepared path KPOINTS; VASPKIT task 103 may create POTCAR but must
  not replace KPOINTS.
- The Run is acceptable only after scheduler completion and synchronization
  show non-empty `OUTCAR` and `BAND.dat` under the exact Run.
