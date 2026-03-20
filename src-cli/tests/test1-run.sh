#!/usr/bin/env bash
# #Human
set -euo pipefail

trap 'echo FAIL; exit 1' ERR

cd "$(dirname "$0")/.."
./stirr > tests/test1-run.log 2>&1
echo Pass
