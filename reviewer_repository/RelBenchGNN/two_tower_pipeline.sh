#!/usr/bin/env bash
set -euo pipefail
ulimit -c 0
cd "$(dirname "$0")/.."
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
OUT="$PWD/RelBenchGNN/results/two_tower_seed_42"
mkdir -p "$OUT"
exec 9>"$OUT/pipeline.lock"
flock -n 9 || exit 75
echo "$$" > "$OUT/pipeline.pid"
if [ -f "$OUT/exitcode" ]; then mv "$OUT/exitcode" "$OUT/previous_$(date +%Y%m%d_%H%M%S).exitcode"; fi
export HF_HOME="$PWD/data/.hf-cache"
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
trap 'CODE=$?; echo "$CODE" > "$OUT/exitcode"; "$PYTHON" RelBenchGNN/tracking.py two_tower_pipeline_exit "Двухбашенный конвейер завершён с кодом $CODE" --run-id hm_twotower_pipeline_v1 --status "$([ "$CODE" = 0 ] && echo complete || echo failed)"' EXIT
FLAGS=(--output_dir "$OUT" --cache_dir "$PWD/RelBenchGNN/cache" --seed 42 --epochs 20 --batch_size 256 --eval_batch_size 128 --max_steps_per_epoch 2000 --temporal_strategy uniform --resume)
if [ ! -f "$OUT/metrics.json" ]; then
    "$PYTHON" -u RelBenchGNN/run_two_tower.py "${FLAGS[@]}" > RelBenchGNN/logs/two_tower_training.log 2>&1
fi
"$PYTHON" -u RelBenchGNN/run_two_tower.py "${FLAGS[@]}" --inference-only > RelBenchGNN/logs/two_tower_inference.log 2>&1
"$PYTHON" RelBenchGNN/report_two_tower.py
