# Magnetic VASP Read-only Checks

From the exact prepared POSCAR and INCAR, establish an unambiguous mapping when
magnetic meaning depends on atom identity or ordering. Compare the index-order
`MAGMOM` assignment with the intended site or layer moments in the approved
Spec. A per-atom table is optional; use a compact grouping, deterministic check,
table, or other reproducible evidence suited to the structure. For a uniform,
single-sublattice assignment with unchanged ordering, verifying array length,
grouping, and values is sufficient. Do not assign or infer a magnetic order.

Distinguish inability to establish the mapping because the intended order is
scientifically underdetermined from a rendering or ordering defect with an
already approved meaning. A near-zero total moment, completed VASP job, or
downstream convergence does not establish the intended order.
