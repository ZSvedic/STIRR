#!/usr/bin/env bash
# #Human
# Calls stirr-tree.py on test-dir and validates output via Codex LLM.

source "$(dirname "$0")/base-testing.sh" "$0"

STIRR_OUT=$(./stirr-tree.py tests/test-dir)

timeout 20 codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Analyze this stirr-tree output and list what files and tags you see: $STIRR_OUT" \
  > "$LOG" 2>&1

rg -q "test-dir" "$LOG"
rg -q "test-hashtags.txt" "$LOG"
rg -qi "foo" "$LOG"
echo Pass
