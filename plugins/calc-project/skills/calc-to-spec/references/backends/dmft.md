# DFT+DMFT scientific design

Use this reference when a Spec commits to a solid_dmft/DFT+DMFT calculation or
interpretation. It owns design choices and decisive criteria, not Run
preparation or postprocessing mechanics.

## Evidence and approval inputs

Read the accepted RQ decisions, current scientific stage plan, project DMFT
parameter records, PLO/local-orbital records, relevant prior Runs, and known
self-energy or convergence failures. Obtain approval for PM/no-spin versus
magnetic/spin scope, one-shot versus charge-self-consistent scope, the
correlated subspace, PLO/local-orbital basis and orbital order, projection
window, `U`/`J`, double counting, interaction convention, solver settings,
requested observables, and their acceptance and stopping criteria.

## Commitments to record

- Bind each DMFT task to the approved subspace, basis, orbital order, projection
  window, interaction, solver, and interpretation scope.
- State which convergence observables decide acceptance, such as the relevant
  DMFT iterations, impurity occupancy, double occupancy, or self-energy
  quantities, using project-approved criteria rather than an inferred
  threshold.
- Declare the lightweight postprocessing result needed for the judgment when
  impurity spectral functions, self-energy MaxEnt, self-energy Pade, or
  convergence plots are required. HDF5 handling remains an execution concern.
- Preserve explicit provenance whenever a downstream comparison depends on a
  prior calculation or postprocessing choice.

Do not claim physical comparability across different PLO/local bases, double
counting, `U`/`J`, or interaction forms without an approved rationale.
Conflicting evidence or an ambiguous convergence judgment returns to Spec
design; no generic template supplies a missing scientific value.
