#!/usr/bin/env bash
# #Human
set -euo pipefail

trap 'echo FAIL; exit 1' ERR

cd "$(dirname "$0")/.."
./stirr.py --dry-run tests/test-dir > tests/test4-dry-run.log 2>&1

rg -q "test-dir" tests/test4-dry-run.log
rg -q "test-hashtags.txt" tests/test4-dry-run.log
rg -qi "#FooBar" tests/test4-dry-run.log
echo Pass
