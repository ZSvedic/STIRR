#!/usr/bin/env bash
# #Human
# This script:
# - Calls `stirr-tree.py` on provided paths, pipes output to a string.
# - Constructs a validation prompt, including the tree output.
# - Calls either Codex or Claude with a given prompt, no tools allowed. 
set -euo pipefail

usage() {
  echo "Usage: stirr-check.sh <codex|claude> PATH1 [PATH2 ...]"
  exit 1
}

[ "$#" -ge 2 ] || usage

AGENT="$1"
shift
PATHS=("$@")

TREE_OUTPUT=$(stirr-tree.py "${PATHS[@]}")

RULES="$(< "$(dirname "$0")/../stirr-rules.md")"

PROMPT=$(cat <<EOF
You are a project compliance checker, without access to external tools.
Below are the STIRR rules and the CLI output of stirr-tree.py for specified paths.
Check if the code structure and files comply with the STIRR rules, format the output for console.

=== STIRR-rules.md:
```md
$RULES
```

=== PATHS:
${PATHS[*]}

=== stirr-tree.py output: 
```console
$TREE_OUTPUT
```
EOF
)

case "$AGENT" in
  codex)
    echo "=== Codex: "
    codex -a never -s read-only exec "$PROMPT"
    ;;
  claude)
    echo "=== Claude: "
    claude -p --tools none "$PROMPT"
    ;;
  *)
    usage
    ;;
esac