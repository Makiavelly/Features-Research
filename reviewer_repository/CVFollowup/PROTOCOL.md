# Medium H&M follow-up v1 (2026-10-18)

Authorized tasks: diagnose ContextGNN's ranking collapse; extend H008/H009
feature search to30 and40 accepted programs; tune Recformer LR/warmup.
Reuse frozen medium-v2 data, all3 folds, shared tree pairs, seed42 and the
original full-target metrics. No Qwen/Llama calls. Preserve medium-v2 sources,
models, API payloads and published results unchanged.

## API budget curves

Fork each of the six saved20-program search streams into a new directory,
with an immutable provenance manifest. Reuse the exact responses, request
messages, trial scores, LightGBM weights and original own-island memories.
Continue adaptively to30, snapshot selection, then40 and snapshot selection.
Three islands,3 repairs,300 actual POSTs TOTAL per arm/fold including the
inherited requests and transport failures. Match the existing Python interface,
LightGBM150/31/.05/4CPU and no automatically appended raw15.

Only search fitness enters proposal history; confirmation chooses top3 plus
constant control at each budget. No outer-test values are sent to GPT.
Snapshot the full selection at20/30/40. Finish all searches and freeze30/40
selections before scoring these budgets on the original test weeks. This is
continuation on already inspected internal test periods, not fresh validation.
Report quality versus accepted-program budget and actual POST/token usage;
numeric duplicates remain a diagnostic. No retrospective program replacement.

## ContextGNN diagnosis

First inspect saved schemas, ID/target alignment and score components using
isolated diagnostic copies. Check both the old successful model and medium
models for local graph context, global item embedding scores, ranking
diversity, feature ranges and inactive-item recommendations. Record evidence
separately from hypotheses. Any causal ablation/fix uses a new run directory
and validation-only selection; retain the failed models and original metrics.
Do not declare the root cause from replay agreement or size differences alone.

## Recformer tuning

Before training, fix a4-setting grid: (peakLR,warmup successful updates)
[(1e-6,100),(3e-6,100),(1e-5,300),(3e-6,300)]. Existing1e-5/100 is the
baseline. Each setting starts from the same original pretrained assets on
each fold, with the same2+2 full epochs, item/history encoding, batch4,
accumulation4, FP16 and multi-positive loss. Keep stage2 behavior unchanged
for this grid so that only LR/warmup differ. Correct descriptive scheduler
metadata to reflect the actual fold-specific total updates.

Use original search256 users for epoch selection. Select one grid setting
globally by the equal-fold mean of the3 inner search scores, including the
existing baseline. Do not use outer-test scores to choose or stop variants.
Freeze the selected setting and its3 checkpoints before outer scoring;
compare it to the saved baseline and zero-shot with paired customer bootstrap.
Report every setting's validation score, even if tuning fails to improve.
An optimizer/stage2 redesign would be a separate ablation, not an unlogged
change within this LR/warmup grid.

## Execution and reporting

CPU/API continuation can run alongside one GPU job. Serialize all GPU jobs;
do not duplicate paid requests on resume. Preserve source/config hashes,
process IDs, stage logs, failed requests and completed-stage markers.
No environment changes. Use native RelBenchGNN/.venv-wsl, not NumPy2 overlays.
Smoke checks are not model-quality results. Final plots include20/30/40 API
curves, Recformer validation grid and the updated paired comparison. Document
that only3 calendar folds/one model seed are available and the test periods
were previously inspected. Distinguish diagnostic failures from final results.
