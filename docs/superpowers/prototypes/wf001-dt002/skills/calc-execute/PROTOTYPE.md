# DT002 SCF to band prototype

Throwaway fixture for `WF-001/DT-002`. The nested `skills/calc-execute/` path
mirrors the approved future skill seam without adding a seventh skill to the
Calc Project plugin. This fixture must not be merged into the production roster.

The probe separates one VASP SCF-to-band task into three kinds of source:

- `references/backends/vasp/`: selectively read execution knowledge;
- `assets/templates/vasp/`: copied task-input baselines;
- `scripts/vasp/`: executable, deterministic staging checks.

Run the filesystem seam without VASP or a scheduler:

```bash
bash docs/superpowers/prototypes/wf001-dt002/skills/calc-execute/scripts/vasp/smoke_scf_band.sh
```

The smoke selects and reads the stage-specific backend reference bundle, stages
representative SCF and band task inputs under a temporary directory, creates a
representative server-side SCF `CHGCAR`, copies it into the band Run boundary,
and verifies the declared inputs and output handoff. It does not claim to
validate material parameters, execute VASP, or submit PBS.
