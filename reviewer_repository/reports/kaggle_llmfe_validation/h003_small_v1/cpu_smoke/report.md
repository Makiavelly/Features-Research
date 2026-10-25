# Qwen7B H003 — small H&M SQL feature search
**CPU SMOKE ONLY: fake H003 responses, not actual LLM performance.**

Same frozen small-v1 data,72813 train pairs,304val/250test users,all5000 catalog items.
All H003 arms use the original local-Qwen SQL JSON interface and NF4/FP16 loading.
Test250 has been inspected in earlier experiments: this is a repeated diagnostic evaluation, not a new untouched test.
Old local Qwen used Q4_K_M/Ollama: this is not byte-identical quantization.
All selections frozen before final test. Same20-success target/300-call cap/3repairs/3islands.
Validation304 includes search/confirmation rows; heldout88 is separate for LLMs.
References selected on original full validation, so their heldout88 is not an untouched selection set.
Baselines have different model tuning/training/pretraining budgets. One seed;250test users.

| Model | Val MAP,% | Test MAP,% |
|---|---:|---:|
| raw_control | 0.97456 | 0.76596 |
| h003a_LightGBM | 0.97456 | 0.76596 |
| h003b_LightGBM | 0.97456 | 0.76596 |
| h003c_LightGBM | 0.97456 | 0.76596 |
| contextgnn | 4.76193 | 3.01558 |
| idgnn | 4.41072 | 2.65341 |
| lightgbm_idgnn | 0.68531 | 0.96667 |
| lightgbm_manual | 0.99832 | 1.23388 |
| recformer_finetuned | 2.47022 | 1.23556 |
| recformer_zero_shot | 2.66996 | 3.30054 |
| two_tower | 1.55256 | 0.68368 |
| popularity | 0.26256 | 0.72645 |

h003a: 2 successful /5 calls; budget_complete=True; selected_call=None (null=raw control).

h003b: 2 successful /5 calls; budget_complete=True; selected_call=None (null=raw control).

h003c: 2 successful /5 calls; budget_complete=True; selected_call=None (null=raw control).

![Comparison](comparison.png)

![Test AP histograms](test_histograms.png)

H003 arms: A=diagnostics; B=A+prompt examples; C=B+duplicate/unchanged policy.
Compare each adjacent variant, and A to the previous archived Qwen7B control.
The same previously inspected test is reused diagnostically, never to select variants.
See generation_efficiency.csv and generation_efficiency.png.
