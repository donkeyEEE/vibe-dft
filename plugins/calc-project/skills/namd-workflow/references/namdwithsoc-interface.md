# NAMDwithSOC interface reference

## Verified behavior: NAMDwithSOC 1.5.2

`couplings.f90` initializes `olap%ISPIN = inp%SOCTYPE`, then rejects a WAVECAR if its parsed spin-component count differs. In `fileio.f90`, the representation is defined as:

- `SOCTYPE=1`: spin-adiabatic; `BMIN/BMAX`; `INICON` rows are `time_index band`.
- `SOCTYPE=2`: spin-diabatic; `BMINU/BMAXU` plus `BMIND/BMAXD`; `INICON` rows are `time_index band spin`.

For VASP 6.5 noncollinear SOC calculations, `OUTCAR` can report `ISPIN = 1` even though the WAVECAR stores spinor coefficients. Use the spin-adiabatic (`SOCTYPE=1`) branch in this case. Do not infer `SOCTYPE=2` solely from `LSORBIT=.TRUE.` or `LNONCOLLINEAR=.TRUE.`.

## Snapshot layout

The coupling code formats snapshot indices with `I0.<len(NSW)>`. For `NSW=5`, the required paths are `RUNDIR/1/WAVECAR` through `RUNDIR/5/WAVECAR`. A PBS script launched from the task root should therefore use:

```text
inp:     RUNDIR = "run"
staging: run/1, run/2, ..., run/5
```

For a general `NSW`, derive the name width from the installed source or run a small interface test; do not assume four-digit VASP-style names.

## Reusable preflight checklist

- Check every source directory and required VASP file is nonempty.
- Check `OUTCAR` effective `ISPIN`, `NKPTS`, `NBANDS`, `LSORBIT`, and `LNONCOLLINEAR` for every snapshot.
- Check `EIGENVAL` band indices and occupations across all frames before selecting an initial band.
- Check that `RUNDIR`, staging directory names, `SOCTYPE`, band fields, and `INICON` column count agree.
- Link source files read-only by convention; do not copy or modify source `WAVECAR`/`CHGCAR`/`POTCAR`.
- Preserve failed logs and staging until the user explicitly authorizes deletion.

## Minimal success evidence

For five snapshots, expect four coupling intervals and nonempty `COUPCAR`, `NATXT`, `EIGTXT`, and one `SHPROP.*`/`PSICT.*` family. Targeted scans must show no `File I/O error`, `No. of spin components does NOT match`, fatal, abort, or segmentation markers.
