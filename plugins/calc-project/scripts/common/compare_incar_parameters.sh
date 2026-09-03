#!/bin/bash
# Compare upstream and prepared downstream INCAR settings before submission.
# Usage: compare_incar_parameters.sh <upstream-INCAR> <downstream-INCAR> [exceptions]
# Exceptions are a whitespace- or comma-separated list of compared key names.

UPSTREAM_INCAR="$1"
DOWNSTREAM_INCAR="$2"
EXCEPTIONS="${3:-}"

[ -n "$UPSTREAM_INCAR" ] || { echo "missing upstream INCAR path" >&2; exit 1; }
[ -n "$DOWNSTREAM_INCAR" ] || { echo "missing downstream INCAR path" >&2; exit 1; }
[ -f "$UPSTREAM_INCAR" ] || { echo "missing upstream INCAR: $UPSTREAM_INCAR" >&2; exit 1; }
[ -f "$DOWNSTREAM_INCAR" ] || { echo "missing downstream INCAR: $DOWNSTREAM_INCAR" >&2; exit 1; }

COMPARE_KEYS="ISPIN ISYM LDAU LDAUTYPE LDAUL LDAUU LDAUJ LDAUPRINT MAGMOM ENCUT NBANDS ISMEAR SIGMA EDIFF EDIFFG NELM"

normalise_value() {
    awk '
        {
            gsub(/[[:space:]]/, "")
            printf "%s", toupper($0)
        }
    '
}

read_incar_value() {
    requested_key="$1"
    incar_path="$2"
    awk -v requested_key="$requested_key" '
        {
            line = $0
            sub(/[!#].*$/, "", line)
            if (line !~ /=/) {
                next
            }
            key = line
            sub(/=.*/, "", key)
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", key)
            if (toupper(key) != requested_key) {
                next
            }
            value = line
            sub(/^[^=]*=/, "", value)
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            found = value
        }
        END {
            if (found != "") {
                print found
            }
        }
    ' "$incar_path" | normalise_value
}

is_exception() {
    requested_key="$1"
    normalised_exceptions="$(printf '%s' "$EXCEPTIONS" | tr ',' ' ' | tr '[:lower:]' '[:upper:]')"
    for exception_key in $normalised_exceptions; do
        [ "$exception_key" = "$requested_key" ] && return 0
    done
    return 1
}

for exception_key in $(printf '%s' "$EXCEPTIONS" | tr ',' ' ' | tr '[:lower:]' '[:upper:]'); do
    case " $COMPARE_KEYS " in
        *" $exception_key "*) ;;
        *) echo "unknown INCAR exception key: $exception_key" >&2; exit 1 ;;
    esac
done

failed=0
for key in $COMPARE_KEYS; do
    is_exception "$key" && continue

    upstream_value="$(read_incar_value "$key" "$UPSTREAM_INCAR")"
    downstream_value="$(read_incar_value "$key" "$DOWNSTREAM_INCAR")"
    [ "$upstream_value" = "$downstream_value" ] && continue

    echo "INCAR mismatch for $key: upstream='${upstream_value:-<unset>}' downstream='${downstream_value:-<unset>}'" >&2
    failed=1
done

[ "$failed" -eq 0 ] || exit 1
