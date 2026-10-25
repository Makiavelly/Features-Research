#!/usr/bin/env bash
set -euo pipefail
ulimit -c 0
cd "$(dirname "$0")/.."
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export HF_HOME="$PWD/data/.hf-cache"
export HF_HUB_DISABLE_XET=1
mkdir -p baseline/results/gnn_embeddings_v1
if [ -f baseline/results/gnn_embeddings_v1/exitcode ]; then
    mv baseline/results/gnn_embeddings_v1/exitcode "baseline/results/gnn_embeddings_v1/previous_$(date +%Y%m%d_%H%M%S).exitcode"
fi
trap 'CODE=$?; echo "$CODE" > baseline/results/gnn_embeddings_v1/exitcode; "$PYTHON" RelBenchGNN/tracking.py embedding_pipeline_exit "Эксперимент GNN → LightGBM завершил работу с кодом $CODE" --run-id hm_gnn_embedding_pipeline_v1 --status "$([ "$CODE" = 0 ] && echo complete || echo failed)"' EXIT
"$PYTHON" RelBenchGNN/tracking.py embedding_protocol "Новый эксперимент: замороженный best.pt ID-GNN seed 42 → 128 представлений плюс availability → LightGBM. Обучающие пары и evaluation pools совпадают с ручным baseline; адаптация Appendix C.2 для H&M ranking, не результат авторов. In-sample GNN train embeddings; параметры дерева выбираются только на validation." --run-id hm_gnn_embedding_pipeline_v1 --status extracting
if [ ! -f baseline/cache/gnn_embeddings_v1/manifest.json ]; then
    "$PYTHON" -u RelBenchGNN/export_embeddings.py --output_dir "$PWD/RelBenchGNN/results/seed_42" > RelBenchGNN/logs/embedding_export.log 2>&1
fi
if [ ! -f baseline/results/gnn_embeddings_v1/metrics.json ]; then
    "$PYTHON" -u baseline/run_embedding_tree.py > RelBenchGNN/logs/embedding_tree.log 2>&1
fi
"$PYTHON" RelBenchGNN/report_embedding_tree.py
