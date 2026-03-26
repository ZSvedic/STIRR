#!/usr/bin/env bash
# #Human
# Checks that `stirr-tree.py` shows help when run with `-h`, `--help`, or no arguments.

source "$(dirname "$0")/base-testing.sh" "$0"

{
  ./stirr-tree.py -h
  ./stirr-tree.py --help
  ./stirr-tree.py
} > "$LOG" 2>&1

rg -q "USAGE:" "$LOG"
echo Pass
