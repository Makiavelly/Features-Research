# H010: GPT research on train folds

Protocol: [PROTOCOL.md](PROTOCOL.md). Current independent run is
`hm_medium_h010_research_seed42_v2`. The optional-tool v1 pilot is preserved,
incomplete, in `results/v1` and `reports/medium_h010_research_v1`.

Run in native WSL from the project root using the existing environment:

```bash
RelBenchGNN/.venv-wsl/bin/python LLMResearch/check.py
RelBenchGNN/.venv-wsl/bin/python LLMResearch/launch.py
```

`check.py` performs no API requests. The real runner uses the existing secret
in `.env`; request logs never include Authorization. The text JSON tool protocol
works over the existing Chat Completions adapter without requiring native tools.

Inspect the actual WSL PID/process tree first. The launcher refuses another
live controller and the pipeline/fold locks prevent duplicate execution. Resume
replays durable API responses and query outputs. A transport/provider failure
stops the pipeline; inspect the saved attempt before any explicit retry. Never
delete attempt directories or reset paid-call counts. Do not refresh frozen
runtime/config after API requests; changed settings require a new run ID.

Current outputs: `results/v2/fold_*/` and `reports/medium_h010_research_v2/`.
The latter contains `pipeline.pid`, `pipeline.log`, `pipeline_status.json`,
`fold_*_status.json`, preflight verification, and eventually the final report.
Raw requests/responses, SQL input/output, database manifests and program trials
are retained in each fold's local output. They are excluded from Git.

The controller runs train/search/confirmation sequentially over three folds,
freezes all choices, then evaluates and replays heldout/val/test. It audits exact
API-message histories and computes a paired customer bootstrap against original
H009-20. Completion still requires visual inspection of final figures and a
tracking event; a detached PID or smoke metric is not a completed experiment.
