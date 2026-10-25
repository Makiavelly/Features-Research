#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_CACHE_DIR="$PWD/RelBenchGNN/.uv-cache"
export HF_HOME="$PWD/data/.hf-cache"
export HF_HUB_DISABLE_XET=1
mkdir -p RelBenchGNN/logs RelBenchGNN/tools
tar -xzf RelBenchGNN/tools/uv.tar.gz -C RelBenchGNN/tools
UV="$PWD/RelBenchGNN/tools/uv-x86_64-unknown-linux-gnu/uv"
"$UV" venv --clear RelBenchGNN/.venv-wsl --python /usr/bin/python3
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python torch==2.2.2 --index-url https://download.pytorch.org/whl/cu118
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python 'numpy==1.26.4' 'pandas==2.2.3' 'pyarrow==15.0.2' 'scipy==1.13.1' 'scikit-learn==1.5.2' 'pytorch-frame==0.2.3' 'torch-geometric==2.5.3' 'sentence-transformers==3.3.1' 'transformers==4.46.3' 'huggingface-hub<1' 'lightgbm==4.3.0' 'optuna==3.6.1' 'duckdb==1.1.3' psutil -e ./RelBenchGNN/upstream
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python pyg-lib torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.2.0+cu118.html
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python matplotlib==3.9.2 numpy==1.26.4 contourpy==1.3.0
RelBenchGNN/.venv-wsl/bin/python -c 'import torch, pyg_lib, torch_frame, relbench; print(torch.__version__, torch.cuda.is_available(), relbench.__version__); print(torch.cuda.get_device_name(0))'
"$UV" pip freeze --python RelBenchGNN/.venv-wsl/bin/python > RelBenchGNN/requirements.lock.txt
