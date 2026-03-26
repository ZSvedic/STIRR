#!/usr/bin/env bash
# #Human
# Runs current iteration of the implementation spec through Codex.

set -euo pipefail

codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Implement the spec." \
  2>&1 | tee codex-output.log