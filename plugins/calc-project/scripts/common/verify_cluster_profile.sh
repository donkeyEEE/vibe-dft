#!/bin/bash
# Verify the bundled mu01 software profile without blocking project creation.
# Usage: bash verify_cluster_profile.sh <project-root/software-profiles.md> <ssh-host>

PROFILE_FILE="$1"
HOST="$2"

[ -n "$PROFILE_FILE" ] && [ -n "$HOST" ] || {
    echo "usage: $0 <cluster-software-profiles.md> <ssh-host>" >&2
    exit 2
}
[ -f "$PROFILE_FILE" ] || { echo "missing profile: $PROFILE_FILE" >&2; exit 1; }

CHECK_DATE=$(date +%F)
STATUS_FILE=$(mktemp) || exit 1

check_remote() {
    name="$1"
    command="$2"
    if ssh "$HOST" "source /etc/profile && $command" >/dev/null 2>&1; then
        printf '| %s | verified | %s | `%s` |\n' "$name" "$CHECK_DATE" "$command" >> "$STATUS_FILE"
    else
        printf '| %s | unverified/unavailable | %s | `%s` |\n' "$name" "$CHECK_DATE" "$command" >> "$STATUS_FILE"
    fi
}

check_remote 'PBS / Torque' 'command -v qsub && command -v qstat'
check_remote 'VASP standard' 'test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_std'
check_remote 'VASP noncollinear' 'test -x /data1/yuzheli-alkemie/01Soft/vasp.x/vasp.6.5.0/bin/vasp_ncl'
check_remote 'VASPKIT' 'test -x /data1/yuzheli-alkemie/01Soft/vaspkit.1.3.5/bin/vaspkit'
check_remote 'Wannier90' 'test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/wannier90.x'
check_remote 'postw90' 'test -x /data1/yuzheli-alkemie/01Soft/wannier90-3.1.0/postw90.x'
check_remote 'VAMPIRE' 'test -x /data1/yuzheli-alkemie/01Soft/vampire/linux/vampire'
check_remote 'Hefei-NAMD' 'test -x /data1/yuzheli-alkemie/07soft/Hefei-NAMD/src/namd'
check_remote 'NAMDwithSOC' 'test -x /data1/yuzheli-alkemie/07soft/NAMDwithSOC/src/namd_soc'
check_remote 'TB2J' 'source ~/.bashrc && conda run -n tb2j wann2J.py --help >/dev/null'

TMP_FILE=$(mktemp) || exit 1
awk '/<!-- cluster-profile-status:start -->/ {skip=1; next} /<!-- cluster-profile-status:end -->/ {skip=0; next} !skip {print}' "$PROFILE_FILE" > "$TMP_FILE" || exit 1
{
    printf '\n<!-- cluster-profile-status:start -->\n'
    printf '## Verification status\n\n'
    printf '| Component | Status | Checked | Command |\n'
    printf '|---|---|---|---|\n'
    cat "$STATUS_FILE"
    printf '<!-- cluster-profile-status:end -->\n'
} >> "$TMP_FILE"
mv "$TMP_FILE" "$PROFILE_FILE" || exit 1
rm -f "$STATUS_FILE"
echo "Recorded cluster verification status in $PROFILE_FILE"
