# Cluster Software Profiles

Create project-root `software-profiles.md` only when cluster configuration is
requested. Record the user-reviewed host, component label, path or invocation,
and one exact non-interactive verification command. A default is configuration,
not verification evidence.

Keep this marker block in the profile so the verifier can replace only its
contents:

```markdown
<!-- cluster-profile-status:start -->
## Verification status

No probes have run. Configured defaults are unverified.
<!-- cluster-profile-status:end -->
```

Probe one reviewed entry at a time:

```bash
bash <calc-project-plugin-root>/skills/calc-setup/scripts/verify_cluster_profile.sh \
  <project-root>/software-profiles.md <ssh-host> <component-label> \
  '<reviewed-remote-command>'
```

The verifier calls `ssh -- "$host" "$remote_command"` directly. It neither
evaluates the command locally nor adds shell initialization, paths, or commands.
After the probe it records the supplied label and command, a bounded output
summary with explicit truncation when needed, and `verified` or `unavailable`
inside the existing marker block. Later probes retain other component rows and
replace the row for the same component label.
An SSH failure is unavailable evidence and returns failure after updating the
profile. Review failed probes before retrying; do not relabel them as verified.

## Example profile entries

The following mu01 examples are historical starting points only. Copy an entry
only when the project selects it, review its current path and exact probe, and
leave it explicitly `unverified` until that probe runs.

| Component | Example configuration | Example probe | Initial status |
|---|---|---|---|
| PBS / Torque | `qsub`, `qstat` after project-reviewed initialization | `source /etc/profile && qstat -B` | unverified |
| VASP standard | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std` | `test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std` | unverified |
| VASP noncollinear | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl` | `test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl` | unverified |
| VASPKIT | `/data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit` | `test -x /data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit` | unverified |
| Wannier90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x` | `test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x` | unverified |
| postw90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x` | `test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x` | unverified |
| TB2J | `conda run -n tb2j wann2J.py` | `conda run -n tb2j wann2J.py --help` | unverified |
| VAMPIRE | `/data1/yuzheli-alkemie/01Soft/vampire/linux/vampire` | `test -x /data1/yuzheli-alkemie/01Soft/vampire/linux/vampire` | unverified |
| Hefei-NAMD | `/data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd` | `test -x /data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd` | unverified |
| NAMDwithSOC | `/data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc` | `test -x /data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc` | unverified |

Concrete Run preparation rechecks the exact mutable environment through
`calc-execute`; setup-time profile evidence does not authorize submission.
