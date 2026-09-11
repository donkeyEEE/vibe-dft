# Spin-resolved Wannier90 window design

Use this reference before a Spec selects final spin-resolved Wannier90 outer and
frozen windows. A VASP-to-Wannier pre-run may provide broad evidence, but it
does not determine the final physical subspace.

## Evidence and approval inputs

Read the accepted RQ decisions and, for each spin channel, bandrange or
equivalent band evidence, projection character, `NUM_WANN`, frozen-state counts
per k point, WOUT diagnostics, and VASP-versus-Wannier fit evidence. Obtain
approval for the target subspace, projections, separate outer and frozen window
bounds, fit criteria, and stopping rule for each spin channel.

## Commitments and acceptance

For each spin channel, the Spec records:

- outer and frozen window bounds and the evidence used to select them;
- `NUM_WANN`, the maximum frozen-state count per k point, and the projection
  set;
- the WOUT diagnostics and spin-resolved VASP-versus-Wannier fit evidence that
  decide acceptance.

A frozen window containing more states at any k point than `NUM_WANN` is not an
acceptable design. Do not silently shrink, expand, or share a window between
spin channels. Bandrange does not replace inspection of projections, WOUT
diagnostics, and fit evidence; a successful Wannier90 Run or broad pre-run
window alone does not establish physical adequacy. Replaced attempts remain
preserved Runs rather than a Spec revision-history section.
