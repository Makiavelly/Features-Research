# Qwen2.5-Coder-14B-Instruct — matched small H&M experiment

Notebook: `../hm_small_qwen14b_sql_kaggle_t4.ipynb`.
Input: the existing `../hm_small_sql_compare_v1.zip`, unchanged.

Run in a fresh Kaggle session with Internet and one T4. The official Qwen14B
repository is public: no access approval, HF login or Kaggle Secret is needed.
The notebook resolves and records an immutable revision before loading NF4/
double-quant/FP16 weights on GPU0. No local model inference has been performed;
the actual14B peak VRAM remains unmeasured. An OOM is saved as failure/ZIP;
context is not silently shortened to obtain an incomparable result.

Only Qwen14B is downloaded and searched. The Qwen7B/Llama notebook may run in
parallel; its output is neither required nor loaded here. Download the final
`hm_small_qwen14b_sql_v1_<hash>_results.zip`. The user will supply all three
LLM results for comparison later, locally in this repository.

All four modules embedded in the running comparison notebook are copied
byte-for-byte: `features.py`, `original_prompt.py`, `worker.py`, `runtime.py`.
The additional `runtime14.py` adapts only the final report to a single selected
LLM; Qwen14B-vs-raw bootstrap replaces the former Llama-vs-Qwen bootstrap.
The parent notebook's checksum and shared module checksums are recorded in
`delivery_manifest.json`. The parent notebook and original data are not edited.

Matched settings:

- small-v1,72813 original train pairs/4804user-times/8cutoffs, train-key SHA unchanged;
- same5000-item full-catalog scoring, original304val/250test users and ordering;
- same seed42 search128/confirmation88/heldout88 validation partitions;
- original local-Qwen SQL/JSON complete programs,24aggregates/12derived maximum;
- identical host joins/time filtering/compact static categories and appended15raw fields;
- LightGBM150rounds/31leaves/4threads, all seeds42, same categorical inputs;
- NF4/double-quant/FP16, SDPA, one generation at a time;
- temperature.8/top_p1/top_k0, input6144/output2048 tokens, seed42+call−1;
- target20 successfully evaluated distinct programs, cap300calls including up to3repairs,
  3islands with1best-in-island demonstration, same canonical duplicate detection;
- top3 search programs plus raw compete on confirmation; test only after selection;
- model reload and separate replay processes for heldout/val/test;
- same frozen baseline predictions, independently recomputed MAP, graphs and histograms.

The14B run config uses a new `protocol` and model ID and omits `llama_source`.
Versions, GPU name, data/runtime/model revision hashes create a unique run fingerprint.
The data, budgets, search instruction and downstream model settings are unchanged.

Outputs have the same `raw_control`, `candidates`, `selected.json`, per-call prompts/
responses/status/island/repair records, program/model/schema/learning curves,
top12 predictions/AP/user IDs, final report/comparison and plots as the parent.
The model directory is `qwen14b`. ZIPs exclude download caches and scratch tables.

Validation304 includes search/confirmation. Baselines used full validation for
selection; their heldout88 was not originally held out. Test250/one seed gives
preliminary evidence, and baseline tuning/graph/pretraining budgets differ.

Build: run `../build_qwen14_small_notebook.py` in the existing project Python.
Check: run `check_delivery.py` with `../.check-deps` on `PYTHONPATH`.
The check verifies notebook schema, unchanged shared source/config/initial prompt,
absence of previous-LLM inputs and secret requirements, and single-model report
output using frozen CPU test fixtures. It does not generate14B predictions.
Verification: `reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json`.
