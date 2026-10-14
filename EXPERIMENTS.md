# Эксперименты и результаты

MAP@12 указан в процентах. Smoke не является оценкой на полном датасете.

Опубликованный RelBench ID-GNN: validation 2.64%, test 2.81% (пять запусков).

| Запуск | Статус | Эпоха | Validation MAP, % | Test MAP, % | Артефакты |
|---|---|---:|---:|---:|---|
| hm_data_snapshot_v1 | complete | — | — | — | data/download_manifest.json |
| hm_global_popularity_v1 | complete | — | 0.35739 | 0.30456 | baseline/results/simple_metrics.json |
| hm_past_visit_v1 | complete | — | 0.78166 | 0.79466 | baseline/results/simple_metrics.json |
| hm_idgnn_last_seed_42_v1 | complete | 20 | 2.63442 | 2.78432 | RelBenchGNN/results/seed_42 |
| hm_idgnn_last_seed_43_v1 | cancelled | 0 | — | — | RelBenchGNN/results/seed_43 |
| hm_idgnn_last_seed_44_v1 | cancelled | — | — | — | RelBenchGNN/results/seed_44 |
| hm_idgnn_last_seed_45_v1 | cancelled | — | — | — | RelBenchGNN/results/seed_45 |
| hm_idgnn_last_seed_46_v1 | cancelled | — | — | — | RelBenchGNN/results/seed_46 |
| hm_idgnn_smoke_v1 | smoke_complete | — | 0.00000 | 3.78788 | RelBenchGNN/results/smoke |
| hm_reproduction_pipeline_v1 | complete | — | — | — | RelBenchGNN/logs |
| hm_visual_report_v1 | complete | — | — | — | reports/relbench_hm_v1/report.md |
| hm_postprocess_v1 | complete | — | — | — | reports/relbench_hm_v1/report.md |
| hm_manual_tree_pipeline_v1 | complete | — | — | — | baseline/results/manual_v1 |
| hm_decision_tree_manual_seed_42_v1 | complete | — | 1.87661 | 2.04076 | baseline/results/manual_v1/decision_tree/seed_42 |
| hm_decision_tree_manual_seed_43_v1 | cancelled | — | — | — | baseline/results/manual_v1/decision_tree/seed_43 |
| hm_decision_tree_manual_seed_44_v1 | cancelled | — | — | — | baseline/results/manual_v1/decision_tree/seed_44 |
| hm_decision_tree_manual_seed_45_v1 | cancelled | — | — | — | baseline/results/manual_v1/decision_tree/seed_45 |
| hm_decision_tree_manual_seed_46_v1 | cancelled | — | — | — | baseline/results/manual_v1/decision_tree/seed_46 |
| hm_lightgbm_manual_seed_42_v1 | complete | — | 2.09318 | 2.26608 | baseline/results/manual_v1/lightgbm/seed_42 |
| hm_lightgbm_manual_seed_43_v1 | cancelled | — | — | — | baseline/results/manual_v1/lightgbm/seed_43 |
| hm_lightgbm_manual_seed_44_v1 | cancelled | — | — | — | baseline/results/manual_v1/lightgbm/seed_44 |
| hm_lightgbm_manual_seed_45_v1 | cancelled | — | — | — | baseline/results/manual_v1/lightgbm/seed_45 |
| hm_lightgbm_manual_seed_46_v1 | cancelled | — | — | — | baseline/results/manual_v1/lightgbm/seed_46 |
| hm_idgnn_last_summary_v1 | complete | — | 2.63442 | 2.78432 | RelBenchGNN/results/summary.json |
| hm_idgnn_last_seed_42_inference_v1 | verified | — | 2.63442 | 2.78432 | RelBenchGNN/results/seed_42/inference |
| hm_gnn_embedding_pipeline_v1 | complete | — | — | — | — |
| hm_idgnn_embeddings_seed_42_v1 | complete | — | — | — | baseline/cache/gnn_embeddings_v1/manifest.json |
| hm_idgnn_lightgbm_embeddings_seed_42_v1 | complete | — | 1.97116 | 2.12451 | baseline/results/gnn_embeddings_v1 |
| hm_gnn_embedding_report_v1 | complete | — | — | — | reports/gnn_embeddings_v1 |

Текущая конфигурация и ограничения сравнения: [RelBenchGNN/README.md](RelBenchGNN/README.md).

Новые протоколы должны получать новые run_id. Завершённые результаты сохраняются в истории.
