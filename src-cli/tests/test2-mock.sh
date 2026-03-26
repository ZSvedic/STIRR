#!/usr/bin/env bash
# #Human
# Checks that `stirr-tree.py` correctly traverses a mock directory structure.

source "$(dirname "$0")/base-testing.sh" "$0"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/sub" "$TMP/.hidden"
printf '#Foo #foo #Bar\n' > "$TMP/a.md"
printf '#foo-bar #Foo\n' > "$TMP/sub/b.txt"
printf '#NOPE\n' > "$TMP/.hidden/skip.md"
printf '\x00\x01\x02' > "$TMP/sub/bin.dat"

./stirr-tree.py "$TMP" > "$LOG" 2>&1

rg -q "a.md 0.01 KB \(1 LOC 6 LTOK\) #Foo \(2#foo 1#bar\)" "$LOG"
rg -q "b.txt 0.01 KB \(1 LOC 6 LTOK\) .*#foo-bar \(1#foo-bar 1#foo\)" "$LOG"
rg -q "3#foo 1#bar 1#foo-bar|3#foo 1#foo-bar 1#bar" "$LOG"
! rg -q "skip.md|bin.dat" "$LOG"
echo Pass
