# VASP server-side handoff

Resolve every source from the selected Spec's exact upstream task and current Run. Never infer an upstream Run from neighboring directories. Large `CHGCAR` and `WAVECAR` files remain server-side and are excluded from local transfer.

During `run.sh prepare`, call `copy_immutable SOURCE DESTINATION || return 1` once per declared file. Band uses the accepted SCF `outputs/CHGCAR`; Wannier pre-run uses the accepted SCF `outputs/CHGCAR` and `outputs/WAVECAR`; MAE uses the one approved SCF `outputs/CHGCAR` for both directional Runs. Existing differing destinations stop preparation. Record source and destination paths and compare bytes before validation and transient review.
