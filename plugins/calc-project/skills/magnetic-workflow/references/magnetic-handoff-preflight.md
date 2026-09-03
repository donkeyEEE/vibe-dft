# Magnetic handoff preflight

Use this review before handing a layered magnetic VASP task to a downstream
SCF follow-up, Wannier90, TB2J, or VAMPIRE stage. It is a human check, not an
automatic magnetic-order assignment.

## Required review

1. From the task-local structure, identify the magnetic atoms and record their
   atom index, species, and fractional z coordinate.
2. Sort only those magnetic atoms by fractional z and assign their z-sorted
   layer rank.
3. From the task-local INCAR, record the `MAGMOM` value assigned to each
   magnetic-atom index.
4. Ask the user to supply or confirm the intended layer-moment sequence.
5. Compare the index-order `MAGMOM` assignment against that intended sequence.
   Record the table and the user's confirmation in the handoff task's
   `README.md`; `calc-task.yaml` remains the task fact source.

| atom index | species | fractional z | z-sorted layer rank | assigned `MAGMOM` | intended layer moment |
|---|---|---:|---:|---:|---|
| `<index>` | `<species>` | `<z>` | `<rank>` | `<value>` | `<user-confirmed moment>` |

## Limits

No fixed sign pattern transfers between structures: atom numbering need not
follow the geometric layer order. A near-zero total moment, a completed VASP
run, or converged downstream TB2J output does not validate the intended layer
sequence. This preflight presents structural and input evidence only; magnetic
order remains a user-confirmed physical choice.
