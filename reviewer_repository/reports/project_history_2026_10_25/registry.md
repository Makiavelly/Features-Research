# Все зарегистрированные этапы на момент обзора

Снимок до регистрации обзора: 323 записей / 3826 событий. Это не число независимых обучений.

Статусы и стандартные MAP перенесены из state.json без исправления истории. Последний статус события взят из events.jsonl. Пустое поле означает отсутствие записи, а не нулевой результат. Наличие пути не доказывает полноту его содержимого. Вложенные MAP изолированного опыта показаны отдельно и известны только из журнала.

[Основной отчёт](report_ru.md) · [CSV со всеми полями](runs.csv)

| Run ID | Реестр / последнее статусное событие | Val MAP, % | Test MAP, % | Артефакт существует | Примечание |
|---|---|---:|---:|---|---|
| hm_data_snapshot_v1 | complete | — | — | True |  |
| hm_global_popularity_v1 | complete | 0.35739 | 0.30456 | True |  |
| hm_past_visit_v1 | complete | 0.78166 | 0.79466 | True |  |
| hm_idgnn_last_seed_42_v1 | complete | 2.63442 | 2.78432 | True |  |
| hm_idgnn_last_seed_43_v1 | cancelled | — | — | True |  |
| hm_idgnn_last_seed_44_v1 | cancelled | — | — | False |  |
| hm_idgnn_last_seed_45_v1 | cancelled | — | — | False |  |
| hm_idgnn_last_seed_46_v1 | cancelled | — | — | False |  |
| hm_idgnn_smoke_v1 | smoke_complete | 0.00000 | 3.78788 | True | Smoke, не итог качества |
| hm_reproduction_pipeline_v1 | complete | — | — | True |  |
| hm_visual_report_v1 | complete | — | — | True |  |
| hm_postprocess_v1 | complete | — | — | True |  |
| hm_manual_tree_pipeline_v1 | complete | — | — | True |  |
| hm_decision_tree_manual_seed_42_v1 | complete | 1.87661 | 2.04076 | True |  |
| hm_decision_tree_manual_seed_43_v1 | cancelled | — | — | False |  |
| hm_decision_tree_manual_seed_44_v1 | cancelled | — | — | False |  |
| hm_decision_tree_manual_seed_45_v1 | cancelled | — | — | False |  |
| hm_decision_tree_manual_seed_46_v1 | cancelled | — | — | False |  |
| hm_lightgbm_manual_seed_42_v1 | complete | 2.09318 | 2.26608 | True |  |
| hm_lightgbm_manual_seed_43_v1 | cancelled | — | — | False |  |
| hm_lightgbm_manual_seed_44_v1 | cancelled | — | — | False |  |
| hm_lightgbm_manual_seed_45_v1 | cancelled | — | — | False |  |
| hm_lightgbm_manual_seed_46_v1 | cancelled | — | — | False |  |
| hm_idgnn_last_summary_v1 | complete | 2.63442 | 2.78432 | True |  |
| hm_idgnn_last_seed_42_inference_v1 | verified | 2.63442 | 2.78432 | True |  |
| hm_gnn_embedding_pipeline_v1 | complete | — | — | unknown |  |
| hm_idgnn_embeddings_seed_42_v1 | complete | — | — | True |  |
| hm_idgnn_lightgbm_embeddings_seed_42_v1 | complete | 1.97116 | 2.12451 | True |  |
| hm_gnn_embedding_report_v1 | complete | — | — | True |  |
| hm_twotower_sage_smoke_v1 | smoke_complete | 0.00000 | 0.00000 | True | Smoke, не итог качества |
| hm_twotower_pipeline_v1 | complete | — | — | unknown |  |
| hm_twotower_report_v1 | complete | — | — | True |  |
| hm_twotower_sage_smoke_v1_inference | verified | — | — | True | Smoke, не итог качества |
| hm_twotower_sage_seed_42_v1 | complete | 0.57431 | 0.54301 | True |  |
| hm_twotower_sage_seed_42_v1_inference | failed | — | — | True |  |
| hm_twotower_sage_seed_42_v1_inference_v2 | verified | — | — | True |  |
| hm_llmfe_qwen25coder7b_seed42_v1 | evaluating | — | — | True | В истории есть superseded; реестр позднее показывает evaluating; Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_llmfe_qwen25coder7b_seed42_v2 | paused | — | — | True |  |
| hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1 | complete | 0.85428 | 0.81175 | True |  |
| hm_llmfe_qwen25coder7b_seed42_h002_shared_v1 | complete | 1.78605 | 1.97540 | True |  |
| hm_llmfe_llama31_8b_kaggle_fulltrain_v2 | notebook_ready | — | — | True |  |
| hm_llmfe_llama31_8b_lightgbm_fulltrain_v3 | notebook_ready | — | — | unknown |  |
| hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4 | notebook_ready | — | — | True |  |
| hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141 | audited_no_llm_result | — | — | True |  |
| hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5 | notebook_ready | — | — | True |  |
| hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef | complete_with_alignment_bug | 0.97730 | 0.73457 | True | Alignment bug: не оценка корректных исторических признаков |
| hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1 | notebook_ready | — | — | unknown |  |
| hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1_6eb8a9ef9ba7 | stopped_by_user | — | — | unknown |  |
| hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1 | notebook_ready | — | — | unknown |  |
| balance_scale_llama31_diagnostic_v1 | notebook_ready | — | — | unknown |  |
| balance_scale_llama31_diagnostic_v1_09de7191636d | failed_before_llm | — | — | unknown |  |
| balance_scale_llama31_diagnostic_v2_cpu | notebook_ready | — | — | unknown |  |
| balance_scale_llama31_diagnostic_v2_cpu_6b5c7786f4b5 | diagnostic_complete | — | — | unknown |  |
| hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1 | notebook_ready | — | — | unknown |  |
| hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1_aa1ed17300ae | complete | 0.74474 | 0.80095 | True |  |
| hm_small_data_v1 | complete | — | — | True |  |
| hm_contextgnn_small_pipeline_v1 | complete | — | — | True |  |
| hm_idgnn_small_seed_42_v1 | complete | 4.41072 | 2.65341 | True |  |
| hm_contextgnn_small_seed_42_v1 | complete | 4.76193 | 3.01558 | True |  |
| hm_small_manual_features_v1 | complete | — | — | True |  |
| hm_idgnn_small_seed_42_v1_inference | verified | — | — | unknown |  |
| hm_contextgnn_small_seed_42_v1_inference | verified | — | — | unknown |  |
| hm_small_idgnn_features_v1 | features | — | — | unknown |  |
| hm_small_lightgbm_manual_seed_42_v1 | complete | 0.99832 | 1.23388 | True |  |
| hm_small_lightgbm_idgnn_seed_42_v1 | complete | 0.68531 | 0.96667 | True |  |
| hm_twotower_small_seed_42_v1 | complete | 1.55256 | 0.68368 | True |  |
| hm_twotower_small_seed_42_v1_inference | verified | — | — | True |  |
| hm_small_comparison_v1 | complete | — | — | unknown |  |
| hm_recformer_small_seed42_v1 | complete | — | — | True |  |
| hm_recformer_small_smoke_v1 | smoke_complete | — | — | unknown | Smoke, не итог качества |
| hm_recformer_small_seed42_v1_zero_shot | complete | 2.66996 | 3.30054 | True |  |
| hm_recformer_small_seed42_v1_finetuned | complete | 2.47022 | 1.23556 | True |  |
| hm_recformer_small_seed42_v1_inference | verified | — | — | unknown |  |
| hm_small_qwen_llama_sql_v1 | completed_on_kaggle_audited | — | — | True |  |
| hm_recformer_ablations_v1 | complete | — | — | True |  |
| hm_recformer_small_low_lr_warmup_seed42_v1 | complete | 3.55434 | 3.85751 | True |  |
| hm_recformer_small_freeze_lower6_seed42_v1 | complete | 1.98481 | 1.76156 | True |  |
| hm_recformer_small_low_lr_warmup_seed42_v1_zero_shot | measured_pending_verification | 2.66996 | 3.30054 | True |  |
| hm_recformer_small_low_lr_warmup_seed42_v1_finetuned | measured_pending_verification | 3.55434 | 3.85751 | True |  |
| hm_recformer_small_low_lr_warmup_seed42_v1_inference | verified | — | — | unknown |  |
| hm_recformer_small_freeze_lower6_seed42_v1_zero_shot | measured_pending_verification | 2.66996 | 3.30054 | True |  |
| hm_recformer_small_freeze_lower6_seed42_v1_finetuned | measured_pending_verification | 1.98481 | 1.76156 | True |  |
| hm_recformer_small_freeze_lower6_seed42_v1_inference | verified | — | — | unknown |  |
| hm_recformer_small_long_floor_seed42_v1 | complete | 3.57807 | 3.43889 | True |  |
| hm_recformer_small_long_floor_seed42_v1_zero_shot | complete | 2.66996 | 3.30054 | True |  |
| hm_recformer_small_long_floor_seed42_v1_short_2plus2 | complete | 3.57807 | 3.43889 | True |  |
| hm_recformer_small_long_floor_seed42_v1_finetuned | complete | 3.57807 | 3.43889 | True |  |
| hm_recformer_small_long_floor_seed42_v1_inference | verified | — | — | unknown |  |
| hm_small_qwen14b_sql_v1 | completed_on_kaggle_audited | — | — | True |  |
| hm_tdm_small_smoke_v1 | smoke_complete | — | — | unknown | Smoke, не итог качества |
| hm_tdm_small_fixed_seed42_v1 | complete | 1.01601 | 1.39519 | True |  |
| hm_tdm_small_cluster_seed42_v1 | complete | 0.74588 | 0.55126 | True |  |
| hm_tdm_small_pipeline_v1 | complete | — | — | True |  |
| hm_tdm_small_pipeline_v1_inference | verified | — | — | unknown |  |
| hm_small_qwen_llama_sql_v1_2ecc60d61fd4_qwen | complete | 0.77718 | 1.10714 | True |  |
| hm_small_qwen_llama_sql_v1_2ecc60d61fd4_llama | complete | 0.84396 | 0.78034 | True |  |
| hm_small_qwen14b_sql_v1_f373011050bf | complete | 1.21121 | 0.74331 | True |  |
| hm_small_llms_comparison_v1 | complete | — | — | True |  |
| hm_small_qwen7b_h003_v1_6852748fc0e4_h003a | complete | 0.64219 | 0.75121 | True |  |
| hm_small_qwen7b_h003_v1_6852748fc0e4_h003b | complete | 0.71267 | 0.87359 | True |  |
| hm_small_qwen7b_h003_v1_6852748fc0e4_h003c | complete | 0.84142 | 0.88874 | True |  |
| hm_small_qwen7b_h003_v1_6852748fc0e4 | complete | — | — | True |  |
| hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0 | complete | 0.79144 | 0.97903 | True |  |
| hm_small_gpt61sol_full_sql_corrected_eval_v2_ffbd51c51899 | complete | 0.79144 | 0.97903 | True |  |
| hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1 | superseded_validator_v2 | — | — | True |  |
| hm_small_gpt61sol_python_seed42_v2_db3ced2f4449 | complete | 1.07971 | 1.35736 | True |  |
| hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9 | complete | 1.26060 | 2.23103 | True |  |
| hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde | complete | 1.47856 | 1.42676 | True |  |
| isolated_hm_20261017_venvwsl_v1 | completed | 2.28082 (журнал) | 2.43712 (журнал) | False | MAP из вложенного metrics; локальный report отсутствует |
| hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0 | complete | 2.28699 | 0.72160 | True |  |
| hm_medium_temporal_cv_v1 | deferred_by_user | — | — | True |  |
| hm_medium_temporal_cv_v2 | complete | — | — | True |  |
| hm_medium_cv_v2_fold0_gnn | complete | — | — | True |  |
| hm_medium_cv_v2_fold0_manual | complete | — | 0.25060 | True |  |
| hm_medium_cv_v2_fold0_raw15 | complete | — | 0.19724 | True |  |
| hm_medium_cv_v2_fold0_h008 | complete | — | 0.52264 | True |  |
| hm_medium_cv_v2_fold0_idgnn | complete | 0.07595 | 0.00000 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold0_contextgnn | complete | 0.29579 | 0.03091 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold0_tdm_fixed | complete | 0.61198 | 0.19526 | True |  |
| hm_medium_cv_v2_fold0_recformer | complete | — | — | True |  |
| hm_medium_cv_v2_fold0_h009 | complete | — | 0.46406 | True |  |
| hm_medium_cv_v2_fold1_manual | complete | — | 0.41278 | True |  |
| hm_medium_cv_v2_fold1_raw15 | complete | — | 0.12659 | True |  |
| hm_medium_cv_v2_fold1_h008 | complete | — | 0.44389 | True |  |
| hm_medium_cv_v2_fold1_gnn | complete | — | — | True |  |
| hm_medium_cv_v2_fold1_idgnn | complete | 0.06665 | 0.04779 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold1_contextgnn | complete | 0.16121 | 0.04727 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold1_tdm_fixed | complete | 0.46179 | 0.15955 | True |  |
| hm_medium_cv_v2_fold1_recformer | complete | — | — | True |  |
| hm_medium_cv_v2_fold1_h009 | complete | — | 0.38667 | True |  |
| hm_medium_cv_v2_fold2_manual | complete | — | 0.37554 | True |  |
| hm_medium_cv_v2_fold2_raw15 | complete | — | 0.09852 | True |  |
| hm_medium_cv_v2_fold2_h008 | complete | — | 0.41977 | True |  |
| hm_medium_cv_v2_fold2_gnn | complete | — | — | True |  |
| hm_medium_cv_v2_fold2_idgnn | complete | 0.04526 | 0.02372 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold2_contextgnn | complete | 0.01953 | 0.00049 | True | Историческая medium GNN: метрики невалидны (ms/ns); см. corrected refit |
| hm_medium_cv_v2_fold2_tdm_fixed | complete | 0.65912 | 0.29624 | True |  |
| hm_medium_cv_v2_fold2_recformer | complete | — | — | True |  |
| hm_medium_cv_v2_fold2_h009 | complete | — | 0.51340 | True |  |
| hm_medium_cv_v2_fold0_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold0_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold0_recformer_zero_shot | complete | 0.81539 | 0.86130 | True |  |
| hm_medium_cv_v2_fold0_recformer_finetuned | complete | 0.54243 | 0.49283 | True |  |
| hm_medium_cv_v2_fold0_recformer_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold1_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold1_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold1_recformer_zero_shot | complete | 0.21577 | 0.46644 | True |  |
| hm_medium_cv_v2_fold1_recformer_finetuned | complete | 0.17869 | 0.37842 | True |  |
| hm_medium_cv_v2_fold1_recformer_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold2_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold2_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_cv_v2_fold2_recformer_zero_shot | complete | 0.45030 | 0.56600 | True |  |
| hm_medium_cv_v2_fold2_recformer_finetuned | complete | 0.91541 | 0.49529 | True |  |
| hm_medium_cv_v2_fold2_recformer_inference | verified | — | — | unknown |  |
| hm_medium_followup_api_budget_v1 | complete | — | — | True |  |
| hm_medium_followup_f0_h008_budget30_seed42_v1 | evaluated_verified | — | 0.44755 | True |  |
| hm_followup_context_f0_probe_gnn | preparing | — | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_followup_context_0_probe_v1 | diagnostic_complete | — | — | True |  |
| hm_medium_followup_f0_gnn_timefix_existing_gnn | preparing | — | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_gnn_timefix_v1 | evaluated_pending_report | — | — | True |  |
| hm_medium_followup_f0_gnn_timefix_existing_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f0_gnn_timefix_existing_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_gnn_timefix_existing_f0_v1 | diagnostic_verified | — | — | True |  |
| hm_medium_followup_f0_gnn_timefix_refit_gnn | preparing | — | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_non_gnn_time_audit_v1 | verified | — | — | True |  |
| hm_medium_followup_f0_gnn_timefix_refit_idgnn | training | 1.76792 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f0_gnn_timefix_refit_contextgnn | training | 1.19911 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f1_gnn_timefix_refit_gnn | preparing | — | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f1_gnn_timefix_refit_idgnn | training | 0.48292 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f1_gnn_timefix_refit_contextgnn | training | 0.19206 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f2_gnn_timefix_refit_gnn | failed | — | — | unknown |  |
| hm_medium_followup_f2_gnn_timefix_refit_idgnn | training | 1.84281 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_recovery_v1 | resuming | — | — | True | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f2_gnn_timefix_refit_contextgnn | training | 1.21791 | — | unknown | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_followup_f0_gnn_timefix_refit_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f0_gnn_timefix_refit_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f1_gnn_timefix_refit_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f1_gnn_timefix_refit_contextgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f0_h008_budget40_seed42_v1 | evaluated_verified | — | 0.44755 | True |  |
| hm_medium_followup_f2_gnn_timefix_refit_idgnn_inference | verified | — | — | unknown |  |
| hm_medium_followup_f2_gnn_timefix_refit_contextgnn_inference | failed | — | — | unknown |  |
| hm_medium_gpu_followup_v1 | interrupted | — | — | unknown |  |
| hm_medium_recformer_grid_seed42_v1 | closed_available_summary | — | — | True |  |
| hm_medium_recformer_tune_f0_lr1e6_w100_seed42_v1 | trained_pending_evaluation | — | — | unknown |  |
| hm_medium_followup_report_gnn_v1 | verified_report | — | — | True |  |
| hm_medium_followup_f0_h009_budget30_seed42_v1 | evaluated_verified | — | 0.46406 | True |  |
| hm_medium_followup_f0_h009_budget40_seed42_v1 | evaluated_verified | — | 0.46406 | True |  |
| hm_medium_followup_f1_h008_budget30_seed42_v1 | evaluated_verified | — | 0.44389 | True |  |
| hm_medium_recformer_tune_f1_lr1e6_w100_seed42_v1 | trained_pending_evaluation | — | — | unknown |  |
| hm_medium_followup_f1_h008_budget40_seed42_v1 | evaluated_verified | — | 0.44389 | True |  |
| hm_medium_recformer_kaggle_split_v1 | prepared_verified | — | — | True |  |
| hm_medium_followup_f1_h009_budget30_seed42_v1 | evaluated_verified | — | 0.38667 | True |  |
| hm_medium_recformer_distributed_v1 | closed_available_summary | — | — | True |  |
| hm_medium_recformer_tune_f2_lr1e6_w100_seed42_v1 | trained_pending_evaluation | — | — | unknown |  |
| hm_medium_followup_f1_h009_budget40_seed42_v1 | evaluated_verified | — | 0.38667 | True |  |
| hm_medium_recformer_tune_f0_lr3e6_w300_seed42_v1 | evaluated_verified | 0.79357 | 0.58607 | True |  |
| hm_medium_recformer_tune_f1_lr3e6_w300_seed42_v1 | evaluated_verified | 0.30049 | 0.44499 | True |  |
| hm_medium_followup_f2_h008_budget30_seed42_v1 | evaluated_verified | — | 0.41977 | True |  |
| hm_medium_recformer_tune_f2_lr3e6_w300_seed42_v1 | evaluated_verified | 1.05128 | 0.67243 | True |  |
| hm_medium_followup_f2_h008_budget40_seed42_v1 | evaluated_verified | — | 0.41977 | True |  |
| hm_medium_followup_f2_h009_budget30_seed42_v1 | evaluated_verified | — | 0.42717 | True |  |
| hm_medium_followup_f2_h009_budget40_seed42_v1 | evaluated_verified | — | 0.54653 | True |  |
| hm_medium_recformer_import_lr1e5_w300_v1 | trained_pending_selection | — | — | unknown |  |
| hm_medium_followup_available_summary_v1 | complete_available_summary | — | — | True |  |
| hm_medium_recformer_tune_f0_lr3e6_w300_seed42_v1_zero_shot | measured_pending_verification | 0.81539 | 0.86130 | True |  |
| hm_medium_recformer_tune_f0_lr3e6_w300_seed42_v1_finetuned | measured_pending_verification | 0.79357 | 0.58607 | True |  |
| hm_medium_recformer_tune_f0_lr3e6_w300_seed42_v1_inference | verified | — | — | unknown |  |
| hm_medium_recformer_tune_f1_lr3e6_w300_seed42_v1_zero_shot | measured_pending_verification | 0.21577 | 0.46644 | True |  |
| hm_medium_recformer_tune_f1_lr3e6_w300_seed42_v1_finetuned | measured_pending_verification | 0.30049 | 0.44499 | True |  |
| hm_medium_recformer_tune_f1_lr3e6_w300_seed42_v1_inference | verified | — | — | unknown |  |
| hm_medium_recformer_tune_f2_lr3e6_w300_seed42_v1_zero_shot | measured_pending_verification | 0.45030 | 0.56600 | True |  |
| hm_medium_recformer_tune_f2_lr3e6_w300_seed42_v1_finetuned | measured_pending_verification | 1.05128 | 0.67243 | True |  |
| hm_medium_recformer_tune_f2_lr3e6_w300_seed42_v1_inference | verified | — | — | unknown |  |
| hm_medium_followup_report_all_v1 | report_generated_pending_visual_review | — | — | True |  |
| hm_medium_followup_f0_h008_budget20_seed42_v1 | evaluated_verified | — | 0.52264 | True |  |
| hm_medium_followup_f0_h009_budget20_seed42_v1 | evaluated_verified | — | 0.46406 | True |  |
| hm_medium_followup_f1_h008_budget20_seed42_v1 | evaluated_verified | — | 0.44389 | True |  |
| hm_medium_followup_f1_h009_budget20_seed42_v1 | evaluated_verified | — | 0.38667 | True |  |
| hm_medium_followup_f2_h008_budget20_seed42_v1 | evaluated_verified | — | 0.41977 | True |  |
| hm_medium_followup_f2_h009_budget20_seed42_v1 | evaluated_verified | — | 0.51340 | True |  |
| hm_medium_h010_research_seed42_v1 | stopped_incomplete | — | — | True |  |
| hm_medium_h010_research_seed42_v1_fold0 | searching | — | — | True | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_h010_research_seed42_v2 | complete | — | 0.42905 | True |  |
| hm_medium_h010_research_seed42_v2_fold0 | evaluated_verified | 0.44276 | 0.42069 | True |  |
| hm_gpt61sol_agent_environment_probe_v1 | probe_recorded | — | — | unknown |  |
| hm_gpt61sol_codex_environment_v1 | complete | — | — | True |  |
| hm_medium_context_first3_seed42_v1 | complete_validation_diagnostics | — | — | True |  |
| hm_medium_context_first3_seed42_v1_fold0_diagnostic | diagnostic_complete | — | — | True |  |
| hm_medium_context_first3_seed42_v1_fold1_diagnostic | diagnostic_complete | — | — | True |  |
| hm_medium_context_first3_seed42_v1_fold2_diagnostic | diagnostic_complete | — | — | True |  |
| hm_medium_context_first3_seed42_v1_fold0_categorical | validation_verified | 1.79408 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold1_categorical | validation_verified | 0.42713 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold2_categorical | validation_verified | 1.77734 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold0_fanout64 | validation_verified | 1.93166 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold1_fanout64 | validation_verified | 0.49189 | — | True |  |
| hm_medium_h011_codex_seed42_v1 | superseded_budget_change | — | — | True |  |
| hm_medium_context_first3_seed42_v1_fold2_fanout64 | validation_verified | 1.73213 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold0_gate | validation_verified | 1.59183 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold1_gate | validation_verified | 0.74110 | — | True |  |
| hm_medium_context_first3_seed42_v1_fold2_gate | validation_verified | 1.81988 | — | True |  |
| hm_medium_h010_research_seed42_v2_fold1 | evaluated_verified | 0.37465 | 0.33242 | True |  |
| hm_medium_context_combined_seed42_v1 | complete_validation_comparison | — | — | True |  |
| hm_medium_context_combined_seed42_v1_fold0_combined | validation_verified | 1.80842 | — | True |  |
| hm_medium_context_combined_seed42_v1_fold1_combined | validation_verified | 0.67809 | — | True |  |
| hm_medium_context_combined_seed42_v1_fold2_combined | validation_verified | 1.87165 | — | True |  |
| hm_medium_context_combined_test_seed42_v1 | complete_verified_plot | — | 1.17660 | True |  |
| hm_medium_context_combined_test_seed42_v1_fold0 | test_verified | — | 1.19423 | True |  |
| hm_medium_context_combined_test_seed42_v1_fold1 | test_verified | — | 1.05757 | True |  |
| hm_medium_context_combined_test_seed42_v1_fold2 | test_verified | — | 1.29645 | True |  |
| hm_medium_h010_research_seed42_v2_fold2 | evaluated_verified | 0.56349 | 0.55090 | True |  |
| hm_medium_novelty_audit_seed42_v1 | complete_verified_diagnostics | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_raw15 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_manual | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_tdm | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f1_tdm | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_h008_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_tdm | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_raw15 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f1_raw15 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_h008_30 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f0_h009_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_manual | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f1_manual | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_h008_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f1_h008_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_h009_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f1_h009_20 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_h009_30 | verified | — | — | True |  |
| hm_medium_novelty_audit_seed42_v1_f2_h009_40 | verified | — | — | True |  |
| codex_agent_h011_codex_seed42_v1_fold0 | searching | — | — | True | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_h011_codex_seed42_budget300_v2 | complete | — | 0.43075 | True |  |
| hm_medium_h011_codex_seed42_budget300_v2_fold0 | evaluated_verified | 0.18908 | 0.19520 | True |  |
| hm_medium_h011_codex_seed42_budget300_v2_fold1 | evaluated_verified | 0.62543 | 0.67949 | True |  |
| hm_medium_h011_codex_seed42_budget300_v2_fold2 | evaluated_verified | 0.49535 | 0.39551 | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v1 | stopped_verification_issue | — | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v1_f0_control | training | 1.60255 | — | True | Исторический нетерминальный статус; не подтверждает живой процесс |
| hm_medium_h011_codex_seed42_budget300_v2_search_budget_diagnostic | verified | — | — | True |  |
| hm_medium_all_methods_h011_plot_v1 | complete | — | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v2 | stopped_dispatch_issue | — | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v2_f0_control | validation_verified | 1.85482 | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3 | complete_validation_with_replay_qualification | — | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3_f0_global_ce | validation_verified | 1.95411 | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3_f1_control | validation_verified | 0.58856 | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3_f1_global_ce | validation_verified | 0.67099 | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3_f2_control | validation_verified | 1.98267 | — | True |  |
| hm_medium_context_global_aux_lambda1_seed42_v3_f2_global_ce | validation_verified_qualified | 0.99032 | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1 | complete | — | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h011_20_fold0 | verified | — | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h010_20_fold0 | verified | — | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h010_20_fold1 | verified | — | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h011_20_fold1 | verified | — | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h010_20_fold2 | verified | — | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1 | complete_verified_validation | — | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f0_feature | validation_verified | 1.60015 | — | True |  |
| hm_medium_h010_h011_novelty_seed42_v1_h011_20_fold2 | verified | — | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f1_feature | validation_verified | 0.70196 | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f2_feature | validation_verified | 1.92314 | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f0_similarity_graph | validation_verified | 1.80855 | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f1_similarity_graph | validation_verified | 0.68334 | — | True |  |
| hm_medium_item_encoder_feature_semgraph_seed42_v1_f2_similarity_graph | validation_verified | 1.82633 | — | True |  |
| hm_medium_feature_test_all_methods_seed42_v1 | complete_verified_plot | — | 1.31107 | True |  |
| hm_medium_feature_test_all_methods_seed42_v1_f0 | test_verified | — | 1.39335 | True |  |
| hm_medium_feature_test_all_methods_seed42_v1_f1 | test_verified | — | 1.10907 | True |  |
| hm_medium_feature_test_all_methods_seed42_v1_f2 | test_verified | — | 1.45773 | True |  |
| hm_medium_feature_novelty_plot_seed42_v1 | complete_verified_plot | — | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v1 | stopped_before_training | — | — | unknown |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2 | complete_validation_with_replay_qualification | — | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f0_interest1 | validation_verified | 1.53535 | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f1_interest1 | validation_verified | 0.40303 | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f2_interest1 | validation_verified | 2.02081 | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f0_interest4 | validation_verified | 1.44048 | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f1_interest4 | validation_verified | 0.77153 | — | True |  |
| hm_medium_context_multi_interest_k1_k4_seed42_v2_f2_interest4 | validation_verified | 2.14627 | — | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1 | complete_test_with_replay_qualification | — | — | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f0_control | test_verified | — | 1.27465 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f0_interest1 | test_verified | — | 1.25428 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f0_interest4 | test_verified | — | 1.06905 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f1_control | test_verified | — | 1.09483 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f1_interest1 | test_verified | — | 0.75599 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f1_interest4 | test_verified | — | 0.89842 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f2_control | test_verified | — | 1.11041 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f2_interest1 | test_verified | — | 0.90435 | True |  |
| hm_medium_multi_interest_test_all_methods_seed42_v1_f2_interest4 | test_verified | — | 1.02808 | True |  |
