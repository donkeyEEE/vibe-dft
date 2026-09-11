# Directional SOC-MAE scientific design

Use this reference for a user-approved magnetocrystalline anisotropy energy
(MAE) judgment based on directional static SOC calculations. It defines a
comparable pair; it does not generate inputs or choose material settings.

## Evidence and approval inputs

Read the accepted RQ decisions, approved source SCF and charge-density
provenance, chemical cells and lattice constants, and the material-specific
VASP settings. Obtain approval for the compared directions, `MAGMOM`, cutoff,
k mesh, Hubbard parameters, electronic convergence settings, spinor `NBANDS`,
whether additional directions or angular scans are required, and the reported
energy-difference convention and units.

## Comparable-pair commitments

1. Both directional tasks use the same approved SCF charge density with
   `ISTART=0` and `ICHARG=11`.
2. Both use `LSORBIT=.TRUE.`, `ISYM=-1`, and the approved spinor `NBANDS`.
3. With `LSORBIT=.TRUE.`, `MAGMOM` has three components for every ion in the
   spinor-space basis defined by `SAXIS`. With the default `SAXIS`, that is the
   Cartesian basis. Retain all three components even for collinear initial
   moments.
4. The paired physical inputs are identical except for the approved `SAXIS`
   direction.
5. The Spec states the energy convention explicitly, for example
   `MAE = E[100] - E[001]`, and requires the result and units under that same
   convention.

Unequal chemical cells or lattice constants do not by themselves establish a
pure interface effect. The acceptance rule must preserve and compare the source
task and both directional inputs. Any required scientific choice not approved
above remains unresolved.
