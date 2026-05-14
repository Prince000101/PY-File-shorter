#!/usr/bin/env bash
set -euo pipefail

button() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: button <input>"
        return 1
    fi

    echo "Processing button: $input"
    # Validate
    if [[ ! -f "$input" ]]; then
        echo "Error: File not found" >&2
        return 1
    fi

    # Process
    local result=$(sanitize "$input")
    echo "$result"
}

main() {
    button "$@"
}

main "$@"
