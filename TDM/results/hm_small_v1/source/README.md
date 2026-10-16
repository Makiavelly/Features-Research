# TDM on frozen H&M small-v1

This is a compact local PyTorch adaptation of TDM, not a TorchEasyRec install
and not JTM. It uses the project's existing `RelBenchGNN/.venv-wsl` environment.
No additional packages are required. The original environments are preserved.

- Protocol and deviations: [PROTOCOL_SMALL.md](PROTOCOL_SMALL.md).
- Data/model/tree/scoring implementation: `common.py`.
- Training/selection/evaluation/replay: `run_small.py`.
- Behavioral checks and isolated smoke: `check_protocol.py`.
- Pipeline: `run_pipeline.sh` (Ubuntu WSL from repository root).
- Report: `../reports/tdm_small_v1/report.md`.
- Results: `results/hm_small_v1/{fixed,cluster}`; logs: `logs/small_v1`.

The existing full runs must not be overwritten. Training refuses an existing
result directory. Do not rerun the pipeline to inspect results: read the report,
JSON metrics and verification files. A change to model/data/hyperparameters
requires a new unique run ID and new result directory.

Each `best.pt` includes the exact node tree, mapping, configuration and encoder
weights. `tree.npz` is an additional tree export. Both are local artifacts ignored
by Git, as are NumPy scores/predictions/traces. JSON metrics do not restore weights.
`selection_pretest.json` freezes both checkpoints before any test evaluation.
`verification.json` verifies all8beam/full ×val/test outputs in a separate process.

Frozen-source replay command (does not train or overwrite saved predictions):

```bash
CUBLAS_WORKSPACE_CONFIG=:4096:8 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 \
RelBenchGNN/.venv-wsl/bin/python TDM/run_small.py verify
```

Training code hashes are checked on replay; preserve the experiment source.
Source assessment/pinned upstream files: `../reports/tdm_assessment/`.
