# Script Asset Catalog

This catalog covers bundled executable helpers only. Reusable `*.template`
assets are formal content in
`plugins/calc-project/knowledge/templates/INDEX.md`; `script-management`
validates them and the named downstream workflow decides whether and how a
formal template is copied into a task.

| Assets | Owner or consumer | Purpose | Principal validation |
|---|---|---|---|
| `common/compare_incar_parameters.sh` | `vasp-workflow` | Compare confirmed INCAR parameters | `bash -n`; task-specific INCAR review |
| `common/probe-cluster-env.sh`, `common/verify_cluster_profile.sh` | `calc-project-structure` | Probe a selected cluster and record project software-profile evidence | `bash -n`; read-only remote checks before writing status |
| `sync/sync_calc_data.py` | `calc-task` for `init`; `calc-sync` for all other commands | Create task YAML and perform reviewed-plan synchronization | `test_sync_calc_data.py`; `test_calc_task_schema.py` |
| `vasp/plot_vasp_band.py` | `vasp-workflow` | Unprojected band plotting | Python syntax; task-specific plot review |
| `wannier/vest2.py`, `wannier/plot_wannier_fit_*.py`, `wannier/wannier-run.env` | `calc-workflows` and `magnetic-workflow` | VEST conversion, fit plotting, and runtime reference | Python syntax; magnetic workflow tests |
| `vampire/plot.py`, `vampire/pack_magnetic_results.sh` | `magnetic-workflow` | VAMPIRE plotting and lightweight result packaging | `bash -n`; Python syntax; magnetic workflow tests |
| `maintenance/report_context_inventory.py` | Plugin maintainers | Read-only skill/reference context inventory | Python syntax; targeted manual invocation |

Historical task directories, completed-run outputs, large upstream files, and
remote paths are not bundled template sources. Adding an asset requires an
owner, an intended consumer, compatibility constraints, and a validation route
in this catalog.
