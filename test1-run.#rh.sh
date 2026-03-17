#!/usr/bin/env bash
set -euo pipefail

trap 'echo FAIL; exit 1' ERR

./stirr.#rh > test1-run.log 2>&1
echo Pass
