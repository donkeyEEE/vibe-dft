# VASP scientific design

Use this reference when a Spec makes VASP physical commitments. It defines the
information the design must settle; it does not prepare inputs or select values
from a template.

## Design evidence

Read the accepted RQ decisions, material-specific calculation records, approved
structure and species order, relevant prior Runs, and available VASP
capabilities. Set the calculation type and material-specific parameters from
the accepted RQ and verified evidence. A generic or project
template is a baseline only and is not evidence that its values are physically
valid for this Spec.

## Commitments to record

- Identify relaxation, SCF, non-self-consistent bands, SOC, DFT+U, or VASP
  Wannier pre-run scope, including the role of each task in the DAG.
- Record the selected `ENCUT`, k-point density, `ISPIN`/`MAGMOM`, smearing, and
  any `LORBIT`, `LWAVE`, or `LCHARG` value whose presence changes the intended
  observable or a declared downstream handoff. Otherwise these output controls
  are execution-owned and `$calc-execute` derives them from the task's named
  products and downstream needs.
- For SOC, record the selected non-collinear executable and `LSORBIT`, `SAXIS`,
  and symmetry commitments.
- For DFT+U, bind every species-indexed array to the selected POSCAR/POTCAR
  species order.
- State acceptance as the minimum result and necessary handoff evidence that
  answer the task Purpose. Add convergence or quality thresholds only when the
  principal judgment depends on them. Preserve the selected material-specific
  source and any scientifically material deviation.

Research missing or conflicting physical settings; interview only when a
critical scientific choice remains unresolved. Do not infer values from a
generic baseline or broaden the RQ into a new parameter study.
