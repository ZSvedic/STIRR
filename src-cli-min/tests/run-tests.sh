#!/usr/bin/env bash
# #Human
# A simple test runner. Reads tests from tests.csv, runs them, and compares .log to .correct.

usage() { 
    printf "USAGE: %s -a | -c CATEGORY | -n NAME\n\n" "$0"
    printf "  -a \t\tRuns all tests\n"
    printf "  -c CATEGORY \tRuns all tests in the CATEGORY.\n"
    printf "  -n NAME \tRuns the NAME test.\n"
    exit "${1:-1}" # Default exit code 1 for error, 0 for help.
}

set -uo pipefail # Exit on undefined variable or pipe failure.

cd "$(dirname "$0")" # Change to the tests dir.

[ $# -gt 0 ] || usage # If no arguments, show usage.

case "${1-}" in # Parse arguments.
  -h|--help) usage 0 ;;
  -a) MODE=all; VAL=all ;;
  -c) [ $# -eq 2 ] || usage; MODE=c; VAL="$2" ;;
  -n) [ $# -eq 2 ] || usage; MODE=n; VAL="$2" ;;
  *) usage ;;
esac

RET=0
while IFS=, read -r NAME CATEGORY CMD; do # Read each row.
  [ "$NAME" = Name ] && continue # Skip header row.
  case "$MODE" in
    all) ;;
    c) [ "$VAL" = all ] || [ "$CATEGORY" = "$VAL" ] || continue ;;
    n) [ "$NAME" = "$VAL" ] || continue ;;
  esac
  printf "Running %s...\t" "$NAME"
  eval "./../$CMD" > "$NAME.log" 2>&1 # Run CMD with prefix and suffix, capture output.
  if DIFF_OUT=$(diff -uw -U0 "$NAME.log" "$NAME.correct" 2>&1); then
    printf "Pass\n"
  else
    printf "FAIL\n$DIFF_OUT\n\n"
    RET=1
  fi
done < tests.csv # Read tests from CSV.
exit $RET