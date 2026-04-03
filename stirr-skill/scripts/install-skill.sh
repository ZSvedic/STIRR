#!/usr/bin/env bash
# #Human
# Humans: Run this script to install stirr-skill for all CLI agents via symlinks. 
# Agents: If you are reading this, the skill is probably already installed! 
#         But, you can run it again if you want to update symlinks or add skill to a new agent.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SOURCE="$SCRIPT_DIR/../stirr-skill"

[ -d "$SKILL_SOURCE" ] || {
  echo "Missing skill dir: $SKILL_SOURCE" >&2
  exit 1
}

SKILL_NAME="stirr-skill"
HOME_DIR="${HOME:-/root}"

TARGETS=(
  "$HOME_DIR/.copilot/skills"
  "$HOME_DIR/.claude/skills"
  "$HOME_DIR/.codex/skills"
  "$HOME_DIR/.cursor/skills"
)

for target_dir in "${TARGETS[@]}"; do
  mkdir -p "$target_dir"
  ln -sfn "$SKILL_SOURCE" "$target_dir/$SKILL_NAME"
  echo "Linked $target_dir/$SKILL_NAME -> $SKILL_SOURCE"
done
