#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$PWD/LLMFeatures/results/qwen25coder7b_seed42_v2"
mkdir -p "$OUT"
exec 8>"$OUT/pipeline.lock"
flock -n 8 || exit 75
echo "$$" > "$OUT/launcher.pid"
if [ -f "$OUT/exitcode" ]; then
    mv "$OUT/exitcode" "$OUT/previous_$(date +%Y%m%d_%H%M%S).exitcode"
fi
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export PYTHONUNBUFFERED=1
trap 'echo "$?" > "$OUT/exitcode"' EXIT
while [ ! -f "$OUT/setup.exitcode" ]; do sleep 5; done
[ "$(cat "$OUT/setup.exitcode")" = 0 ] || exit 1
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/test_protocol.py
RelBenchGNN/.venv-wsl/bin/python -u LLMFeatures/run.py
