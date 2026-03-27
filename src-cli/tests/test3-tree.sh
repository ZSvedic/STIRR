#!/usr/bin/env bash
# #AI
# Checks that `stirr-tree.py` correctly traverses a real directory structure.

source "$(dirname "$0")/base-testing.sh" "$0"

./stirr-tree.py tests/test-dir > "$LOG" 2>&1

EXPECTED=$(cat <<'TXT'
== FILE TREE as NAME SIZE (LOC LTOK) FirstTag (Top 3 tags) ===
test-dir/ 0.29 KB (12 LOC 59 LTOK)
  #AI.#Test 0.00 KB (0 LOC 0 LTOK)
  test-hashtags.txt 0.29 KB (12 LOC 59 LTOK) #human (4#foo 3#foobar 2#bar)
== TAG TOTALS ===
4#foo 3#foobar 2#bar 1#foo-bar 1#human
TXT
)

ACTUAL="$(cat "$LOG")"
[[ "$ACTUAL" == "$EXPECTED" ]]
echo Pass
