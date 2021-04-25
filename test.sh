#!/usr/bin/env bash
set -eu -o pipefail

if ! [ "$(cat quine.sh)" = "$(./quine.sh)" ]; then
    echo "Wrong" >&2
    diff quine.sh <(./quine.sh)
    exit 1
fi

echo OK

