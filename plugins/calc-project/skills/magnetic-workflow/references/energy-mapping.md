# Energy mapping method record

Use this reference when a user requests exchange-parameter energy mapping. It
records the assumptions and fit diagnostics required to interpret a result; it
does not choose a Hamiltonian, cutoff, configuration subset, or physical
acceptance criterion.

## Required task record

Record the following in the task README or analysis record:

- Hamiltonian and fitted unknowns, simulation cell, magnetic configurations,
  and reference-energy convention.
- Periodic bond-counting method, including the no-double-counting convention.
- Design matrix, matrix rank, duplicate rows, configuration coverage, and the
  number of independent equations relative to fitted unknowns.
- Fit residual or RMSE, units, and the evidence used to judge the fit.

## Interpretation boundary

Report duplicate rows and rank deficiency rather than treating them as added
constraints. A zero-RMSE, exactly determined subset does not by itself establish
reliable exchange parameters, and selecting a subset for a desired fitted sign
is not valid validation. Numerical fitted signs or a small residual alone do
not establish a magnetic ground state. Interface bond equivalence, the model,
cutoffs, and physical interpretation remain explicit user-confirmed modelling
choices.
