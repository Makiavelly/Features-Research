# Larger H&M comparison

The authorized nine-method comparison runs locally in WSL. Neural methods use
the RTX3060; tree training and feature construction use CPU. GPT requests go to
the existing configured provider. No Qwen/Llama model is loaded or called.

Use the existing `RelBenchGNN/.venv-wsl/bin/python` without the older audit
dependency overlay: its NumPy2 is incompatible with the native PyTorch2.2.
No environment changes are needed.

Entry point: `CVBenchmark/launch.py`. It starts a detached pipeline, saves its
PID, and refuses to launch a second live copy. The pipeline performs validator
and GPU smoke checks, then runs a sequential GPU lane alongside a sequential
CPU/API lane. All model selections must finish before any outer-test scoring.
Completed stages are reused on resume; paid responses are stored individually.
If an interrupted neural fit lacks its completion marker, inspect its checkpoint
before restarting: this runner does not claim mid-epoch optimizer recovery.

Read the live `reports/medium_cv_v2/pipeline.log`, `pipeline_status.json` and
`stages/*.log`. Status files alone do not prove a process is still alive; check
the WSL PID/process tree after a reboot. Provider/transport failures stop their
lane and preserve outputs. Never call a partial budget a completed experiment.

Protocol: [PROTOCOL.md](PROTOCOL.md). V1 data preparation is retained but not used
for fitting. V2 retains original targets outside the10000-item catalog in the
primary metric, including users with no retrievable positives. Catalog-conditional
MAP is a separate diagnostic. Train pairs are shared by all four tree methods.

Reports appear only after all27 method/fold results and replays complete:
`reports/medium_cv_v2/report.md`, `fold_metrics.csv`, `comparison.json`,
`paired_differences.csv`, `api_usage.csv` and comparison/fold/histogram graphics.
Raw datasets, weights, caches and API payloads stay outside Git via `.gitignore`.
Do not edit frozen runtime sources or experimental settings during a live run.
