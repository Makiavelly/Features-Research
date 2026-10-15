#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$PWD/LLMFeatures/results/qwen25coder7b_seed42_v2/shared_idgnn"
mkdir -p "$OUT"
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
trap 'echo "$?" > "$OUT/exitcode"' EXIT
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/run_shared_evaluation.py
