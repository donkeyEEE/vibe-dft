#!/usr/bin/env bash
# Package only lightweight magnetic results for synchronization or archival.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SOURCE_DIR DEST_DIR" >&2
    exit 1
fi

SOURCE_DIR=$1
DEST_DIR=$2
if [ ! -d "$SOURCE_DIR" ]; then
    echo "SOURCE_DIR is not a directory: $SOURCE_DIR" >&2
    exit 1
fi

mkdir -p "$DEST_DIR" || exit 1
SOURCE_DIR=$(cd "$SOURCE_DIR" && pwd -P) || exit 1
DEST_DIR=$(cd "$DEST_DIR" && pwd -P) || exit 1

if [ "$SOURCE_DIR" = "$DEST_DIR" ]; then
    echo "DEST_DIR must not be SOURCE_DIR: $DEST_DIR" >&2
    exit 1
fi

: > "$DEST_DIR/manifest.included"
: > "$DEST_DIR/manifest.skipped"

while IFS= read -r -d '' file; do
    relative=${file#"$SOURCE_DIR"/}
    name=${file##*/}
    include=false

    case "$name" in
        *_hr.dat|*.h5|*.hdf5|*.hdf|WAVECAR|CHGCAR|CHG|vasprun.xml|vampire.*)
            ;;
        exchange.out|JvsR*|M_vs_T*|Tc*|susceptibility*|heat_capacity*|*.png|*.pdf)
            include=true
            ;;
    esac

    if [ "$include" = true ]; then
        mkdir -p "$DEST_DIR/$(dirname "$relative")" || exit 1
        cp -p "$file" "$DEST_DIR/$relative" || exit 1
        printf '%s\n' "$relative" >> "$DEST_DIR/manifest.included"
    else
        printf '%s\n' "$relative" >> "$DEST_DIR/manifest.skipped"
    fi
done < <(
    case "$DEST_DIR/" in
        "$SOURCE_DIR/"*) find "$SOURCE_DIR" -path "$DEST_DIR" -prune -o -type f -print0 ;;
        *) find "$SOURCE_DIR" -type f -print0 ;;
    esac
)
