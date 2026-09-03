# Cluster Software Profiles

When requested, create project-root `software-profiles.md` from the selected
profile. Write the defaults below, then run every verification command on the
target host and record the command, date, output summary, and `verified` or
`unavailable` status. Default values are not verification evidence.

Resolve `<calc-project-plugin-root>` from the active installed skill, then the
bundled verifier may be run as:

```bash
bash <calc-project-plugin-root>/scripts/common/verify_cluster_profile.sh \
  <project-root>/software-profiles.md <ssh-host>
```

## mu01 defaults

| Component | Default path or invocation | Verification |
|---|---|---|
| PBS / Torque | `qsub`, `qstat` after `source /etc/profile` | `source /etc/profile && qstat -B` |
| VASP standard | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std` | `test -x <path>` |
| VASP noncollinear | `/data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl` | `test -x <path>` |
| VASPKIT | `/data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit` | `test -x <path>` |
| Wannier90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x` | `test -x <path>`; record MPI launcher separately |
| postw90 | `/data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x` | `test -x <path>` |
| TB2J | `conda run -n tb2j wann2J.py` | `conda run -n tb2j wann2J.py --help` |
| VAMPIRE | `/data1/yuzheli-alkemie/01Soft/vampire/linux/vampire` | `test -x <path>` |
| Hefei-NAMD | `/data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd` | `test -x <path>` |
| NAMDwithSOC | `/data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc` | `test -x <path>` |
| Intel MPI | `/opt/intel2020/compilers_and_libraries_2020.1.217/linux` | source `compilervars.sh`, `mklvars.sh`, and `mpi/intel64/bin/mpivars.sh`; then `command -v mpirun` |

Non-interactive SSH does not load `/etc/profile`; source it before PBS queries.
Use the versioned VASP path for new scripts unless the task explicitly selects a
different build. Do not invent a TB2J executable path, and recheck queue, cores,
walltime, modules, and executables for every concrete task.
