#!/bin/bash

set -u

usage() {
    echo "usage: $0 PROFILE HOST LABEL REMOTE_COMMAND" >&2
    exit 2
}

[ "$#" -eq 4 ] || usage

profile_file=$1
host=$2
label=$3
remote_command=$4

[ -n "$profile_file" ] && [ -n "$host" ] && [ -n "$label" ] && [ -n "$remote_command" ] || usage
case "$host" in
    -*) echo "host must not begin with an option marker: $host" >&2; exit 2 ;;
esac
[ -f "$profile_file" ] || { echo "missing profile: $profile_file" >&2; exit 1; }

start_count=$(grep -c '^<!-- cluster-profile-status:start -->$' "$profile_file")
end_count=$(grep -c '^<!-- cluster-profile-status:end -->$' "$profile_file")
[ "$start_count" -eq 1 ] && [ "$end_count" -eq 1 ] || {
    echo "profile must contain one existing cluster-profile-status marker block" >&2
    exit 1
}
start_line=$(grep -n '^<!-- cluster-profile-status:start -->$' "$profile_file" | cut -d: -f1)
end_line=$(grep -n '^<!-- cluster-profile-status:end -->$' "$profile_file" | cut -d: -f1)
[ "$start_line" -lt "$end_line" ] || {
    echo "cluster-profile-status start marker must precede end marker" >&2
    exit 1
}

probe_output_file=$(mktemp) || exit 1
replacement_file=$(mktemp) || { rm -f "$probe_output_file"; exit 1; }
existing_rows_file=$(mktemp) || { rm -f "$probe_output_file" "$replacement_file"; exit 1; }
updated_file=$(mktemp) || { rm -f "$probe_output_file" "$replacement_file" "$existing_rows_file"; exit 1; }
trap 'rm -f "$probe_output_file" "$replacement_file" "$existing_rows_file" "$updated_file"' EXIT

if ssh -- "$host" "$remote_command" >"$probe_output_file" 2>&1; then
    probe_status=verified
    exit_status=0
else
    probe_status=unavailable
    exit_status=1
fi

output_summary=$(tr '\n' ' ' < "$probe_output_file" | sed 's/[[:space:]][[:space:]]*/ /g; s/^ //; s/ $//')
[ -n "$output_summary" ] || output_summary="(no output)"
if [ "$(printf '%s' "$output_summary" | LC_ALL=C wc -c)" -gt 200 ]; then
    output_summary=$(printf '%.200s... [truncated]' "$output_summary")
fi
output_summary=$(printf '%s' "$output_summary" | sed 's/|/\\|/g')
safe_label=$(printf '%s' "$label" | tr '\n' ' ' | sed 's/|/\\|/g')
safe_command=$(printf '%s' "$remote_command" | tr '\n' ' ' | sed 's/|/\\|/g')

awk -v component="| $safe_label |" '
    /^<!-- cluster-profile-status:start -->$/ { inside = 1; next }
    /^<!-- cluster-profile-status:end -->$/ { inside = 0; next }
    inside && /^\| / && $0 !~ /^\| Component \|/ && $0 !~ /^\|---/ && index($0, component) != 1 { print }
' "$profile_file" > "$existing_rows_file" || exit 1

{
    echo '<!-- cluster-profile-status:start -->'
    echo '## Verification status'
    echo
    echo '| Component | Status | Command | Output summary |'
    echo '|---|---|---|---|'
    cat "$existing_rows_file"
    printf '| %s | %s | `%s` | %s |\n' "$safe_label" "$probe_status" "$safe_command" "$output_summary"
    echo '<!-- cluster-profile-status:end -->'
} > "$replacement_file"

awk -v replacement="$replacement_file" '
    /^<!-- cluster-profile-status:start -->$/ {
        while ((getline line < replacement) > 0) print line
        close(replacement)
        skipping = 1
        next
    }
    /^<!-- cluster-profile-status:end -->$/ && skipping { skipping = 0; next }
    !skipping { print }
' "$profile_file" > "$updated_file" || exit 1

mv "$updated_file" "$profile_file" || exit 1
echo "Recorded $probe_status evidence for $label in $profile_file"
exit "$exit_status"
