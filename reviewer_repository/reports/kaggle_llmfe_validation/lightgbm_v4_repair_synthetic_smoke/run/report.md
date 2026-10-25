# SYNTHETIC SMOKE — not Llama results

This report tests software using a synthetic generator and tiny data. No real Llama inference or quality experiment.

# Llama3.1-8B → Python features → LightGBM: bounded H&M

Adaptation of LLM-FE; not a numerical reproduction of the paper. All MAP values in percent.
One seed42,180-day selected-cohort history, frozen shared ID-GNN pools.
LightGBM selects features throughout search and confirmation; all new trees use identical803377 training pairs.
Manual and GNN→LightGBM references use those same803377 supervised pairs and these exact evaluation rows/pools.
Tuning protocols, derived seeds and historical representations differ; GNN also used upstream graph training.
Compare pipeline quality on this subset, not differences in isolated feature quality or full-dataset MAP.
Selection uses only search256 + confirmation512; heldout val1024 and test2048 used after freezing.
Native ID-GNN reference used more training data and is contextual, not a matched-budget comparison.
LLM calls6/10; evaluated distinct2/2; target met: True. Raw control selected: True.
All raw/LLM heldout predictions reproduced from saved models in separate CPU processes with1 thread.

| Model | Validation MAP, % | Test MAP, % |
|---|---:|---:|
| Raw LightGBM | 0.00000 | 6.25000 |
| LLM-FE LightGBM | 0.00000 | 6.25000 |
| Manual features → LightGBM | 0.00000 | 3.12500 |
| GNN → LightGBM | 0.00000 | 3.12500 |
| ID-GNN (graph training budget) | 0.00000 | 6.25000 |

Selected program: `raw_control/program.py`.
![MAP](comparison.png)
![AP](ap_histograms.png)
![Paired](paired_comparison.png)
![Search](search_progress.png)
![Training](training_and_rejections.png)
![LightGBM](lightgbm_comparison.png)