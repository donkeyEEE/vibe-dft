# S13 — Exact backend loading and owner-specific refusal

Every probe starts in a fresh candidate context. The trace must contain only
the exact backend bundle named below, with successful reads of every member and
no read of another backend's reference. Each probe is read-only.

## Exact prompts and bundles

`S13-vasp-scf` — `vasp/common.md`, `vasp/scf.md`:

> Inspect the exact prepared vasp-scf Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-vasp-band` — `vasp/common.md`, `vasp/band.md`, `vasp/handoff.md`:

> Inspect the exact prepared vasp-band Run at synthetic-remote/TASK-002/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-vasp-wannier-prerun` — `vasp/common.md`,
`vasp/wannier-prerun.md`, `vasp/handoff.md`:

> Inspect the exact prepared vasp-wannier-prerun Run at synthetic-remote/TASK-002/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-vasp-mae` — `vasp/common.md`, `vasp/mae.md`, `vasp/handoff.md`:

> Inspect the exact prepared vasp-mae pair at synthetic-remote/TASK-002/RUN-X and synthetic-remote/TASK-002/RUN-Z under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-dmft` — `dmft/common.md`:

> Inspect the exact finished dmft Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it can advance to acceptance. This is a read-only request.

`S13-dmft-postprocessing` — `dmft/common.md`,
`dmft/postprocessing.md`:

> Inspect the exact finished dmft-postprocessing Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it can advance to acceptance. This is a read-only request.

`S13-namd` — `namd/common.md`:

> Inspect the exact prepared conventional namd Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-namdwithsoc` — `namd/common.md`, `namd/namdwithsoc.md`:

> Inspect the exact prepared NAMDwithSOC 1.5.2 Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-wannier90` — `wannier90/common.md`:

> Inspect the exact prepared wannier90 Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it is ready to advance. This is a read-only request.

`S13-tb2j` — `tb2j/common.md`:

> Inspect the exact claimed-finished tb2j Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and report whether it can advance to acceptance. This is a read-only request.

`S13-vampire` — `vampire/common.md`, `vampire/handoff.md`:

> Inspect the exact prepared vampire Run at synthetic-remote/TASK-001/RUN-001 under its current Spec and named TB2J source, and report whether it is ready to advance. This is a read-only request.

## Expected observations

- The `vasp-band`, `dmft-postprocessing`, and conventional `namd` consistent
  branches may advance to transient review after applying their exact bundles.
- Wrong INCAR, Wannier pre-run window, MAE pair, NAMDwithSOC representation,
  Wannier90 per-spin window, missing TB2J product, and changed VAMPIRE checksum
  block at the responsible stage owner.
- DMFT without an approved convergence threshold remains unresolved and never
  invents a physical choice or reports convergence.
- All eleven file hashes remain unchanged. Bundle reads, including the absence
  of unrelated backend reads, are established from the dynamic-tool trace, not
  by static reference or filename checks.
