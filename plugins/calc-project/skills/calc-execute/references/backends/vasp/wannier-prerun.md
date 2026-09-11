# VASP Wannier pre-run execution

Use `assets/templates/vasp/wannier-prerun/cluster-env.sh.template` and `assets/templates/vasp/wannier-prerun/run.pbs.template`. Before review, prepare POTCAR and copy the exact approved SCF `CHGCAR` and `WAVECAR` through the common immutable handoff.

The prepared INCAR contains only the approved broad pre-run outer window (`dis_win_min = -10`, `dis_win_max = 10`) and omits `dis_froz_*`; it does not determine the final subspace. Require nonempty spin-resolved `wannier90.1.{amn,mmn,eig,win}` and `wannier90.2.{amn,mmn,eig,win}`. A missing channel blocks the handoff.
