#!/usr/bin/env bash
set -u
for ROOT in /home/*/miniconda3 /home/*/anaconda3 /opt/conda /root/miniconda3 /home/*/miniforge3; do
    if [ -x "$ROOT/bin/conda" ]; then
        "$ROOT/bin/conda" env list
    fi
    if [ -x "$ROOT/envs/unsloth/bin/python" ]; then
        "$ROOT/envs/unsloth/bin/python" -c 'import sys, torch; print(sys.executable); print(sys.version); print("Torch", torch.__version__, "CUDA", torch.version.cuda, "GPU", torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no GPU"); import importlib.util; print({name: importlib.util.find_spec(name) is not None for name in ["pyg_lib", "torch_geometric", "torch_frame", "relbench", "sentence_transformers"]})'
    fi
done
