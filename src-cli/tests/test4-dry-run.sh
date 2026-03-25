#!/usr/bin/env bash
# #Human
set -euo pipefail

cd "$(dirname "$0")/.."
LOG="tests/test4-dry-run.log"
trap 's=$?; echo "FAIL: ${BASH_COMMAND} (exit $s)"; exit $s' ERR

./stirr.py --dry-run tests/test-dir > "$LOG" 2>&1

rg -q "test-dir" "$LOG"
rg -q "test-hashtags.txt" "$LOG"
rg -qi "#FooBar" "$LOG"
echo Pass
