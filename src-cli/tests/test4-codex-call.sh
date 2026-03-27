#!/usr/bin/env bash
# #Human
# Calls stirr-tree.py on test-dir and validates output via Codex call.

source "$(dirname "$0")/base-testing.sh" "$0"

timeout 50 ./stirr-check.sh codex tests/test-dir > "$LOG" 2>&1

rg -q "test-dir" "$LOG"
rg -q "test-hashtags.txt" "$LOG"
rg -qi "foo" "$LOG"
echo Pass
