# DMFT postprocessing execution

Load this reference in addition to `common.md` only when the approved Spec
declares DMFT postprocessing. The Spec must name the method, exact source,
inputs, lightweight products, and decisive criteria before this branch prepares
`inputs/run.pbs`.

## Select the declared operation

Use only the matching project-approved source below:

- `calculation_templates/dmft-postprocessing/impurity_spectral_function/` for
  impurity spectral function MaxEnt continuation and its plots;
- `calculation_templates/dmft-postprocessing/self_energy/maxent/` for
  self-energy MaxEnt continuation and its plots;
- `calculation_templates/dmft-postprocessing/self_energy/pade/` for
  self-energy Pade continuation and its plots;
- the Spec-named approved convergence plotting source for already-synchronized
  lightweight convergence tables.

A missing source, undecided method, or changed analytic-continuation choice is a
design stop for `$calc-to-spec`, not permission to substitute a neighboring
directory or infer parameters.

## Prepare and run

Render the common `inputs/run.sh` as directed by `common.md`. Its preparation
body copies every named script/config with
`copy_immutable SOURCE DESTINATION || return 1`, and every validation command
ends in `|| return 1`. Render the concrete `inputs/run.pbs` from the selected
approved source instructions; no DMFT postprocessing PBS template is universal.

Impurity and self-energy continuation run only on the server. Prepare the exact
approved HDF5 handoff there before review, keep its expected relative
`../vasp.h5` relationship to the selected postprocessing subdirectory, and run
the chosen script from that subdirectory. The HDF5 source and Run-local handoff
never enter the local project, Git, a synchronization plan, or a result package.
The concrete PBS script refuses nonempty `outputs/`, works in its private
Run-local output tree, and checks each Spec-named lightweight product before it
succeeds.

Convergence plotting may instead consume only the exact already-synchronized
lightweight `conv_imp<N>.dat` and `observables_imp<N>.dat` files named by the
Spec. It never reads HDF5 locally. Package only declared PNG/SVG plots and text
summaries; keep scripts, full logs, and large solver data out of the result
package.

Compare the resulting lightweight evidence with the approved Spec's decisive
criteria. Ambiguous or conflicting convergence evidence returns to
`$calc-to-spec`; execution neither invents a threshold nor claims convergence
from the presence of a plot.
