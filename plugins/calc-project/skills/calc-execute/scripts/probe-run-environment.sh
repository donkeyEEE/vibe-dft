#!/bin/bash

HOST="${1:-}"
REMOTE_COMMAND="${2:-}"

if [ "$#" -ne 2 ] || [ -z "$HOST" ] || [ -z "$REMOTE_COMMAND" ]; then
    echo "usage: $0 HOST REMOTE_COMMAND" >&2
    exit 2
fi

exec ssh -- "$HOST" "$REMOTE_COMMAND"
