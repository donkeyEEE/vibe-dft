# VASP scientific design

Use this reference when a Spec makes VASP physical commitments. It defines the
information the design must settle; it does not prepare inputs or select values
from a template.

## Evidence and approval inputs

Read the accepted RQ decisions, material-specific calculation records, approved
structure and species order, relevant prior Runs, and available VASP
capabilities. Obtain approval for the calculation type and every
material-specific parameter that affects the judgment. A generic or project
template is a baseline only and is not evidence that its values are physically
valid for this Spec.

## Commitments to record

- Identify relaxation, SCF, non-self-consistent bands, SOC, DFT+U, or VASP
  Wannier pre-run scope, including the role of each task in the DAG.
- Record the approved `ENCUT`, k-point density, `ISPIN`/`MAGMOM`, smearing,
  `LORBIT`, and output controls `LWAVE` and `LCHARG` that the task requires.
- For SOC, record the approved non-collinear executable and `LSORBIT`, `SAXIS`,
  and symmetry commitments.
- For DFT+U, bind every species-indexed array to the approved POSCAR/POTCAR
  species order.
- State acceptance and stopping criteria in terms of the intended scientific
  result and necessary handoff evidence. Record every intentional deviation
  from the approved material-specific source.

Missing or conflicting physical settings remain an open design decision. Do
not infer them from a generic baseline or broaden a completed RQ into a new
parameter study.
