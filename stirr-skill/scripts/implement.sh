#!/usr/bin/env bash
# #Human

usage() {
  printf "USAGE: %s <codex|claude|copilot|cursor>\n\n" "$0"
  printf "Runs current iteration of the implementation spec through a selected agent.\n"
  exit 1
}

set -euo pipefail # Exit on error, undefined variable, or pipe failure.

[ "$#" -eq 1 ] || usage # If no arguments, show usage.

PROMPT="Implement the spec."

case "$1" in
  codex)   AGENT=codex;   ARGS=(exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check "$PROMPT") ;;
  claude)  AGENT=claude;  ARGS=(-p --verbose -debug --permission-mode bypassPermissions "$PROMPT") ;;
  copilot) AGENT=copilot; ARGS=(-p "$PROMPT" --allow-all-tools --allow-all-paths --allow-all-urls) ;;
  cursor)  AGENT=agent;   ARGS=(--print --force --trust "$PROMPT") ;;
  *) usage ;;
esac

# Calls the appropriate agent and logs output.
"$AGENT" "${ARGS[@]}" 2>&1 | tee "$AGENT.log.md"
