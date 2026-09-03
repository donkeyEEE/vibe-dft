---
name: TRK-011-magnetic-handoff-mae-energy-map-evidence
type: calc-experience-candidate
source_plugin: calc-project
status: candidate
updated_at: 2026-08-18
---

# TRK-011: Magnetic handoff, MAE, and energy-mapping evidence

## Status

Active evidence record. PRP-011 has added documentation-only workflow guidance;
the record preserves the project-supplied evidence and changes no task directory
or remote calculation.

## Targeted evidence

- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-08-03-TB2J收敛与bulk对照问题及解决方案.md`
- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-07-26-MAE-厚度依赖假设与计算记录.md`
- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-07-30-2L-MnSe与界面能量映射交换常数.md`

## Distilled experience

### EXP-001: magnetic-layer-order-magmom-handoff

#### Observation

For the original `TI-4L-MnSe-TI` calculation line, Mn atom numbering did not
follow the z-direction layer order. Assigning `MAGMOM` as `+ - + -` by atom
index produced the actual layer order `up down down up`, rather than the
intended A-type AFM `up down up down`. Normal VASP completion, a near-zero
total moment, and TB2J grid convergence did not reveal this mismatch.

#### Evidence

- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-08-03-TB2J收敛与bulk对照问题及解决方案.md` documents the Mn z coordinates, the mismatch, and that the corrected index-order pattern is `+ - - +` for this structure.
- `/home/donk/02projects/MnSe-TI/04-New-data/TI-4L-MnSe-TI-v2-all-relax/01-vasp-relax-afm/calc-task.yaml` is the restarted all-atom-relaxation task that should be inspected as a future reference case.

#### Conditions and limits

Applies to layered magnetic structures whenever the intended magnetic order is
defined by geometric layer sequence. It is not a claim that every magnetic
task is layered, nor that a fixed `MAGMOM` sequence is transferable between
structures.

#### Candidate knowledge

Before handing a magnetic VASP task to SCF or downstream Wannier/TB2J stages,
future workflow development should consider presenting a checkable table of
magnetic atom index, species, fractional z, z-sorted layer rank, and assigned
`MAGMOM`; the intended order must remain a user-confirmed physical choice.

#### Suggested ownership

`magnetic-workflow` for the cross-stage handoff check, with `vasp-workflow`
owning any INCAR-level presentation or validation.

#### Proposal status

Implemented: PRP-011

### EXP-002: soc-mae-directional-static-workflow

#### Observation

The completed 2QL MnSe--Bi2Te3 SOC-MAE task used charge-density handoff from
SCF and two static directions, with `MAE = E[100] - E[001]`. Its project
template specifies `ISTART=0`, `ICHARG=11`, `LSORBIT=.TRUE.`, `ISYM=-1`, an
explicit spinor `NBANDS`, identical direction inputs except `SAXIS`, and an
analysis script that reports this convention.

#### Evidence

