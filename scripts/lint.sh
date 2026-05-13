#!/usr/bin/env bash
set -euo pipefail

profile() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: profile <input>"
        return 1
    fi

    echo "Processing profile: $input"
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
    profile "$@"
}

main "$@"


#!/usr/bin/env bash
set -euo pipefail

repo() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        echo "Usage: repo <input>"
        return 1
    fi

    echo "Processing repo: $input"
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
    repo "$@"
}

main "$@"
