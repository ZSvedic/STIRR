#!/usr/bin/env bash
# #Human
set -euo pipefail

./llm-call.sh codex "What is the height of the Eiffel Tower in m?" 
./llm-call.sh claude "What is the height of the Eiffel Tower in ft?"