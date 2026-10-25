#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$PWD/LLMFeatures/results/qwen25coder7b_seed42_v1"
mkdir -p "$OUT"
exec 9>"$OUT/setup.lock"
flock -n 9 || exit 75
echo "$$" > "$OUT/setup.pid"
trap 'echo "$?" > "$OUT/setup.exitcode"' EXIT
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/bootstrap.py
