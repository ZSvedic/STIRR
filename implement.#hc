#!/usr/bin/env bash
set -euo pipefail

codex exec \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  "Implement #STIRR spec based on the given rules." \
  2>&1 | tee ai-output.log