#!/usr/bin/env bash
# #Human

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

cd "$(dirname "$0")" # Change to the stirr-check.sh dir.

TREE_OUTPUT=$(./stirr-tree.py "${PATHS[@]}") # Captures the stirr-tree.py output.

RULES="$(< "../stirr-skill/SKILL.md")"

# Constructs the prompt with rules, paths, and tree output. 
PROMPT=$(cat <<EOF
You are a project compliance checker that: 
- Can read and search files in the project paths. 
- Can read test logs. 
- CANNOT modify files, execute tests or code, or access files outside the project paths. 
Below are the STIRR rules and the CLI output of stirr-tree.py for the specified paths. 
Check if the code structure and files comply with the STIRR rules. 
You should output pure text for console, no Markdown. 
Answer within 45 seconds (e.g. use \`date\` at the start). 

=== STIRR rules (from SKILL.md):
\`\`\`md
$RULES
\`\`\`

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
  codex)
    echo "Running Codex..."
    codex -a never -s workspace-write exec "$PROMPT" 2>&1 \
      | awk '/^=== PATHS:/,0' # Codex is a bit verbose, display only after path part.
    ;;
  claude)
    echo "Running Claude..."
    claude -p "$PROMPT" 2>&1
    ;;
  copilot)
    echo "Running Copilot..."
    copilot -p "$PROMPT" --allow-all-tools --allow-all-paths --allow-all-urls 2>&1
    ;;
  cursor)
    echo "Running Cursor..."
    agent --print --force --trust "$PROMPT" 2>&1
    ;;
  *)
    usage
    ;;
esac
