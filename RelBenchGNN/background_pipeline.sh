#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p RelBenchGNN/logs
echo "$$" > RelBenchGNN/logs/pipeline.pid
export HF_HOME="$PWD/data/.hf-cache"
export HF_HUB_DISABLE_XET=1
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
PYTHON="$PWD/RelBenchGNN/.venv-wsl/bin/python"
trap 'CODE=$?; echo "$CODE" > RelBenchGNN/logs/pipeline.exitcode; "$PYTHON" RelBenchGNN/tracking.py pipeline_exit "Конвейер завершён с кодом $CODE" --run-id hm_reproduction_pipeline_v1 --status "$([ "$CODE" = 0 ] && echo complete || echo failed)"' EXIT
if [ "${1:-full}" = resume ]; then
    "$PYTHON" RelBenchGNN/tracking.py stage "Продолжение по выбранным seeds: готовое обучение повторно не запускается" --run-id hm_reproduction_pipeline_v1 --status postprocessing
    bash RelBenchGNN/run_experiment.sh full
    exit 0
fi
"$PYTHON" RelBenchGNN/tracking.py stage "Проверка локального датасета" --run-id hm_reproduction_pipeline_v1 --status checking_data
"$PYTHON" -u RelBenchGNN/inspect_data.py > RelBenchGNN/logs/data_check.log 2>&1
"$PYTHON" RelBenchGNN/tracking.py stage "Вычисление простых baseline" --run-id hm_reproduction_pipeline_v1 --status baselines
"$PYTHON" -u baseline/run_simple.py > RelBenchGNN/logs/simple_baselines.log 2>&1
"$PYTHON" RelBenchGNN/tracking.py stage "Короткая проверка ID-GNN" --run-id hm_reproduction_pipeline_v1 --status smoke
bash RelBenchGNN/run_experiment.sh smoke > RelBenchGNN/logs/smoke.log 2>&1
"$PYTHON" RelBenchGNN/tracking.py stage "Полные прогоны ID-GNN согласно experiment_plan.json" --run-id hm_reproduction_pipeline_v1 --status training
bash RelBenchGNN/run_experiment.sh full
