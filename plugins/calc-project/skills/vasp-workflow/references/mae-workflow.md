# Directional SOC-MAE workflow

Use this reference for a user-confirmed magnetocrystalline anisotropy energy
(MAE) comparison based on directional static SOC calculations. It documents a
manual preparation and review method; it does not generate inputs or select
physical settings.

## Paired static comparison

1. Record the confirmed source SCF task and charge-density provenance.
2. Start each directional static calculation from that charge density with
   `ISTART=0` and `ICHARG=11`.
3. Use `LSORBIT=.TRUE.`, `ISYM=-1`, and a user-confirmed spinor `NBANDS`.
4. With `LSORBIT=.TRUE.`, supply `MAGMOM` as three components for every ion.
   Specify those components in the spinor-space basis defined by `SAXIS`; with
   the default `SAXIS`, this is the Cartesian basis. Keep all three components
   even when the intended initial moments are collinear.
5. Keep the paired inputs identical except for the user-confirmed `SAXIS`
   direction.
6. State the energy-difference convention explicitly, for example
   `MAE = E[100] - E[001]`, alongside the reported result and units.

## Limits

`MAGMOM`, cutoff, k mesh, Hubbard parameters, electronic convergence settings,
and the need for additional directions or angular scans remain material-specific
choices. Unequal chemical cells or lattice constants cannot, by themselves,
establish a pure interface effect. Preserve the source task and both directional
inputs so that the comparison remains reviewable.
