# Wannier90 execution

Use `assets/templates/wannier90/{cluster-env.sh.template,run.pbs.template,wannier-run.env.template}`. Before review, copy the exact accepted pre-run `.amn`, `.mmn`, `.eig`, and `.win` files for both spins, the band Run's two nonempty range files, two reformatted bands and `DOSCAR`, and the two owner plot helpers. Each named `copy_immutable SOURCE DESTINATION` call ends with `|| return 1`; no wildcard or directory guessing is allowed.

Render all eight separate up/down outer and frozen window values from the approved Spec into `wannier-run.env`. Changed, shared, missing, or reordered values block and return to `$calc-to-spec`; plotting bounds are not window values. The review checks `NUM_WANN`, projections, maximum frozen-state counts, and the approved window evidence before submission.

Require nonempty spin-resolved `.wout`, `_hr.dat`, `_centres.xyz`, `_band.dat`, and VASP-versus-Wannier fit plots. The PBS template preserves the immutable interface inputs, changes window keys only in private output copies, and runs both spin seeds. A successful executable alone does not prove physical adequacy.
