#!/usr/bin/env bash
# #AI
# Checks that `stirr-tree.py` correctly traverses a real directory structure.

source "$(dirname "$0")/base-testing.sh" "$0"

./stirr-tree.py tests/test-dir > "$LOG" 2>&1

EXPECTED=$(cat <<'EOF'
FILE TREE:
. 0.29KB
  #AI.#Test 0.00KB
  test-hashtags.txt 0.29KB #human (4#foo 3#foobar 2#bar 1#human 1#foo-bar)
TAG TOTALS:
4#foo 3#foobar 2#bar 1#foo-bar 1#human
EOF
)

echo Pass