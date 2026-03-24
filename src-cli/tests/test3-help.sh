#!/usr/bin/env bash
# #Human
set -euo pipefail

trap 'echo FAIL; exit 1' ERR

cd "$(dirname "$0")/.."

{
  ./stirr.py -h
  ./stirr.py --help
  ./stirr.py
} > tests/test3-help.log 2>&1

rg -q "USAGE:" tests/test3-help.log
echo Pass
