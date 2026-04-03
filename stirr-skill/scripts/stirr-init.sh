#!/usr/bin/env bash
# #Human
# Humans/Agents: Run this script in a project dir to create files (skips existing):
# - `spec.md` and `journal.md` files with #Human frontmatter and template content.
# - `implement.sh`, `stirr-tree.py` and `stirr-check.sh` symlinks.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

create_file() {
  local filename="$1"
  local content="$2"
  if [ -f "$filename" ]; then
    printf "%s... \tSkipping, already exists\n" "$filename"
  else
    printf "%s" "$content" > "$filename"
    printf "%s... \tCreated\n" "$filename"
  fi
}

create_file "spec.md" "$(
cat <<'SPEC'
--
tags: #Human
--

# #ConventionRL
Read and follow `stirr-skill` rules.

# #SDD
- 

# #TDD
-

# #ImplementRL
- 

# ToDo: Iteration 1
-

<!-- Iteration format: 
# Done: Iteration 1..N-1 
# ToDo: Iteration N 
-->
SPEC
)"

create_file "journal.md" "$(
cat <<'JOURNAL'
--
tags: #Human
--

# Iteration 1
- 

<!-- Iteration format: # Iteration 1..N -->
JOURNAL
)"

create_symlink() {
  local source="$1"
  local target="$2"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    printf "%s... \tSkipping, already exists\n" "$target"
  else
    ln -sfn "$source" "$target"
    printf "%s... \tSymlink set\n" "$target"
  fi
}

create_symlink "$SKILL_DIR/scripts/implement.sh" "implement.sh"
create_symlink "$SKILL_DIR/scripts/stirr-tree.py" "stirr-tree.py"
create_symlink "$SKILL_DIR/scripts/stirr-check.sh" "stirr-check.sh"
