# Exchange-parameter energy-mapping design

Use this reference when a Spec derives exchange parameters by energy mapping.
It records the assumptions and fit diagnostics required for the scientific
judgment; it does not choose a Hamiltonian, cutoff, configuration subset, or
physical acceptance criterion.

## Evidence and approval inputs

Read the accepted RQ decisions, approved structures and magnetic
configurations, relevant computed or planned energies, symmetry/equivalence
evidence, and prior model evidence. Obtain approval for the Hamiltonian and
fitted unknowns, simulation cell, configuration set, reference-energy
convention, interaction cutoff, bond-equivalence assumptions, and the rank,
coverage, residual, and physical criteria that will decide acceptance.

## Required design and acceptance record

- State the Hamiltonian and fitted unknowns, simulation cell, magnetic
  configurations, and reference-energy convention.
- State the periodic bond-counting method, including its no-double-counting
  convention.
- Require the design matrix, matrix rank, duplicate rows, configuration
  coverage, and number of independent equations relative to fitted unknowns.
- Require the fit residual or RMSE, units, and the evidence used to judge it.

Duplicate rows and rank deficiency are reported rather than counted as added
constraints. A zero-RMSE exactly determined subset does not by itself establish
reliable exchange parameters, and selecting a subset to obtain a desired fitted
sign is not valid validation. Numerical signs or a small residual alone do not
establish a magnetic ground state. Interface bond equivalence, model, cutoffs,
and physical interpretation remain explicit approved modelling choices.
