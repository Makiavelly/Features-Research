#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p Recformer/logs
exec 9>Recformer/logs/pipeline.lock
flock -n 9 || exit 75
echo $$ > Recformer/logs/pipeline.pid
trap 'echo $? > Recformer/logs/pipeline.exitcode' EXIT
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HOME="$PWD/data/.hf-cache"
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
"$PYTHON" -u Recformer/run_small.py > Recformer/logs/training.log 2>&1
"$PYTHON" -u Recformer/run_small.py --verify-only > Recformer/logs/verification.log 2>&1
"$PYTHON" -u Recformer/report_small.py > Recformer/logs/report.log 2>&1
