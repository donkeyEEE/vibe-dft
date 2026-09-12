#!/bin/bash

STAGE="${1:-}"
PROTOTYPE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
BACKEND_ROOT="$PROTOTYPE_ROOT/references/backends/vasp"

case "$STAGE" in
    scf) FILES="common.md scf.md" ;;
    band) FILES="common.md band.md handoff.md" ;;
    *) echo "usage: $0 {scf|band}" >&2; exit 1 ;;
esac

for name in $FILES; do
    [ -s "$BACKEND_ROOT/$name" ] || { echo "missing backend knowledge: $name" >&2; exit 1; }
    echo "$BACKEND_ROOT/$name"
done
