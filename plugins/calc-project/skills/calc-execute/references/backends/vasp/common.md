# VASP execution common

Use only after the Spec fixes the calculation type, structure and species order, `ENCUT`, k mesh, `ISPIN`/`MAGMOM`, smearing, `LORBIT`, `LWAVE`, `LCHARG`, and any SOC or DFT+U commitments. A template supplies no physical default. A missing or conflicting choice returns to `$calc-to-spec`.

Render `assets/templates/vasp/cluster-env.sh.template`, the selected VASP PBS template, and the common `assets/templates/common/run.sh.template` into the new Run's `inputs/`. The profile paths are rechecked before review. Prepare `POTCAR` before review beside the approved `POSCAR` in a private temporary directory with exact VASPKIT task 103, then call `copy_immutable TEMP/POTCAR "$INPUTS_DIR/POTCAR" || return 1`; task 102 is allowed only when the Spec explicitly requests generated KPOINTS. Every preparation command ends with `|| return 1`.

Require nonempty `INCAR`, `POSCAR`, `KPOINTS`, `POTCAR`, `cluster-env.sh`, `run.pbs`, and the stage-specific handoffs. Check POSCAR/POTCAR order and species-indexed INCAR arrays. When an upstream VASP input must be preserved, stage `scripts/vasp/compare_incar_parameters.sh` and run it with only the Spec-declared exception keys. Any mismatch stops before review.

For layered magnetic work, compare the prepared index-order `MAGMOM` assignment with the Spec's approved atom-index, species, fractional-z, z-layer-rank, and intended-moment table. A changed order or value blocks execution and returns to `$calc-to-spec`; a small total moment or successful downstream Run is not evidence of the intended order.

PBS receives the exact Run directory as `PBS_O_WORKDIR`, reads only its immutable `inputs/`, copies named approved bytes into its private `outputs/`, and records backend command output under `logs/`. It refuses any prior output rather than deleting products or guessing another Run.
