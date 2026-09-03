# Formal Template Index

Only the templates registered here are formal shared assets. Every calculation
template also requires the acceptance recorded in
[`computation/ACCEPTANCE.md`](computation/ACCEPTANCE.md).

| Path | Method | Purpose | Status |
|---|---|---|---|
| `common/prepare_and_submit.sh.template` | common | Prepare, validate, and submit a tagged run | accepted |
| `common/prepare_run.sh.template` | common | Prepare a tagged run directory | accepted |
| `common/submit_run.sh.template` | common | Submit an already prepared run | accepted |
| `common/validate_run.sh.template` | common | Validate prepared inputs before submission | accepted |
| `tb2j/cluster-env.sh.template` | TB2J | Define cluster-specific TB2J environment | accepted |
| `tb2j/run_tb2j.pbs.template` | TB2J | Execute exchange extraction on PBS | accepted |
| `vampire/cluster-env.sh.template` | VAMPIRE | Define cluster-specific VAMPIRE environment | accepted |
| `vampire/run_vampire.pbs.template` | VAMPIRE | Execute atomistic spin simulation on PBS | accepted |
| `vasp/cluster-env.sh.template` | VASP | Define cluster-specific VASP environment | accepted |
| `vasp/run_vasp.pbs.template` | VASP | Execute a standard VASP run on PBS | accepted |
| `vasp/run_vasp_band.pbs.template` | VASP | Execute band postprocessing and handoff on PBS | accepted |
| `wannier/cluster-env.sh.template` | Wannier90 | Define cluster-specific Wannier environment | accepted |
| `wannier/run_vasp_wannier_prerun.pbs.template` | VASP/Wannier90 | Produce spin-resolved Wannier inputs | accepted |
| `wannier/run_wannier90.pbs.template` | Wannier90 | Execute and validate spin-resolved Wannier models | accepted |

