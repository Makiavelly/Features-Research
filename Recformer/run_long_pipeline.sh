#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p Recformer/logs/long_v1
exec 9>Recformer/logs/pipeline.lock
flock -n 9 || exit 75
echo $$ > Recformer/logs/long_v1/pipeline.pid
trap 'echo $? > Recformer/logs/long_v1/pipeline.exitcode' EXIT
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export HF_HOME="$PWD/data/.hf-cache"
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
"$PYTHON" -u Recformer/run_long.py --train-only > Recformer/logs/long_v1/training.log 2>&1
"$PYTHON" -u Recformer/run_long.py --evaluate-only > Recformer/logs/long_v1/evaluation.log 2>&1
"$PYTHON" -u Recformer/run_long.py --verify-only > Recformer/logs/long_v1/verification.log 2>&1
"$PYTHON" -u Recformer/report_long.py > Recformer/logs/long_v1/report.log 2>&1
