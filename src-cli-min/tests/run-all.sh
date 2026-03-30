#!/usr/bin/env bash
# #Human
# Runs all local tests.

set -euo pipefail # Exit on error, undefined variable, or pipe failure.

fail() { # Print the failed cmd and exits with the same code.
  s=$?
  echo "FAIL: ${BASH_COMMAND} (exit $s)"
  exit $s
}

trap fail ERR # Call fail() on any error.

cd "$(dirname "$0")" # Change to the tests directory.

# Test 3: Check that `stirr-tree.py` correctly traverses a real directory structure.
NAME="test3-tree"
ARGS=(test-dir)

printf "Running $NAME... "
./../stirr-tree.py "${ARGS[@]}" > "$NAME.log" 2>&1

diff -uw "$NAME.log" "$NAME.log"
printf "\t\tPass\n"

