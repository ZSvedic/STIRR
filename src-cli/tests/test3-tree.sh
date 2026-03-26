#!/usr/bin/env bash
# #Human
# Checks that `stirr-tree.py` correctly traverses a real directory structure.

source "$(dirname "$0")/base-testing.sh" "$0"

./stirr-tree.py tests/test-dir > "$LOG" 2>&1

rg -q "test-dir" "$LOG"
rg -q "test-hashtags.txt" "$LOG"
rg -qi "#FooBar" "$LOG"
echo Pass
