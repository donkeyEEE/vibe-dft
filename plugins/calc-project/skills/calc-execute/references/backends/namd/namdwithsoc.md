# NAMDwithSOC 1.5.2 execution

Load this reference after `common.md` only for a NAMDwithSOC branch. The source
behavior below is verified for NAMDwithSOC 1.5.2. Another implementation or
version requires its own evidence in `$calc-to-spec` before preparing
`inputs/run.pbs`; similarity is not evidence.

## Representation contract

In NAMDwithSOC 1.5.2, `couplings.f90` initializes
`olap%ISPIN = inp%SOCTYPE` and rejects a WAVECAR when its parsed spin-component
count differs. `fileio.f90` defines these two representations:

- `SOCTYPE=1` is spin-adiabatic, uses `BMIN/BMAX`, and each `INICON` row is
  `time_index band`.
- `SOCTYPE=2` is spin-diabatic, uses `BMINU/BMAXU` plus `BMIND/BMAXD`, and each
  `INICON` row is `time_index band spin`.

For a VASP 6.5 noncollinear SOC source, `OUTCAR` may report effective `ISPIN =
1` while WAVECAR stores spinor coefficients. The verified choice for that case
is spin-adiabatic `SOCTYPE=1`. `LSORBIT=.TRUE.` or
`LNONCOLLINEAR=.TRUE.` does not establish `SOCTYPE=2`. If the approved Spec says
otherwise, or the WAVECAR representation is not established, block the Run and
return the conflict to `$calc-to-spec`.

Before review, compare the approved `BMIN/BMAX` or
`BMINU/BMAXU`+`BMIND/BMAXD` bounds with the `EIGENVAL` band indices and
occupations in every frame. Each initial band and optional spin value in
`INICON` must satisfy the matching approved window and column contract. A
missing field, a band outside the window, or inconsistent occupations blocks;
changing the window or initial-condition meaning belongs to `$calc-to-spec`.

## Snapshot layout

The coupling source formats snapshot indices as `I0.<len(NSW)>`. For `NSW=5`,
the exact layout is `RUNDIR/1/WAVECAR` through `RUNDIR/5/WAVECAR`; the five
directory names have one digit and the Run expects four coupling intervals.
For any other `NSW`, derive the width from the installed source or establish it
with a small interface test before rendering the exact staging paths. A
four-digit VASP-style convention is not evidence.

Make the value written in the approved NAMD input's `RUNDIR` field match the
Run-local staging root exactly. Preparation follows `common.md` to stage every
named snapshot into immutable server-side inputs without modifying the source
Runs. The concrete `inputs/run.pbs` recreates only that approved relative
layout in its private `outputs/` working tree and runs the configured
NAMDwithSOC executable; it does not scan for snapshots or repair names.

## Targeted failure and success evidence

Preserve the full log and staging on failure. Targeted scans treat `File I/O
error`, `No. of spin components does NOT match`, fatal, abort, and segmentation
markers as failure evidence. These markers identify a preflight category, not
an authorized patch; missing knowledge or competing diagnoses stop the
workflow.

For the five-snapshot interface case, success requires evidence of four
coupling intervals plus nonempty `COUPCAR`, `NATXT`, `EIGTXT`, and at least one
nonempty `SHPROP.*` or `PSICT.*` output family, with none of the failure markers
in the targeted scan. These are minimal interface-success checks only. The
approved Spec's production observables and decisive criteria still determine
whether the Run can be accepted; an interface smoke test is not production
trajectory validation.
