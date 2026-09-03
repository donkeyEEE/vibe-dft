# VASPKIT Operations

Run VASPKIT only beside the intended `POSCAR`. Record the task ID and generated
files in the workflow handoff. In a VASP PBS script, define and use:

```bash
VASPKIT_EXE="${VASPKIT_EXE:-vaspkit}"
(echo <menu-input>) | "$VASPKIT_EXE" >> vaspkit_output 2>&1
```

The variable may be set to the verified absolute executable path; preserve the
redirect so each VASPKIT call is captured in `vaspkit_output`.

| Need | Task | Rule |
|---|---:|---|
| Explicit KPOINTS mesh | 102 | Only with `GENERATE_KPOINTS=1`: `(echo 102; echo 2; echo 0.04) \| "$VASPKIT_EXE" >> vaspkit_output 2>&1` |
| POTCAR without changing KPOINTS | 103 | Use for generic VASP, bands, and Wannier pre-runs: `(echo 103) \| "$VASPKIT_EXE" >> vaspkit_output 2>&1` |
| Band path | 301/302/303 | Check dimensionality and symmetry before `KPATH.in -> KPOINTS` |
| Export bands | 211 | Require `BAND.dat` after completion |

Use task 302 only for a deliberately 2D/slab SOC band path; use 303 for bulk.
Before VASP, check POSCAR species order against PAW choices and species-indexed
INCAR arrays. For a plain VASPKIT band plot, run
`python plot_vasp_band.py --input BAND.dat --output band.png`.
