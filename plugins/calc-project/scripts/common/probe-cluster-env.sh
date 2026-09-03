#!/bin/bash
# Run manually on the cluster login node after filling scripts/cluster-env.sh.
# Example: bash scripts/probe-cluster-env.sh vasp wannier90

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ENV_FILE="$SCRIPT_DIR/cluster-env.sh"

[ -f "$ENV_FILE" ] || { echo "missing $ENV_FILE" >&2; exit 1; }
source "$ENV_FILE" || exit 1

require_command() {
    command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 1; }
}

require_executable() {
    [ -n "$2" ] && [ -x "$2" ] || { echo "invalid $1: ${2:-unset}" >&2; exit 1; }
}

[ "$#" -gt 0 ] || { echo "usage: $0 <vasp|wannier90|tb2j|vampire> [...]" >&2; exit 2; }

for method in "$@"; do
    case "$method" in
        vasp)
            require_command mpirun
            require_executable VASP_EXE "${VASP_EXE:-}"
            require_executable VASPKIT_EXE "${VASPKIT_EXE:-}"
            ;;
        wannier90)
            require_command "${WANNIER90_MPI_LAUNCHER:-mpirun}"
            require_executable WANNIER90_EXE "${WANNIER90_EXE:-}"
            ;;
        tb2j)
            require_command conda
            [ -n "${TB2J_CONDA_ENV:-}" ] || { echo "unset TB2J_CONDA_ENV" >&2; exit 1; }
            conda run -n "$TB2J_CONDA_ENV" wann2J.py --help >/dev/null || exit 1
            ;;
        vampire)
            require_executable VAMPIRE_EXE "${VAMPIRE_EXE:-}"
            ;;
        *)
            echo "unknown method: $method" >&2
            exit 2
            ;;
    esac
    echo "verified: $method"
done
