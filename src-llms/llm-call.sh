#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: llm-call <codex|claude> \"question\""
  exit 1
}

[ "$#" -ge 2 ] || usage

AGENT="$1"
PROMPT="$2"

case "$AGENT" in
  codex)
    echo "=== Codex: "
    codex -a never -s read-only exec "$PROMPT"
    ;;
  claude)
    echo "=== Claude: "
    claude -p "$PROMPT" --tools ""
    ;;
  *)
    usage
    ;;
esac