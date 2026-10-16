# Recformer H&M small-v1

Run: hm_recformer_small_seed42_v1. Authorised2026-10-16.
Frozen dataset: data/rel-hm-small-v1 (train4804/val304/test250; catalog5000).
No new membership selection, filtering of empty histories, or test-driven tuning.

Upstream replication commit26b00a58e7affe0c54a89c143ea7bce37f2e8e08.
Original author repository currently contains README only and points to this replication.
Checkpoint and tokenizer provenance/hashes: data/models/recformer/download_manifest.json.
Checkpoint must pass file size/ZIP check and tensor loading before any full run.
No package changes: use RelBenchGNN/.venv-wsl; import only model/tokenizer modules
without invoking upstream Lightning package imports. Upstream source unchanged.

Inputs: title=prod_name; category=product_type_name/product_group_name/section_name;
description=colour_group_name/graphical_appearance_name/detail_desc. Three attributes,
32tokens per attribute,256tokens total,50items max. IDs used only for lookup.
Histories: t_dat<=each row timestamp, repeats preserved, source transaction row
order breaks same-day ties (not an observed intraday order). Future events cannot
displace past events during history truncation. No targets enter the input.

Transfer variants: published pretrained weights without H&M training (zero-shot)
and short two-stage fine-tuning. Full pretraining is outside this experiment.
Loss: per-user-time mean negative log full-catalog softmax across unique positive
weekly targets, then batch mean. This differs from paper next-item supervision.
Both stages nominally2 full epochs; timing probe must establish budget before launch.
FP16 autocast; normalized FP32 matrix multiplication for exact catalog scoring,
temperature.05, AdamW lr5e-5/weight_decay0/foreachFalse, gradient clipping1,
batch4/accum4, seed42. All4804rows each epoch; no sampled negatives.
Stage1 re-encodes full catalog before each epoch. Stage2 reloads best stage1
model plus corresponding fixed item cache and continues with that cache.
Model selection considers trained checkpoints by full validation MAP@12;
zero-shot is a separately reported control, not eligible as fine-tuned checkpoint.
No test evaluation until model selection ends. No masking of purchased items.

Scores: cosine/temperature; equal scores ordered by local article_id ascending.
Evaluate all5000items on all304val/250test rows using RelBench evaluator and
an independent AP computation. Save full score matrices, top12, per-user AP.
Save encoder checkpoint together with its exact item cache, especially for stage2.
Independent process must reload both zero-shot and fine-tuned checkpoints and
repeat full val/test. Require matching top12 and numerically close full scores.
Metrics status remains pending until replay passes. Old models/reports unchanged.

Preparation/download and smoke timings recorded separately from training/evaluation.
Target wall-clock about1hour; no empirical guarantee before the probe.
No early claim of paper reproduction or performance superiority: small conditional
task,250test rows,one seed,external Amazon pretraining and differing training budgets.

Commands from project root in WSL:

```bash
RelBenchGNN/.venv-wsl/bin/python -u Recformer/run_small.py --probe
RelBenchGNN/.venv-wsl/bin/python -u Recformer/run_small.py
RelBenchGNN/.venv-wsl/bin/python -u Recformer/run_small.py --verify-only
RelBenchGNN/.venv-wsl/bin/python Recformer/report_small.py
```
