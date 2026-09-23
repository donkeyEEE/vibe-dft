# Magnetic pipeline scientific design

Use this reference when one principal judgment needs a VASP → Wannier90 → TB2J
→ VAMPIRE task graph. This is a candidate scientific DAG, not a fixed directory
layout or mandatory pipeline.

## Design evidence

Read the accepted RQ decisions, approved structure provenance, relevant prior
Runs, and method capability records. For magnets whose intended order depends
on atom identity or ordering, establish an unambiguous mapping between structure
atoms, index-order `MAGMOM`, and the intended site or layer moments. Choose any
unambiguous evidence form; a compact grouping, deterministic check, or per-atom
table may be used according to risk. Research an unresolved mapping and
interview only if its physical meaning remains indeterminate. Set only the
tasks actually needed, their dependencies and conditions, material settings,
Wannier subspaces, TB2J model choices, and the VAMPIRE observable and stopping
criterion from the accepted RQ and evidence.

## Candidate DAG and evidence

When required by the judgment, declare separate tasks for:

1. VASP SCF, accepted by the stated criterion needed for its Purpose and preserving the
   original `OUTCAR` final `E-fermi` needed downstream.
2. SCF-derived VASP bands, accepted with the approved spin-resolved band
   evidence and required handoff products.
3. The VASP-to-Wannier pre-run, accepted with spin-resolved `.amn`, `.mmn`,
   `.eig`, and generated `.win` interface files.
4. Spin-resolved Wannier90, accepted with two nonempty `*_hr.dat`,
   `*_centres.xyz`, band data, and fit evidence needed for the judgment.
5. TB2J, accepted with the chosen spin assets, `exchange.out`, and the model
   handoff required for VAMPIRE.
6. VAMPIRE, accepted by the stated observable and stopping criterion, with
   evidence tied to the immutable TB2J-generated source model.

Record the structure, magnetic atoms/orbitals, Fermi convention, spin
representation, `wann2J.py` arguments, and selected TB2J k mesh. Wannier
`mp_grid` does not determine the TB2J mesh. Require sensitivity evidence only
when the judgment depends on its robustness or the strict level calls for it.
Load the separate Wannier90 design reference when selecting final
per-spin windows.

## Magnetic-order boundary

Record enough reproducible evidence to recover the approved correspondence; do
not impose a fixed table when a simpler representation is unambiguous. No fixed
sign pattern transfers between structures because atom numbering need
not follow geometric layer order. A near-zero total moment, completed VASP Run,
or converged downstream TB2J result does not validate the intended layer
sequence. When the physical meaning is not already determined, no stage template
or historical case supplies a default.
