# VASP Input Checklist

Use the task-specific calculation note and existing approved templates as the parameter authority. Before generating inputs, identify the calculation type: relaxation, SCF, non-self-consistent bands, SOC, DFT+U, or Wannier pre-run.

For every type, verify `ENCUT`, k-point density, `ISPIN`/`MAGMOM`, smearing, `LORBIT`, and output controls (`LWAVE`, `LCHARG`). For SOC, use the approved non-collinear executable and check `LSORBIT`, `SAXIS`, and symmetry settings. For DFT+U, keep all species-indexed arrays aligned to the POSCAR/POTCAR order.

Do not treat a generic template as physically validated input. Preserve the calculation note's material-specific settings and record every intentional deviation.
