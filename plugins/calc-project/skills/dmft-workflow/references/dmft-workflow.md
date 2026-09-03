# DMFT Workflow Reference

## Project Authority

Before modifying an FGET/FGAT DMFT workflow, read the current stage plan plus the project documents for DMFT parameters, PLO/local orbitals, and known self-energy or convergence failures. They define the approved projection window, orbital order, U/J, double counting, solver settings, and PM versus magnetic interpretation.

## Postprocessing

Use `calculation_templates/dmft-postprocessing/`:

- `impurity_spectral_function/` for impurity Green's-function MaxEnt continuation and spectral-function plots.
- `self_energy/maxent/` for self-energy MaxEnt continuation and plots.
- `self_energy/pade/` for self-energy Pade continuation and plots.

Run the chosen script from its postprocessing subdirectory so its relative `../vasp.h5` convention remains valid. Do not commit or synchronize the HDF5 input or copies.

## PBS and Outputs

Apply `../calc-workflows/references/pbs.md`: no `set -euo pipefail`, explicit prerequisite checks, and a default walltime of 144 hours. Keep run scripts and result packaging separate, and inspect long logs only with targeted commands.
