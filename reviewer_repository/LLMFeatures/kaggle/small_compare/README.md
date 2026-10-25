# Qwen vs Llama on ContextGNN's small H&M dataset

Delivery:

- `../hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb`: self-contained Kaggle T4 notebook.
- `../hm_small_sql_compare_v1.zip`: attach as a Kaggle Dataset/Input (about0.9MB).
- `delivery_manifest.json`: notebook, embedded module and bundle checksums.

Import the notebook into a fresh Kaggle session, enable Internet and T4, attach the
new small archive, choose `LLAMA_SOURCE`, then Run All or Save Version/Run All.
Official Meta weights require approved access and an enabled `HF_TOKEN` secret;
the alternative publisher is `unsloth/Meta-Llama-3.1-8B-Instruct`. Both are loaded
with Transformers, not the Unsloth library. Qwen uses its public official repository.
Remote immutable model revisions are resolved and saved before either search starts.

Both models use Qwen's original JSON interface: up to24 `aggregates` entries with
`name/keys/sql` and12 `derived` entries with `name/sql`. These are complete feature
sets, not Python and not free text. The host uses the frozen local-Qwen FeatureEngine;
it materializes input transactions before disabling external access. Item categories
are factorized once in both static features and history, preventing sparse high-valued
category codes from creating huge LightGBM categorical bitsets. This is an explicit
encoding adaptation. Format/SQL operations remain the original interface. There is
no grammar-constrained decoding in this comparison.

The earlier local Qwen was `qwen2.5-coder:7b-instruct-q4_K_M` through Ollama.
Here Qwen2.5-Coder-7B-Instruct and Llama-3.1-8B-Instruct both use NF4/double-quant/
FP16 on GPU0, one model at a time. This does not reproduce the exact earlier Qwen
quantized artifact. Chat templates are model-specific; instructions, data access,
evaluation, feedback rules, call seeds and success budgets are shared.

Data and evaluation:

- Frozen `data/rel-hm-small-v1`:5000 customers,5000 items,46442 transactions.
- Original72813 labeled train pairs/4804 user-times/8snapshots from the small manual
  baseline, sorted-key/label SHA verified against its saved metrics; no resampling.
- Past-only transactions (`t_dat <= cutoff`), exactly the original local-Qwen
  history semantics. All retained subset history is available; no additional
  180-day truncation is introduced (the test cutoff has about187days of history).
- Original304 validation and250 test rows; full5000-item catalog for each user.
- Fixed seed42 validation split:search128/confirmation88/heldout88, no overlap.
- Each LLM gets20 successful distinct programs, at most300 calls including up to3
  repairs/proposal;3 independent islands with best-in-island memory, as in local H002.
- All15 raw fields always appended. No manually engineered history or GNN features
  are supplied to either model. Raw control can win the selection.
- LightGBM binary150rounds/31leaves,4threads, all seeds42, identical parameters.
- Top3 search programs plus raw compete on confirmation; both selections frozen
  before final heldout/val/test. Independent subprocesses reload saved models and
  repeat final scoring. Exact tie order: descending score, ascending article_id.
- Seven frozen baselines are bundled with provenance and top12 predictions:
  ContextGNN,IDGNN,two-tower,manual LightGBM,IDGNN→LightGBM,Recformer zero-shot/finetuned.
  Their MAPs are recomputed; the original popularity control is also recomputed.

Outputs: per-call `prompt.txt`, `response.json`, `trial.json` (call/proposal/island/
repair/parent/status/error/failure_stage), feature programs, LightGBM weights and
learning curves; `selected.json`, full-catalog predictions/AP/user order; independent
replay metrics; `comparison.csv`, comparison/search/loss plots, AP histograms,
paired-user bootstrap interval. Results ZIP is updated after every call and at
exceptions/finalization. Download caches are excluded and removed after each model
to avoid keeping both unquantized download artifacts on disk. Cancel is not a
guarantee that Kaggle publishes outputs.

Validation304 includes search/confirmation and is not untouched for LLMs. Baselines
used original full validation for selection, so their heldout88 is not untouched
either. Test is the shared comparison endpoint.250 users/one seed is preliminary.
Baselines have different tuning/graph/pretraining budgets. This is not a reproduction
of the LLM-FE paper or a direct comparison with the large H&M dataset.

Rebuild bundle: run `prepare_bundle.py` in the existing project WSL environment.
Rebuild notebook: run `../build_small_compare_notebook.py`.
Validate: run `check_delivery.py` with `../.check-deps` on `PYTHONPATH` for nbformat.
CPU smoke uses deterministic fake responses and real LightGBM/data; it measures
pipeline correctness, never Qwen/Llama quality. Smoke artifacts live separately in
`reports/kaggle_llmfe_validation/small_compare_v1`.
