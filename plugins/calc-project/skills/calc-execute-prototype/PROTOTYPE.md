# DT002 SCF to band prototype

Throwaway source for `WF-001/DT-002`. It is not a published skill and must not
be merged into the production roster.

The probe separates one VASP SCF-to-band task into three kinds of source:

- `references/backends/vasp/`: selectively read execution knowledge;
- `assets/templates/vasp/`: copied task-input baselines;
- `scripts/vasp/`: executable, deterministic staging checks.

Run the filesystem seam without VASP or a scheduler:

```bash
bash plugins/calc-project/skills/calc-execute-prototype/scripts/vasp/smoke_scf_band.sh
```

The smoke stages representative SCF and band task inputs under a temporary
directory, creates a representative server-side SCF `CHGCAR`, copies it into
the band Run boundary, and verifies the declared inputs and output handoff. It
does not claim to validate material parameters, execute VASP, or submit PBS.
