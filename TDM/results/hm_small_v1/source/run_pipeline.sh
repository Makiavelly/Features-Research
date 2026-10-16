#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p TDM/logs/small_v1
exec 9>TDM/logs/small_v1/pipeline.lock
flock -n 9 || exit 75
echo $$ >TDM/logs/small_v1/pipeline.pid
trap 'echo $? >TDM/logs/small_v1/pipeline.exitcode' EXIT
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
"$PYTHON" -u TDM/check_protocol.py >TDM/logs/small_v1/checks.log 2>&1
"$PYTHON" -u TDM/run_small.py train >TDM/logs/small_v1/training.log 2>&1
"$PYTHON" -u TDM/run_small.py evaluate >TDM/logs/small_v1/evaluation.log 2>&1
"$PYTHON" -u TDM/run_small.py verify >TDM/logs/small_v1/verification.log 2>&1
"$PYTHON" -u TDM/report_small.py >TDM/logs/small_v1/report.log 2>&1
