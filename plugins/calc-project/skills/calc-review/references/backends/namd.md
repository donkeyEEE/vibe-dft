# Hefei-NAMD Read-only Checks

Compare the prepared representation and band window with the current Spec.
For NAMDwithSOC 1.5.2, require `SOCTYPE=1` with `BMIN/BMAX` and two-column
`INICON` for spin-adiabatic input, or `SOCTYPE=2` with the up/down band fields
and three-column `INICON` for spin-diabatic input. Do not infer `SOCTYPE=2`
solely from non-collinear or SOC VASP flags; VASP 6.5 non-collinear SOC may
report effective `ISPIN=1` while storing spinors.

Inspect every declared snapshot's nonempty OUTCAR/EIGENVAL/WAVECAR sources;
effective `ISPIN`, `NKPTS`, `NBANDS`, SOC flags, indices, and occupations;
`RUNDIR`; the installed-code-derived `I0.<len(NSW)>` names; and source
read-only protection. For `NSW=5`, expected names are `1` through `5`, not
four-digit VASP-style names. Require the task's exact coupling/product and
failure-marker checks. A small interface smoke test is not evidence that a
production trajectory is valid. Scientific mismatch belongs to
`$calc-to-spec`; staging, protection, field, or environment mismatch belongs
to `$calc-execute`, and either is `block`.
