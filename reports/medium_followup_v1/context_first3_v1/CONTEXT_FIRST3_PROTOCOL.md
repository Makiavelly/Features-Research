# ContextGNN first three checks, v1

Authorized 2026-10-18. Run family: `hm_medium_context_first3_seed42_v1`.
Original corrected GNN checkpoints and their outputs remain immutable.
No provider requests, environment changes or test evaluation.

1. Measure unique sampled article coverage of positive labels, separately for
   all positives and in-catalog positives, on every train and validation row.
   Compare fanouts 32/16 and 64/32, temporal strategy last, two hops, seed42.
   Assert valid epoch-second cutoffs and no future temporal nodes per batch.
   Frozen-weight validation inference at the larger fanout is a sensitivity
   diagnostic, not a model trained for that fanout. Also train a separate 64/32
   arm from scratch, keeping all original features/loss/optimizer settings.
2. Inspect materialized feature types, after removing key columns. The isolated
   categorical ablation changes eight numerical article codes to categorical:
   colour_group_code, department_no, graphical_appearance_no,
   perceived_colour_master_id, perceived_colour_value_id, product_type_no,
   section_no, product_code. Other features and graph structure stay fixed.
   Use new cache, initialization seed42 and the original optimizer, epoch limit,
   validation selection and early stopping. Never reuse old weights with new
   feature encoders. Report as a joint eight-column ablation.
3. Reconstruct global and local logits exactly from corrected saved weights.
   Check original reconstruction against upstream construct_logits. Evaluate
   global-only, original local overwrite and fixed local blend weights .25/.5/.75
   at validation only. These are post-training diagnostics. A separate learned
   gate arm trains from scratch with a per-user sigmoid of projected user
   embedding, 64 zero-initialized weights and bias log(9), initially alpha=.9.
   It mixes global/local scores only at local positions. All other baseline
   settings stay fixed. Gate specification is saved before its first fit.
   Count local share of top12, gained/lost relevant items and helped/hurt users.

Use the original full-target AP denominator, stable item-ID ties and independent
AP verification. Baseline replay must satisfy the already documented FP32
amendment and exact per-user AP. Store per-user predictions/AP and checkpoint
hashes. Do not infer architectural superiority from these exploratory checks.
Training effects require refitting and confirmation on new predeclared weeks.
History uses RelBenchGNN/tracking.py. Existing H010 CPU/API is left untouched.
