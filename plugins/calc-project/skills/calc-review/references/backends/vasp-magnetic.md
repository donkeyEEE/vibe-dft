# Magnetic VASP Read-only Checks

From the exact prepared POSCAR and INCAR, list each magnetic atom's index,
species, fractional z coordinate, z-sorted layer rank, and assigned `MAGMOM`.
Compare the index-order assignments with the intended layer-moment sequence in
the current approved Spec. Do not assign or infer a magnetic order.

A mismatch, missing approved sequence, or changed atom order is `block` owned
by `$calc-to-spec`; a rendering mismatch against an approved sequence is
`block` owned by `$calc-execute`. A near-zero total moment, completed VASP job,
or downstream convergence does not establish the intended layer sequence.
