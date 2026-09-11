# VASP band execution

Use `assets/templates/vasp/band/run.pbs.template`. Before review, copy the exact current upstream SCF `CHGCAR` to `inputs/CHGCAR` through `copy_immutable SOURCE DESTINATION || return 1`, stage the exact owner helper `scripts/wannier90/vest2.py` as `inputs/vest2.py`, and prepare POTCAR. Name the upstream Run and source file from the Spec; directory guessing is not allowed.

PBS runs the VASP band calculation, then VASPKIT menu input `21 → 211 → 1`, then exactly `printf '5\ny\n8\n' | python3 ./vest2.py`. Require nonempty `BAND.dat`, `DOSCAR`, `REFORMATTED_BAND_UP.dat`, `REFORMATTED_BAND_DW.dat`, `bandrange_spin0.dat`, and `bandrange_spin1.dat`. VEST reports spin ranges; it never selects Wannier windows. `scripts/vasp/plot_vasp_band.py` may plot the unprojected blank-separated `BAND.dat`.
