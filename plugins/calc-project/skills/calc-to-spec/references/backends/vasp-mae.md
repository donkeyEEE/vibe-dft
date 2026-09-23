# Directional SOC-MAE scientific design

Use this reference for a magnetocrystalline anisotropy energy
(MAE) judgment based on directional static SOC calculations. It defines a
comparable pair; it does not generate inputs or choose material settings.

## Design evidence

Read the accepted RQ decisions, source SCF and charge-density provenance,
chemical cells and lattice constants, and material-specific VASP settings.
Set the compared directions, `MAGMOM`, cutoff, k mesh, Hubbard parameters,
electronic convergence settings, spinor `NBANDS`, and reported energy-difference
convention from the accepted question and evidence. Add directions or angular
scans only when the judgment requires them or the strict level explicitly asks.

## Comparable-pair commitments

1. Both directional tasks use the same selected SCF charge density with
   `ISTART=0` and `ICHARG=11`.
2. Both use `LSORBIT=.TRUE.`, `ISYM=-1`, and the selected spinor `NBANDS`.
3. With `LSORBIT=.TRUE.`, `MAGMOM` has three components for every ion in the
   spinor-space basis defined by `SAXIS`. With the default `SAXIS`, that is the
   Cartesian basis. Retain all three components even for collinear initial
   moments.
4. The paired physical inputs are identical except for the selected `SAXIS`
   direction.
5. The Spec states the energy convention explicitly, for example
   `MAE = E[100] - E[001]`, and requires the result and units under that same
   convention.

Unequal chemical cells or lattice constants do not by themselves establish a
pure interface effect. The acceptance rule must preserve and compare the source
task and both directional inputs. Research unresolved choices and interview
only if the principal judgment remains indeterminate.
