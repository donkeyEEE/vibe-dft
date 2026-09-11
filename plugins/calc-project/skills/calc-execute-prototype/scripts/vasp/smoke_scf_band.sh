#!/bin/bash
set -eu

PROTOTYPE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
WORK_ROOT="$(mktemp -d)"
trap 'rm -rf -- "$WORK_ROOT"' EXIT

for stage in scf band; do
    mkdir -p "$WORK_ROOT/$stage/inputs" "$WORK_ROOT/$stage/run-001"
    sed -e 's/__SYSTEM__/demo/' -e 's/__ENCUT__/520/' -e 's/__ISPIN__/2/' \
        "$PROTOTYPE_ROOT/assets/templates/vasp/$stage/INCAR.template" \
        > "$WORK_ROOT/$stage/inputs/INCAR"
    for name in POSCAR POTCAR KPOINTS; do
        printf 'representative %s\n' "$name" > "$WORK_ROOT/$stage/inputs/$name"
    done
done

printf 'SCF complete\n' > "$WORK_ROOT/scf/run-001/OUTCAR"
printf 'representative charge density\n' > "$WORK_ROOT/scf/run-001/CHGCAR"
bash "$PROTOTYPE_ROOT/scripts/vasp/validate_stage.sh" scf \
    "$WORK_ROOT/scf/inputs" "$WORK_ROOT/scf/run-001"

[ ! -e "$WORK_ROOT/band/run-001/CHGCAR" ] || exit 1
cp "$WORK_ROOT/scf/run-001/CHGCAR" "$WORK_ROOT/band/run-001/CHGCAR"
printf 'Band complete\n' > "$WORK_ROOT/band/run-001/OUTCAR"
printf 'representative band data\n' > "$WORK_ROOT/band/run-001/BAND.dat"
bash "$PROTOTYPE_ROOT/scripts/vasp/validate_stage.sh" band \
    "$WORK_ROOT/band/inputs" "$WORK_ROOT/band/run-001"

echo "SCF to band staging and handoff smoke passed"
