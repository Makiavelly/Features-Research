# Текущий статус

Обновлено: 2026-10-16T10:02:46+03:00 (Москва).

Последнее событие: **Получен итог v5 из features-llama-plus-lightgbm-v3.ipynb:20 технически оценённых программ за154 calls,134 отказа. Выбран candidate151, valMAP0.977301%,test0.734573% на общих1024/2048 пользователях. Но обнаружено неверное pandas-сопоставление: groupby Series поarticle_id/customer_id присвоены вRangeIndex F безmap/reindex по ID. Перестановка/разбиение128пар меняют признаки;mean_price неверен у70/128, customer-признаки у52/128. Такой probe провалили кандидаты56,131,147,151. 20 model/program SHA и2 runtimeSHA совпали, независимый replay Raw/selected×val/test точный. Метрики воспроизводимы, но не означают правильные исторические признаки. Никакого ремонта/переобучения или нового выбора поtest не было; исходники/ZIP неизменны. Flat запуск20/23 иtest0.800949% остаётся отдельным экспериментом.**

Статус в файле отражает последнее записанное событие. Проверяйте процесс и логи после перерыва.

| Запуск | Статус | Завершённые эпохи | Текущая эпоха / шаг | Последнее обновление |
|---|---|---:|---|---|
| hm_data_snapshot_v1 | complete | — | — | 2026-10-14T17:23:38+03:00 |
| hm_global_popularity_v1 | complete | — | — | 2026-10-14T17:23:38+03:00 |
| hm_past_visit_v1 | complete | — | — | 2026-10-14T17:23:38+03:00 |
| hm_idgnn_last_seed_42_v1 | complete | 20 | — | 2026-10-14T18:38:23+03:00 |
| hm_idgnn_last_seed_43_v1 | cancelled | 0 | — | 2026-10-14T18:45:02+03:00 |
| hm_idgnn_last_seed_44_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_idgnn_last_seed_45_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_idgnn_last_seed_46_v1 | cancelled | — | — | 2026-10-14T18:45:03+03:00 |
| hm_idgnn_smoke_v1 | smoke_complete | — | — | 2026-10-14T17:23:38+03:00 |
| hm_reproduction_pipeline_v1 | complete | — | — | 2026-10-14T19:47:18+03:00 |
| hm_visual_report_v1 | complete | — | — | 2026-10-14T19:47:18+03:00 |
| hm_postprocess_v1 | complete | — | — | 2026-10-14T19:46:58+03:00 |
| hm_manual_tree_pipeline_v1 | complete | — | — | 2026-10-14T19:46:54+03:00 |
| hm_decision_tree_manual_seed_42_v1 | complete | — | — | 2026-10-14T19:46:10+03:00 |
| hm_decision_tree_manual_seed_43_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_decision_tree_manual_seed_44_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_decision_tree_manual_seed_45_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_decision_tree_manual_seed_46_v1 | cancelled | — | — | 2026-10-14T18:45:03+03:00 |
| hm_lightgbm_manual_seed_42_v1 | complete | — | — | 2026-10-14T19:46:54+03:00 |
| hm_lightgbm_manual_seed_43_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_lightgbm_manual_seed_44_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_lightgbm_manual_seed_45_v1 | cancelled | — | — | 2026-10-14T18:45:02+03:00 |
| hm_lightgbm_manual_seed_46_v1 | cancelled | — | — | 2026-10-14T18:45:03+03:00 |
| hm_idgnn_last_summary_v1 | complete | — | — | 2026-10-14T19:33:00+03:00 |
| hm_idgnn_last_seed_42_inference_v1 | verified | — | — | 2026-10-14T19:36:13+03:00 |
| hm_gnn_embedding_pipeline_v1 | complete | — | — | 2026-10-14T20:36:13+03:00 |
| hm_idgnn_embeddings_seed_42_v1 | complete | — | — | 2026-10-14T20:35:12+03:00 |
| hm_idgnn_lightgbm_embeddings_seed_42_v1 | complete | — | — | 2026-10-14T20:37:32+03:00 |
| hm_gnn_embedding_report_v1 | complete | — | — | 2026-10-14T20:36:12+03:00 |
| hm_twotower_sage_smoke_v1 | smoke_complete | 1 | — | 2026-10-14T21:51:33+03:00 |
| hm_twotower_pipeline_v1 | complete | — | — | 2026-10-15T10:49:10+03:00 |
| hm_twotower_report_v1 | complete | — | — | 2026-10-15T10:49:09+03:00 |
| hm_twotower_sage_smoke_v1_inference | verified | — | — | 2026-10-14T21:53:47+03:00 |
| hm_twotower_sage_seed_42_v1 | complete | 20 | — | 2026-10-15T00:33:29+03:00 |
| hm_twotower_sage_seed_42_v1_inference | failed | — | — | 2026-10-15T00:38:41+03:00 |
| hm_twotower_sage_seed_42_v1_inference_v2 | verified | — | — | 2026-10-15T10:49:01+03:00 |
| hm_llmfe_qwen25coder7b_seed42_v1 | evaluating | — | — | 2026-10-15T12:09:29+03:00 |
| hm_llmfe_qwen25coder7b_seed42_v2 | paused | — | — | 2026-10-15T14:11:31+03:00 |
| hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1 | complete | — | — | 2026-10-15T14:13:38+03:00 |
| hm_llmfe_qwen25coder7b_seed42_h002_shared_v1 | complete | — | — | 2026-10-15T15:39:42+03:00 |
| hm_llmfe_llama31_8b_kaggle_fulltrain_v2 | notebook_ready | — | — | 2026-10-15T15:51:47+03:00 |
| hm_llmfe_llama31_8b_lightgbm_fulltrain_v3 | notebook_ready | — | — | 2026-10-15T16:14:09+03:00 |
| hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4 | notebook_ready | — | — | 2026-10-15T20:03:02+03:00 |
| hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141 | audited_no_llm_result | — | — | 2026-10-15T20:28:19+03:00 |
| hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5 | notebook_ready | — | — | 2026-10-15T20:28:19+03:00 |
| hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef | complete_with_alignment_bug | — | — | 2026-10-16T10:02:46+03:00 |
| hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1 | notebook_ready | — | — | 2026-10-15T21:15:01+03:00 |
| hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1_6eb8a9ef9ba7 | stopped_by_user | — | — | 2026-10-15T21:46:46+03:00 |
| hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1 | notebook_ready | — | — | 2026-10-15T21:47:15+03:00 |
| balance_scale_llama31_diagnostic_v1 | notebook_ready | — | — | 2026-10-15T22:49:57+03:00 |
| balance_scale_llama31_diagnostic_v1_09de7191636d | failed_before_llm | — | — | 2026-10-15T23:20:46+03:00 |
| balance_scale_llama31_diagnostic_v2_cpu | notebook_ready | — | — | 2026-10-15T23:20:48+03:00 |
| balance_scale_llama31_diagnostic_v2_cpu_6b5c7786f4b5 | diagnostic_complete | — | — | 2026-10-15T23:52:44+03:00 |
| hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1 | notebook_ready | — | — | 2026-10-16T00:17:53+03:00 |
| hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1_aa1ed17300ae | complete | — | — | 2026-10-16T09:54:57+03:00 |

Подробности: [контекст](CONTEXT.md), [результаты](EXPERIMENTS.md), [журнал](WORK_LOG.md).
