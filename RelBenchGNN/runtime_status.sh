#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
if [ -f RelBenchGNN/logs/pipeline.pid ]; then
    PIPELINE=$(cat RelBenchGNN/logs/pipeline.pid)
    ps -p "$PIPELINE" -o pid,etime,pcpu,rss,args
    ps --ppid "$PIPELINE" -o pid,etime,pcpu,rss,args
fi
ps -eo pid,ppid,etime,pcpu,rss,args | grep -E 'run_idgnn.py|run_simple.py|inspect_data.py|run_inference.py|run_manual_tree.py|postprocess.py' | grep -v grep || true
free -h
nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv
