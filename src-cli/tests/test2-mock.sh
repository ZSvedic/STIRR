#!/usr/bin/env bash
# #Human
set -euo pipefail

cd "$(dirname "$0")/.."
LOG="tests/test2-mock.log"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
trap 's=$?; echo "FAIL: ${BASH_COMMAND} (exit $s)"; exit $s' ERR

mkdir -p "$TMP/sub" "$TMP/.hidden"
printf '#Foo #foo #Bar\n' > "$TMP/a.md"
printf '#foo-bar #Foo\n' > "$TMP/sub/b.txt"
printf '#NOPE\n' > "$TMP/.hidden/skip.md"
printf '\x00\x01\x02' > "$TMP/sub/bin.dat"

./stirr-tree.py "$TMP" > "$LOG" 2>&1

rg -q "a.md .*#Foo \(2#foo 1#bar\)" "$LOG"
rg -q "b.txt .*#foo-bar \(1#foo-bar 1#foo\)" "$LOG"
rg -q "3#foo 1#bar 1#foo-bar|3#foo 1#foo-bar 1#bar" "$LOG"
! rg -q "skip.md|bin.dat" "$LOG"
echo Pass
