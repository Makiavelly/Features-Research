#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export HF_HOME="$PWD/data/.hf-cache"
export HF_HUB_DISABLE_XET=1
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
MODE="${1:-full}"
if [ "$MODE" = smoke ]; then
    exec "$PYTHON" -u RelBenchGNN/run_idgnn.py --dataset rel-hm --task user-item-purchase \
        --cache_dir "$PWD/RelBenchGNN/cache" --output_dir "$PWD/RelBenchGNN/results/smoke" \
        --epochs 1 --max_steps_per_epoch 1 --batch_size 32 --eval_batch_size 32 --smoke --run_id hm_idgnn_smoke_v1
fi
for SEED in $("$PYTHON" RelBenchGNN/experiment_plan.py); do
    OUTPUT="$PWD/RelBenchGNN/results/seed_$SEED"
    if [ -f "$OUTPUT/metrics.json" ]; then
        continue
    fi
    "$PYTHON" -u RelBenchGNN/run_idgnn.py --dataset rel-hm --task user-item-purchase \
        --cache_dir "$PWD/RelBenchGNN/cache" --output_dir "$OUTPUT" \
        --seed "$SEED" --run_id "hm_idgnn_last_seed_${SEED}_v1" --resume --epochs 20 --lr 0.001 --batch_size 512 --eval_batch_size 128 \
        --channels 128 --aggr sum --num_layers 2 --num_neighbors 128 --temporal_strategy last \
        --max_steps_per_epoch 2000 > "RelBenchGNN/logs/seed_$SEED.log" 2>&1
done
"$PYTHON" RelBenchGNN/summarize.py
