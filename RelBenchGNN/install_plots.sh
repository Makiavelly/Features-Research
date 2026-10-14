#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_CACHE_DIR="$PWD/RelBenchGNN/.uv-cache"
UV="$PWD/RelBenchGNN/tools/uv-x86_64-unknown-linux-gnu/uv"
"$UV" pip install --python RelBenchGNN/.venv-wsl/bin/python matplotlib==3.9.2 numpy==1.26.4 contourpy==1.3.0
"$UV" pip freeze --python RelBenchGNN/.venv-wsl/bin/python > RelBenchGNN/requirements.lock.txt
