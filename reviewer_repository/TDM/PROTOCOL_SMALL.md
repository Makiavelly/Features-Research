# TDM small-v1: fixed tree and embedding-cluster tree

Authorized 2026-10-16. This is a local PyTorch adaptation, not an unchanged
TorchEasyRec execution or reproduction of paper metrics. No dependency changes.
Algorithm references and pinned inspected upstream: reports/tdm_assessment/.

Runs: hm_tdm_small_fixed_seed42_v1, hm_tdm_small_cluster_seed42_v1.
Separate smoke: hm_tdm_small_smoke_v1. Pipeline: hm_tdm_small_pipeline_v1.

Frozen data/rel-hm-small-v1: all 10 manifest files checked by SHA256, 4804
train / 304 validation / 250 test user-times, full 5000-item catalog. Repeat
purchases allowed. Histories use t_dat<=timestamp, stable source order for
same-day transactions, latest 50 purchases in reverse chronological order.
No targets enter histories. Model/tree training uses train targets only.

History-only model: shared node embeddings24d, padding ID0 distinct from all
items (original article_id0 is mapped to a nonzero leaf). Candidate-conditioned
attention [history,history*candidate,candidate] -> Linear72/36,PReLU,
Linear36/1,PReLU. Weighted mean within positional windows
[1,1,1,2,2,2,5,6,10,20], concatenate candidate -> MLP128/64/24 with
BatchNorm/PReLU, scalar logit. Single-logit BCE is equivalent to binary
classification, but is an explicit adaptation from upstream two-class head.
No pretrained weights, text encoder, GNN, manual aggregates or LLM features.
Functional attention pooling matches the inspected MultiWindowDIN computation;
local tensor implementation and loader/sampler/tree/search are ours.

Balanced binary category initialization: product_type_no; shuffled category
order and shuffled items within categories, seed42, recursive equal-size split.
Short leaves extended down unary paths to common depth13; missing children
masked, no dummy item predictions. Internal IDs follow heap numbering, root1.
Every item has exactly one valid leaf; all 5000 leaves reachable.

Weekly objective: for every user-time and non-root level, positive nodes are
the UNIQUE ancestors of ALL weekly positive items. Sample up to8 distinct
other nodes of that level without replacement; never sample ANY positive
ancestor. Level loss=.5*mean positive BCE+.5*mean negative BCE when negatives
exist, otherwise mean positive BCE. Average equally over13levels and user-times.
This balanced multi-positive loss is our specified weekly adaptation.
Old72813binary-pair caches are not used. Sampling on CPU seed42+epoch.

Adam lr.001, batch32user-times, FP32, gradient clip5, seed42, deterministic
PyTorch algorithms, 4CPUthreads. Pair forwards chunked at512, gradients sum
weighted losses before optimizer step. BatchNorm sees pair chunks in training.
Up to20 full epochs; patience4 after at least5epochs, best by validation
beam64 MAP@12. Do not begin another epoch after minimum5 if elapsed plus last
epoch exceeds15minutes per model. Strict improvement; ties keep earlier best.
Final epoch/stop reason recorded. No resume/retrain over completed runs.

Native retrieval: beam64 at every internal level, final leaves sorted by
logit descending/article_id ascending; return12. Evaluation also scores all
5000 leaves with the SAME weights and tree, sorted identically. Full-leaf
result is a diagnostic, never a separate checkpoint selection criterion.
No candidate restriction from IDGNN. Beam width fixed before seeing metrics.

Cluster stage: use trained fixed-tree best checkpoint's own leaf embeddings;
recursive KMeans2 (seed42,n_init10), split half by distance-to-centroid0 minus
distance-to-centroid1 (stable item-ID ties), balancing each split. This explicit
balanced split is our adaptation, not JTM. Tree frozen before clustered model
training, with saved source-checkpoint SHA. Train clustered model FROM SCRATCH
seed42, same hyperparameters and selection budget; not warm-started.
Training sample pairs differ because the tree changes. Report tree construction
and full first-stage prerequisite cost separately. Cold-item assignment is
deterministic but may depend on untrained initial embeddings; coverage reported.

Train/validation select BOTH models before evaluating either on test; save
selection_pretest.json. Four evaluations/model: beam/full ×val/test. Save all
leaf score matrices, retrieved node traces/scores, top12, per-user AP, user/time
order, timings, visited nodes, unique item coverage and CUDA memory. Frozen
checkpoint includes tree and SHA, full config and encoder state. Separate
Python process repeats all8evaluations and verifies scores/top12/AP exactly.
Independent NumPy MAP calculation checked against RelBench evaluator.
Paired-user bootstrap95% describes fixed models on250testusers/one seed;
it does not establish training-seed stability. Old results untouched.
