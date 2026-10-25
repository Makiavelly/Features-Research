# H&M medium: nested temporal cross-validation v2

V1 preparation is retained separately. Before fitting, v2 corrects evaluation:
ALL source user-times and ALL original weekly positives are retained in val/test,
including purchases outside the10000 candidates. Unretrievable positives have
stable IDs above9999; predictions stay within0..9999. AP denominator uses the
original positive count, capped at12; users with only unretrievable purchases
receive0, not exclusion. Primary MAP is unconditional. Report conditional catalog
MAP on users with any in-catalog targets as an explicitly separate diagnostic.
No expansion of the catalog based on future labels. There are5519 outer user-times.

Authorized 2026-10-17. Nine methods: manual LightGBM, raw15 LightGBM,
ID-GNN, ContextGNN, pretrained Recformer zero-shot, Recformer LR/warmup,
fixed-tree TDM beam64, API GPT H008 best-only and H009 full own-island history.
No Qwen/Llama calls. This is a larger local benchmark, not paper reproduction.

Dataset: seed42, 20000 users sampled among users active in the90 days ending
2020-06-29, excluding the5000 original small-v1 users. Top10000 items by their
purchase frequency within this cohort in180 days ending2020-06-29.
Membership and ID maps are fixed before the first training cutoff. All source
tables stay untouched. Static H&M metadata is the same supplied snapshot;
historical availability of every static attribute cannot be established.

Three rolling-origin outer tests:2020-08-17,2020-08-31,2020-09-14; weekly labels
are purchases strictly after cutoff through cutoff+7days. Inner validation is
the preceding week. Each fold trains on the preceding SIX weekly cutoffs;
the last training label window ends at the inner-validation cutoff. Known
transactions at/before a prediction cutoff can be used in its history.
Reusing earlier outer-test weeks as later-fold training history is deliberate
online evaluation; model weights and LLM dialogues are reset per fold.
No outer labels/metrics enter selection or prompts. Outer scoring is delayed
until all training/selection finishes. Evaluation uses every source user-time
and all10000 items (TDM beam may prune branches, all leaves remain eligible).
Report lost positive coverage and zero-retrievable-target user-times.
Inference therefore measures this fixed restricted catalog, not full H&M.

All tree models share identical positive and negative train pairs (all positives,
up to8 history negatives +8 uniform, seed2026). Neural models use those same
training user-times and positive labels with their native documented objectives;
their effective sampled examples differ. Primary MAP@12; also recall@12/hit@12,
per-user AP, training/search/inference time and API usage. No adaptive search
based on outer metrics. One fixed model seed42 per fold; this estimates temporal
and user variation, not independent initialization stability.

Inner validation: seeded user partition,60% search,20% confirmation,20% heldout.
Search uses at most256 users for all methods' checkpoint selection; confirmation
chooses between the three best LLM search programs and a constant control.
Heldout is diagnostic only. No automatic raw15 in either H008/H009; explicit
static copies returned by GPT are allowed. Each arm/fold:20 accepted structurally
distinct programs, at most300 actual POST requests,3 repairs,3 isolated islands,
Python modify_features(X, history),36 generated inputs maximum. Best-only vs
full history is the sole planned difference between API arms. Numeric duplicates
are counted separately in the audit. HTTP/provider failures stop that arm and
preserve paid responses for resume. No provider-model identity attestation.

LightGBM:150 rounds,31 leaves,lr.05,4CPU; identical seeds/regularization across
all four tree methods. Manual features are the existing ManualFeatures SQL;
no tuning15/31 leaves, to match the LLM/raw downstream budget.
GNN: existing official classes,64channels,2layers,neighbors32/16,batch128,
lr.001,10 full epochs maximum,patience3. Unlike old pilot, no50step cap.
GNN transaction preprocessing statistics/category mappings fit only on history
at/before the first training cutoff, then transform later visible rows unchanged.
Static attributes use the provided snapshot. All scoring ties use stable item IDs.
Recformer: same pretrained assets,256tokens/50history items,3attributes,
batch4/accum4,FP16,2+2 full epochs,all parameters trainable,peakLR1e-5,
100 successful updates warmup then linear decay across fold-specific updates.
Stage2 starts from stage1 best checkpoint; optimizer/schedule handling remains
as in the existing ablation. Zero-shot weights never selected by outer targets.
TDM: same fixed category initialization,24d,beam64,Adam.001,batch32,
20epochs maximum,patience4,minimum5;30min training/validation ceiling after
minimum5 epochs, declared before seeing results. No cluster/full-search arms.

Validation and outer-test ordering, shapes, IDs, cutoff boundaries and label
windows are checked. API validator regressions must pass before billable calls;
fix the known host hasattr omission equally for both arms. Frozen-model replay
and independent NumPy MAP check are required. Save unique run IDs and source
hashes; keep old runs unchanged. Raw data/cache/weights stay ignored by Git.

Final report: all fold scores, pooled AP and equal-fold mean; paired user-cluster
bootstrap (resample original customers, retaining their observations across folds),
paired differences and descriptive95% intervals. Also show three individual
fold differences; with only3 time blocks no strong time-generalization claim.
Exploratory all-pair tests use Holm correction and are explicitly exploratory.
Do not force an idea into good/bad if differences are small or inconsistent.
