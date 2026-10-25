#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p Recformer/logs/ablations_v1
exec 9>Recformer/logs/pipeline.lock
flock -n 9 || exit 75
echo $$ > Recformer/logs/ablations_v1/pipeline.pid
trap 'echo $? > Recformer/logs/ablations_v1/pipeline.exitcode' EXIT
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export HF_HOME="$PWD/data/.hf-cache"
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
for variant in low_lr_warmup freeze_lower6; do
  "$PYTHON" -u Recformer/run_ablations.py --variant "$variant" --train-only > "Recformer/logs/ablations_v1/${variant}_training.log" 2>&1
done
for variant in low_lr_warmup freeze_lower6; do
  "$PYTHON" -u Recformer/run_ablations.py --variant "$variant" --evaluate-only > "Recformer/logs/ablations_v1/${variant}_evaluation.log" 2>&1
  "$PYTHON" -u Recformer/run_ablations.py --variant "$variant" --verify-only > "Recformer/logs/ablations_v1/${variant}_verification.log" 2>&1
done
"$PYTHON" -u Recformer/report_ablations.py > Recformer/logs/ablations_v1/report.log 2>&1
