#!/usr/bin/env bash
# #Human

usage() {
  printf "USAGE: %s <codex|claude|copilot|cursor>\n\n" "$0"
  printf "Runs current iteration of the implementation spec through a selected agent.\n"
  exit 1
}

set -euo pipefail # Exit on error, undefined variable, or pipe failure.

[ "$#" -eq 1 ] || usage # If no arguments, show usage.

PROVIDER="$1"
PROMPT="Implement the spec."

# Calls the appropriate agent and logs output.
case "$PROVIDER" in
  codex)
    codex exec \
      --dangerously-bypass-approvals-and-sandbox \
      --skip-git-repo-check \
      "$PROMPT" \
      2>&1 | tee codex-output.log
    ;;
  claude)
    claude -p --verbose -debug \
      --permission-mode bypassPermissions \
      "$PROMPT" \
      2>&1 | tee claude-output.log
    ;;
  copilot)
    copilot -p "$PROMPT" \
      --allow-all-tools --allow-all-paths --allow-all-urls \
      2>&1 | tee copilot-output.log
    ;;
  cursor)
    agent --print --force --trust "$PROMPT" \
      2>&1 | tee cursor-output.log
    ;;
  *)
    usage
    ;;
esac
