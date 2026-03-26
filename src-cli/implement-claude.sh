#!/usr/bin/env bash
# #Human
# Runs current iteration of the implementation spec through Claude.

set -euo pipefail

claude -p --verbose -debug \
  --permission-mode bypassPermissions \
  "Implement the spec." \
  2>&1 | tee claude-output.log