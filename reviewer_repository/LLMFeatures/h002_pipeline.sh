#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$PWD/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1"
mkdir -p "$OUT"
exec 8>"$OUT/pipeline.lock"
flock -n 8 || exit 75
echo "$$" > "$OUT/launcher.pid"
if [ -f "$OUT/exitcode" ]; then
    mv "$OUT/exitcode" "$OUT/previous_$(date +%Y%m%d_%H%M%S).exitcode"
fi
trap 'echo "$?" > "$OUT/exitcode"' EXIT
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export LLMFE_VALIDATOR_VERSION=h002
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/test_protocol.py
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/test_h002.py
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/h002_run.py
