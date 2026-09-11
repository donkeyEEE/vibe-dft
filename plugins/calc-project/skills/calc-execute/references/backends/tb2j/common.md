# TB2J execution

Use `assets/templates/tb2j/{cluster-env.sh.template,run.pbs.template}`. Before review, copy exactly `POSCAR`, the accepted SCF `OUTCAR`, both approved `wannier90.*_hr.dat`, and both `wannier90.*_centres.xyz` files into the new Run's inputs with failure-propagating `copy_immutable` calls.

Render the Spec-declared magnetic elements/orbitals, cutoff, energy range, spin prefixes, Fermi convention, and TB2J k mesh. The template reads the final `E-fermi` from the declared SCF OUTCAR and passes that value plus the separately approved k mesh to `wann2J.py`; it never derives the mesh from Wannier `mp_grid`.

Require nonempty `TB2J_results/exchange.out`, `TB2J_results/Vampire/vampire.UCF`, `vampire.mat`, and `input`. A missing spin handoff or VAMPIRE product stops the branch.
