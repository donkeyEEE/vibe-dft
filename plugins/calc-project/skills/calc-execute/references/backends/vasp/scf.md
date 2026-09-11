# VASP SCF execution

Use `assets/templates/vasp/scf/run.pbs.template` and render `__VASP_CHARGE_HANDOFF__` as `none`. The preparation body creates only the Spec-approved POTCAR or KPOINTS described in `common.md`; it does not defer VASPKIT input generation to PBS. The validation body checks every named input, the rendered cluster environment, `mpirun`, and the configured VASP executable, with each command propagating failure by `|| return 1`.

Require a nonempty `OUTCAR` and the Spec's convergence and handoff outputs. Keep the original final `E-fermi` in `OUTCAR`; downstream TB2J uses that declared convention rather than an inferred Fermi value.
