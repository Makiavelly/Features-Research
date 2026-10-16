#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
OUT="$PWD/ContextGNN/results/hm_small_v1"
mkdir -p "$OUT" ContextGNN/logs
exec 9>"$OUT/pipeline.lock"
flock -n 9 || exit 75
export HF_HOME="$PWD/data/.hf-cache"
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
"$PYTHON" ContextGNN/prepare_small_dataset.py > ContextGNN/logs/subset.log 2>&1
"$PYTHON" ContextGNN/test_small_protocol.py > ContextGNN/logs/protocol_checks.log 2>&1
if [ ! -f "$OUT/idgnn/metrics.json" ] || [ ! -f "$OUT/contextgnn/metrics.json" ]; then
    "$PYTHON" -u ContextGNN/run_small.py > ContextGNN/logs/training.log 2>&1
fi
if [ ! -f "$OUT/verification.json" ]; then
    "$PYTHON" -u ContextGNN/run_small.py --verify-only > ContextGNN/logs/inference.log 2>&1
fi
"$PYTHON" -u ContextGNN/prepare_tree_features.py > ContextGNN/logs/manual_features.log 2>&1
if [ ! -f ContextGNN/cache/hm_small_v1/idgnn_features/manifest.json ]; then
    "$PYTHON" -u ContextGNN/run_small.py --export-idgnn > ContextGNN/logs/idgnn_features.log 2>&1
fi
"$PYTHON" -u ContextGNN/run_small_trees.py > ContextGNN/logs/trees.log 2>&1
if [ ! -f "$OUT/two_tower/metrics.json" ]; then
    "$PYTHON" -u ContextGNN/run_small_two_tower.py > ContextGNN/logs/two_tower_training.log 2>&1
fi
if [ ! -f "$OUT/two_tower/verification.json" ]; then
    "$PYTHON" -u ContextGNN/run_small_two_tower.py --verify-only > ContextGNN/logs/two_tower_inference.log 2>&1
fi
"$PYTHON" ContextGNN/report_small.py
