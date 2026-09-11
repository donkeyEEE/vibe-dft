# TB2J Read-only Checks

Compare the prepared structure, magnetic atoms and orbitals, spin
representation, `wann2J.py` arguments, and separately approved TB2J k mesh with
the current Spec. Require the named current SCF OUTCAR as the Fermi-level
source and the exact accepted spin-resolved Wannier Hamiltonian and centres
files. A Wannier `mp_grid` does not authorize the TB2J mesh.

Require the rendered environment, command, expected `exchange.out`, and named
`TB2J_results/Vampire/vampire.*` products. A missing scientific selection is
`block` owned by `$calc-to-spec`; a stale source, copied input, environment, or
product-contract mismatch is `block` owned by `$calc-execute`.
