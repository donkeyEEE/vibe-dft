#!/bin/bash

STAGE="${1:-}"
INPUTS_DIR="${2:-}"
RUN_DIR="${3:-}"

case "$STAGE" in
    scf) REQUIRED_INPUTS="INCAR POSCAR POTCAR KPOINTS"; REQUIRED_OUTPUTS="OUTCAR CHGCAR" ;;
    band) REQUIRED_INPUTS="INCAR POSCAR POTCAR KPOINTS"; REQUIRED_OUTPUTS="CHGCAR OUTCAR BAND.dat" ;;
    *) echo "usage: $0 {scf|band} INPUTS_DIR RUN_DIR" >&2; exit 1 ;;
esac

for name in $REQUIRED_INPUTS; do
    [ -s "$INPUTS_DIR/$name" ] || { echo "missing $STAGE input: $name" >&2; exit 1; }
done
for name in $REQUIRED_OUTPUTS; do
    [ -s "$RUN_DIR/$name" ] || { echo "missing $STAGE output: $name" >&2; exit 1; }
done
echo "$STAGE stage valid"