- `/home/donk/02projects/MnSe-TI/02原始数据/01-MnSe-TI-interface/2L-MnSe-2QL-Bi2Te3/07-MAE/calc-task.yaml` and `/home/donk/02projects/MnSe-TI/02原始数据/01-MnSe-TI-interface/2L-MnSe-2QL-Bi2Te3/07-MAE/` are the completed task reference.
- `/home/donk/02projects/MnSe-TI/calculation_templates/vasp/mae/README.md` and `/home/donk/02projects/MnSe-TI/calculation_templates/vasp/mae/scripts/{prepare_run.sh,validate_run.sh,run_vasp_mae.pbs,submit_run.sh,analyze_mae.py}` record the local reusable procedure and analysis convention.
- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-07-26-MAE-厚度依赖假设与计算记录.md` records completed outputs and the limits on comparing unequal cells or lattices.

#### Conditions and limits

These are project-specific validated settings and a method record, not a
universal SOC-MAE default. Material-specific magnetic order, `MAGMOM`,
cutoff, k mesh, Hubbard parameters, and the need for `[010]` or angular scans
remain explicit scientific choices. Unequal chemical cells or lattice constants
cannot establish a pure interface effect without controlled references.

#### Candidate knowledge

Future plugin development may evaluate a MAE workflow reference that requires
an explicit energy-difference convention, direction-paired input comparison,
SCF charge-density provenance, and a stated comparability boundary; it must
not infer physical settings or causal conclusions.

#### Suggested ownership

`vasp-workflow` for SOC-MAE task preparation; `script-management` for any
future promotion of these project templates.

#### Proposal status

Implemented: PRP-011

### EXP-003: energy-map-design-matrix-and-fit-diagnostics

#### Observation

For the fixed `2x2x1` eight-configuration energy-mapping set, the fit has four
unknowns. Symmetry-equivalent stripe configurations duplicate design-matrix
rows, so they do not add independent equations. A full interface fit with a
large residual and exactly determined four-configuration subsets with zero
RMSE cannot be reported as reliable exchange parameters merely from their
fitted signs.

#### Evidence

- `/home/donk/02projects/MnSe-TI/calculation_templates/EnergyMap/count_exchange_bonds.py`, `/home/donk/02projects/MnSe-TI/calculation_templates/EnergyMap/generate_energy_map_matrix.py`, and `/home/donk/02projects/MnSe-TI/calculation_templates/EnergyMap/scan_energy_map_subsets.py` implement periodic bond counting, matrix generation, fitting, and subset diagnostics.
- `/home/donk/02projects/MnSe-TI/calculation_templates/EnergyMap/README.md` documents the unit-cell assumptions, no-double-counting convention, rank requirement, and interpretation limits.
- `/home/donk/02projects/MnSe-TI/03Key-data/2L-MnSe/05-energy-map/` and `/home/donk/02projects/MnSe-TI/03Key-data/2L-MnSe-1QL-Bi2Te3/05-energy-map/` are the corresponding eight-task calculation references; their `energy-map-fit.json` and `energy-map-subset-scan.json` retain fit evidence.
- `/home/donk/02projects/MnSe-TI/01mnse-ti-interface-magnetism/03-计算笔记/2026-07-30-2L-MnSe与界面能量映射交换常数.md` records the model, duplicated rows, residuals, and interpretation boundary.

#### Conditions and limits

The generator is intentionally limited to the pure 2L MnSe two-Mn primitive
cell and fixed eight-configuration scheme. Bond equivalence in an interface,
the Hamiltonian, cutoff, fitting subset, and physical acceptance criteria are
scientific modelling decisions and must not be silently generalized.

#### Candidate knowledge

Future plugin development may evaluate a separate opt-in energy-mapping
workflow that preserves explicit bond-counting conventions and reports matrix
rank, duplicate rows, residuals, configuration coverage, and fit limits before
presenting exchange parameters. It must not select a subset by a desired J
sign or turn a numerical fit into a magnetic-ground-state claim.

#### Suggested ownership

A future dedicated `energy-map-workflow` skill, with `script-management`
owning template/script promotion and `calc-task` owning individual
configuration-task metadata.

#### Proposal status

Implemented: PRP-011

### EXP-004: spin-resolved-wannier-window-evidence

#### Observation

The VASP-to-Wannier pre-run supplies only a broad outer window; the final
spin-resolved outer and frozen windows are selected later from the task's
bandrange evidence and must satisfy the `NUM_WANN` state-count constraint. In
the six-layer bulk V2 case, an 8.5 eV frozen maximum failed because it contained
more states than `NUM_WANN=48`; VEST bandrange showed band 73 begins at 8.351
eV, so 8.3 eV retains bands 25--72. In the corrected interface V2 case,
outer-window bounds and an initial frozen window were identified from band
edges and the gap; the frozen upper bound was later expanded to 8.70 eV while
retaining at most 45 frozen states per k point for `NUM_WANN=47`.

#### Evidence

- `/home/donk/02projects/MnSe-TI/04-New-data/bulk-MnSe-6L-v2/05-wannier90-afm/calc-task.yaml`, `/home/donk/02projects/MnSe-TI/04-New-data/bulk-MnSe-6L-v2/05-wannier90-afm/README.md`, and `/home/donk/02projects/MnSe-TI/04-New-data/bulk-MnSe-6L-v2/05-wannier90-afm/wannier/wannier90.1.win` record the 8.5 eV failure, 8.3 eV correction, VEST bandrange basis, `guiding_centres = true`, current windows, and pulled fit artefacts.
- `/home/donk/02projects/MnSe-TI/04-New-data/TI-4L-MnSe-TI-v2-all-relax/05-wannier90-afm/calc-task.yaml` and `/home/donk/02projects/MnSe-TI/04-New-data/TI-4L-MnSe-TI-v2-all-relax/05-wannier90-afm/wannier/wannier90.1.win` record the corrected-AFM interface band edges, gap-based initial window, expanded 8.70 eV frozen maximum, and final WIN settings.
- `/home/donk/02projects/MnSe-TI/04-New-data/bulk-MnSe-6L-v2/05-wannier90-afm/inputs/plot_wannier_fit_up.py`, `/home/donk/02projects/MnSe-TI/04-New-data/bulk-MnSe-6L-v2/05-wannier90-afm/inputs/plot_wannier_fit_dn.py`, `/home/donk/02projects/MnSe-TI/04-New-data/TI-4L-MnSe-TI-v2-all-relax/05-wannier90-afm/inputs/plot_wannier_fit_up.py`, and `/home/donk/02projects/MnSe-TI/04-New-data/TI-4L-MnSe-TI-v2-all-relax/05-wannier90-afm/inputs/plot_wannier_fit_dn.py` are the spin-resolved VASP-versus-Wannier fit-plot helpers; corresponding `wannier/band_structure-up.png` and `wannier/band_structure-dn.png` are the lightweight validation artefacts.
- `/home/donk/02projects/MnSe-TI/02原始数据/01-MnSe-TI-interface/01-vasp-wannier-tb2j-vampire/03-wannier-prerun/calc-task.yaml` records that pre-run broad windows do not automatically determine the spin-specific Wannier90 windows.

#### Conditions and limits

The listed windows, band indices, projections, and `NUM_WANN` values are valid
only for their recorded structures, magnetic states, and selected subspaces.
Bandrange is the selection evidence in these V2 tasks; it does not replace
inspection of projections, WOUT diagnostics, or spin-resolved fit plots. A
successful Wannier90 run is not by itself proof that a window is physically
adequate.

#### Candidate knowledge

Future plugin development may evaluate an explicit, task-local Wannier-window
record and preflight: record per-spin outer/frozen bounds, their bandrange or
other stated basis, `NUM_WANN`, the maximum frozen-state count per k point,
projection set, and links to WOUT and fit plots. The preflight should reject or
flag a frozen window that exceeds the target Wannier-function count, preserve
superseded attempts as evidence, and require user confirmation of the
scientific subspace rather than deriving windows automatically from a VASP
pre-run.

#### Suggested ownership

`magnetic-workflow` for VASP--Wannier90 stage handoff, `calc-workflows` for a
shared handoff contract, and `script-management` for any reusable bandrange or
fit-plot helper.

#### Proposal status

Implemented: PRP-011

## Proposal

### PRP-011: magnetic handoff and method references

On the user's confirmed direction, make the following scoped documentation
changes in a subsequent implementation step:

1. `magnetic-workflow` defines a required VASP-to-downstream handoff check for
   layered magnetic tasks: review magnetic-atom index, species, fractional-z
   ordering, intended layer sequence, and assigned `MAGMOM`. The workflow must
   present evidence for user confirmation and must not infer a magnetic order.
2. `vasp-workflow` adds a reference for directional SOC-MAE static calculations:
   state the energy-difference convention, SCF charge-density provenance,
   paired-input comparison, and cross-cell comparability boundary. It must not
   promote project-specific numerical settings as universal defaults.
3. `magnetic-workflow/references/` adds an energy-mapping method record:
   preserve Hamiltonian and bond-counting assumptions, matrix rank and duplicate
   rows, residual and coverage diagnostics, and fit-interpretation limits.
4. `magnetic-workflow/references/` adds a spin-resolved Wannier-window strategy:
   require task-local selection evidence, `NUM_WANN` state-count checks, WOUT
   and fit-plot review, and user confirmation of the selected subspace.

No new task generator, scientific default, or automatic physical decision is
in scope for this proposal.

## Implementation

PRP-011 was implemented as documentation-only guidance in
`magnetic-workflow` and `vasp-workflow`: magnetic-layer/MAGMOM handoff,
directional SOC-MAE, energy mapping, and spin-resolved Wannier-window
references. The implementation adds no scripts or automatic scientific choice.

## Versions

- First recorded: `0.1.0+codex.20260803151026`
- Last verified: project evidence inspected on 2026-08-03
