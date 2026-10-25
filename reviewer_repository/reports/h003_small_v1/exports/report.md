# Qwen7B H003 — small H&M SQL feature search

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
| raw_control | 0.43442 | 0.95963 |
| h003a_LightGBM | 0.64219 | 0.75121 |
| h003b_LightGBM | 0.71267 | 0.87359 |
| h003c_LightGBM | 0.84142 | 0.88874 |
| contextgnn | 4.76193 | 3.01558 |
| idgnn | 4.41072 | 2.65341 |
| lightgbm_idgnn | 0.68531 | 0.96667 |
| lightgbm_manual | 0.99832 | 1.23388 |
| recformer_finetuned | 2.47022 | 1.23556 |
| recformer_zero_shot | 2.66996 | 3.30054 |
| two_tower | 1.55256 | 0.68368 |
| popularity | 0.26256 | 0.72645 |

h003a: 20 successful /65 calls; budget_complete=True; selected_call=58 (null=raw control).

h003b: 20 successful /78 calls; budget_complete=True; selected_call=31 (null=raw control).

h003c: 20 successful /51 calls; budget_complete=True; selected_call=8 (null=raw control).

![Comparison](comparison.png)

![Test AP histograms](test_histograms.png)

H003 arms: A=diagnostics; B=A+prompt examples; C=B+duplicate/unchanged policy.
Compare each adjacent variant, and A to the previous archived Qwen7B control.
The same previously inspected test is reused diagnostically, never to select variants.
See generation_efficiency.csv and generation_efficiency.png.
