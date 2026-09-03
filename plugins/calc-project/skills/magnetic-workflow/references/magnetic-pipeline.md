# Magnetic Pipeline

`calc-task` creates these execution tasks under the confirmed magnetic calculation
line. Each has the standard task skeleton; the numbered names preserve handoff
order. `00-structure/` holds approved structure sources and provenance but is not
a task. The Wannier scientific stage has separate VASP pre-run and Wannier90 tasks.

| Task directory | Stage owner | Required handoff and acceptance |
|---|---|---|
| `01-vasp-scf-<tag>/` | `vasp-workflow` | Converged SCF; retain original `OUTCAR` final `E-fermi`; for layered magnetic tasks, complete the [magnetic-handoff preflight](magnetic-handoff-preflight.md) before downstream handoff. |
| `02-vasp-band-<tag>/` | `vasp-workflow` | SCF-derived band run; `band/vest2.py`, two nonempty spin-range files, reformatted bands, and `DOSCAR`. |
| `03-wannier-prerun-<tag>/` | magnetic workflow | Spin-resolved `.amn`, `.mmn`, `.eig`, and generated `.win` interface files. |
| `04-wannier90-<tag>/` | magnetic workflow | Two nonempty `*_hr.dat`, `*_centres.xyz`, band data, and fit plots. |
| `05-tb2j-<tag>/` | magnetic workflow | Chosen spin assets, `exchange.out`, and `TB2J_results/Vampire/` source. |
| `06-vampire-<tag>/` | magnetic workflow | Verified source-to-copy mapping and `M_vs_T.png` from named `output` columns. |

- Put workflow purpose and handoff summaries in the relevant task `README.md`;
  `calc-task.yaml` remains authoritative for task facts.
- `vasp-workflow` runs VASPKIT `21 → 211 → 1` in the band task. This workflow
  writes approved plugin `scripts/wannier/vest2.py` to `band/vest2.py`, runs VEST
  only after that export, and requires two nonempty spin-range files. VEST reports
  a range and never selects Wannier windows.
- Pre-run `INCAR` uses only `dis_win_min = -10` and `dis_win_max = 10`; omit
  `dis_froz_*`. The user supplies separate up/down `dis_win_*` and `dis_froz_*`
  values in `04-wannier90-<tag>/inputs/wannier-run.env`. Never derive, replace, or
  share them; `PLOT_EMIN`/`PLOT_EMAX` are plotting controls only.
- Before selecting or reviewing the final per-spin windows in the Wannier90
  stage, follow [Wannier-window selection](wannier-window-selection.md).
- TB2J records the structure, magnetic atoms/orbitals, Fermi convention, spin
  representation, `wann2J.py` arguments, and user-selected k mesh. Do not infer
  that mesh from Wannier `mp_grid`; require sensitivity evidence.
- Preserve stage inputs, outputs, material settings, and each source-to-copy
  mapping before considering the pipeline complete.
