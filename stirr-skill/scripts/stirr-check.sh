#!/usr/bin/env bash
# #Human #STIRR #Include

usage() {
  printf "USAGE: stirr-check.sh <codex|claude|copilot|cursor> PATH1 [PATH2 ...]\n\n"
  printf "1. Calls stirr-tree.py on provided PATHs, pipes output to a string.\n"
  printf "2. Constructs a validation prompt, including the tree output.\n"
  printf "3. Calls CLI agent with a given prompt.\n"
  exit 1
}

set -euo pipefail

[ "$#" -ge 2 ] || usage # Displays usage if less than 2 args.

AGENT="$1"
shift
PATHS=("$@")

DIR="$(cd "$(dirname "$0")" && pwd)"
TREE_OUTPUT=$("$DIR/stirr-tree.py" "${PATHS[@]}")

# Constructs the prompt with rules, paths, and tree output. 
PROMPT=$(cat <<EOF
You are the STIRR-skill project compliance checker that: 
- Can read and search files in the project paths. 
- Can read test logs. 
- CANNOT modify files, execute tests or code, or access files outside the project paths. 
Below is the CLI output of stirr-tree.py for the specified paths. 
Check if the code structure and files comply with the #STIRR rules. 
You should output pure text for console, no Markdown. 
Answer within 40 seconds (e.g. use \`date\` at the start). 

=== PATHS:
${PATHS[*]}

=== stirr-tree.py output: 
\`\`\`console
$TREE_OUTPUT
\`\`\`
EOF
)

# Calls the appropriate agent.
case "$AGENT" in
  codex)   CMD=(codex -a never -s read-only exec "$PROMPT");;
  claude)  CMD=(claude -p "$PROMPT");;
  copilot) CMD=(copilot -p "$PROMPT");;
  cursor)  CMD=(agent --print --trust "$PROMPT");;
  *) usage;;
esac

printf "===== Running:\n${CMD[*]}\n=====\n"
exec "${CMD[@]}"
