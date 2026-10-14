#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_CACHE_DIR="$PWD/RelBenchGNN/.uv-cache"
UV="$PWD/RelBenchGNN/tools/uv-x86_64-unknown-linux-gnu/uv"
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python numpy==1.26.4 pandas==2.2.3 pyarrow==15.0.2 scipy==1.13.1 scikit-learn==1.5.2 lightgbm==4.3.0 optuna==3.6.1 duckdb==1.1.3
"$UV" pip freeze --python RelBenchGNN/.venv-wsl/bin/python > RelBenchGNN/requirements.lock.txt
RelBenchGNN/.venv-wsl/bin/python -c 'import pyarrow, pandas, torch, pyg_lib, torch_frame; print(pyarrow.__version__, pandas.__version__, torch.__version__, torch.cuda.is_available())'
