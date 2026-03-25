#!/usr/bin/env bash
# #Human
set -euo pipefail

cd "$(dirname "$0")/.."
LOG="tests/test2-mock.log"
trap 's=$?; echo "FAIL: ${BASH_COMMAND} (exit $s)"; exit $s' ERR

./stirr.py > "$LOG" 2>&1

echo Pass
