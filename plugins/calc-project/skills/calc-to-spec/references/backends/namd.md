# Hefei-NAMD/NAMDwithSOC scientific design

Use this reference when a Spec commits to a VASP-to-Hefei-NAMD/NAMDwithSOC
representation or band window. The version-specific rules below were verified
for NAMDwithSOC 1.5.2; other versions require their own evidence.

## Evidence and approval inputs

Read the accepted RQ decisions, installed NAMD implementation/version evidence,
source VASP records, and representative `OUTCAR` and `EIGENVAL` evidence across
the intended snapshots. Obtain approval for the physical representation,
`SOCTYPE`, band-window fields and bounds, initial-condition meaning, source
snapshot set, requested observables, and production acceptance and stopping
criteria. An interface smoke test is not approval of a production trajectory.

## Representation commitments

In NAMDwithSOC 1.5.2, `couplings.f90` initializes `olap%ISPIN` from
`inp%SOCTYPE` and rejects a WAVECAR whose parsed spin-component count differs.
The corresponding input representations are:

- `SOCTYPE=1`: spin-adiabatic, with `BMIN/BMAX`; each `INICON` row is
  `time_index band`.
- `SOCTYPE=2`: spin-diabatic, with `BMINU/BMAXU` and `BMIND/BMAXD`; each
  `INICON` row is `time_index band spin`.

For VASP 6.5 noncollinear SOC calculations, `OUTCAR` can report `ISPIN = 1`
while WAVECAR stores spinor coefficients. The verified representation for that
case is the spin-adiabatic `SOCTYPE=1` branch. `LSORBIT=.TRUE.` or
`LNONCOLLINEAR=.TRUE.` alone does not establish `SOCTYPE=2`.

Before approving band commitments, inspect effective `ISPIN`, `NKPTS`,
`NBANDS`, `LSORBIT`, and `LNONCOLLINEAR` for every included snapshot and check
band indices and occupations across all frames. The Spec must make `SOCTYPE`,
band fields, and `INICON` column meaning agree. Representation uncertainty or
incomplete version evidence remains an unresolved design decision.
