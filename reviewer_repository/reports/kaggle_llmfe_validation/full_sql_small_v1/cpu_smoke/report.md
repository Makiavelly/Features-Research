# Qwen7B full SQL — small H&M SQL feature search
**CPU SMOKE ONLY: scripted SQL responses, not actual LLM performance.**

Same frozen small-v1 data,72813 train pairs,304val/250test users,all5000 catalog items.
Qwen7B returns complete SELECT scripts; NF4/FP16 loading matches the control.
Test250 has been inspected in earlier experiments: this is a repeated diagnostic evaluation, not a new untouched test.
Old local Qwen used Q4_K_M/Ollama: this is not byte-identical quantization.
All selections frozen before final test. Same20-success target/300-call cap/3repairs/3islands.
Validation304 includes search/confirmation rows; heldout88 is separate for LLMs.
References selected on original full validation, so their heldout88 is not an untouched selection set.
Baselines have different model tuning/training/pretraining budgets. One seed;250test users.

| Model | Val MAP,% | Test MAP,% |
|---|---:|---:|
| raw_control | 0.43442 | 0.95963 |
| qwen_full_sql_LightGBM | 0.49581 | 0.66519 |
| contextgnn | 4.76193 | 3.01558 |
| idgnn | 4.41072 | 2.65341 |
| lightgbm_idgnn | 0.68531 | 0.96667 |
| lightgbm_manual | 0.99832 | 1.23388 |
| recformer_finetuned | 2.47022 | 1.23556 |
| recformer_zero_shot | 2.66996 | 3.30054 |
| two_tower | 1.55256 | 0.68368 |
| popularity | 0.26256 | 0.72645 |

qwen_full_sql: 2 successful /5 calls; budget_complete=True; selected_call=5 (null=raw control).

![Comparison](comparison.png)

![Test AP histograms](test_histograms.png)

Full SQL: ordinary SELECT/WITH scripts with host-owned candidate joins.
Compare locally to archived Qwen7B and H003; SQL interface/dedup semantics differ.
The same previously inspected test is reused diagnostically, never to select variants.
See generation_efficiency.csv and generation_efficiency.png.
