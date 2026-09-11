# VAMPIRE execution

Use `assets/templates/vampire/{cluster-env.sh.template,run.pbs.template}` and stage the exact `scripts/vampire/plot.py`. The prepared input must name `output:temperature` and `output:mean-magnetisation-length`; malformed or missing columns block before review and the plot helper rejects malformed output.

PBS verifies the reviewed model checksum manifest, copies only the named input/model/helper files to private outputs, records source and copy checksums, executes the configured VAMPIRE binary, and requires nonempty `output` and `M_vs_T.png`. It refuses prior outputs and never alters `inputs/`.

Use `scripts/vampire/pack_magnetic_results.sh` only for lightweight results. It excludes VAMPIRE models, Wannier Hamiltonians, HDF5, `WAVECAR`, `CHGCAR`, `CHG`, and `vasprun.xml`, and writes included/skipped manifests.
