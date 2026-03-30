#!/usr/bin/env bash
# #Human

usage() { 
    echo -e "USAGE: $0 -a | -c CATEGORY | -n NAME\n"
    echo "  -a: Runs all tests"
    echo "  -c CATEGORY: Runs tests in the CATEGORY."
    echo "  -n NAME: Runs the test with the NAME."
    exit "${1:-1}" # Default exit code 1 for error, 0 for help.
}

set -uo pipefail # Exit on undefined variable or pipe failure.

cd "$(dirname "$0")" # Change to the tests directory.

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
  printf "Running %s... \t\t" "$NAME"
  CMD="./../$CMD"
  if eval "$CMD" > "$NAME.log" 2>&1 && diff -uw "$NAME.log" "$NAME.expected.log" > /dev/null; then
    echo Pass
  else
    echo "FAIL: $CMD"
    RET=1
  fi
done < tests.csv # Read tests from CSV.
exit $RET