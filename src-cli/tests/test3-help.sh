#!/usr/bin/env bash
# #Human
set -euo pipefail

cd "$(dirname "$0")/.."
LOG="tests/test3-help.log"
trap 's=$?; echo "FAIL: ${BASH_COMMAND} (exit $s)"; exit $s' ERR

{
  ./stirr.py -h
  ./stirr.py --help
  ./stirr.py
} > "$LOG" 2>&1

rg -q "USAGE:" "$LOG"
echo Pass
