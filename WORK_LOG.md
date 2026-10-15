# Журнал работы и экспериментов

История добавляется в конец; время московское.

## 2026-10-14T17:23:38+03:00 — context

Добавлен постоянный журнал по просьбе пользователя. Следующие записи фиксируют уже выполненные действия ретроспективно; время — момент записи.

## 2026-10-14T17:23:38+03:00 — setup

Скачаны RelBench и экспертные SQL; создано локальное окружение WSL; unsloth и системный драйвер не изменялись.

```json
{
  "upstream_commit": "919fb8a61a4b4cb787283860597f45701895578d",
  "torch": "2.2.2+cu118",
  "environment": "RelBenchGNN/.venv-wsl",
  "checked_unsloth_torch": "2.5.1+cu121"
}
```

## 2026-10-14T17:23:38+03:00 — compatibility_fix

Исправлена несовместимость PyArrow 26 с NumPy 1.26: установлен PyArrow 15.0.2 и зафиксированы версии научных библиотек.

## 2026-10-14T17:23:38+03:00 — data_download

Локальный H&M скачан, размеры и SHA256 проверены; проверено чтение всех label-таблиц.

Запуск: `hm_data_snapshot_v1`.

```json
{
  "status": "complete",
  "revision": "7abf5d46a48534d918704ca2af278861b932f4dc",
  "files": 18,
  "artifacts": "data/download_manifest.json"
}
```

## 2026-10-14T17:23:38+03:00 — protocol

Выбрано воспроизведение исходного кода с last; статья указывает uniform. Seeds 42..46 выбраны нами. Оценочный batch уменьшен до 128; обучающий 512 сохранён.

```json
{
  "published_val_map_percent": 2.64,
  "published_test_map_percent": 2.81
}
```

## 2026-10-14T17:23:38+03:00 — baseline_complete

Завершён baseline global_popularity на полном validation/test

Запуск: `hm_global_popularity_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.0035739078014296673
  },
  "test_metrics": {
    "map": 0.0030455769442783946
  },
  "artifacts": "baseline/results/simple_metrics.json"
}
```

## 2026-10-14T17:23:38+03:00 — baseline_complete

Завершён baseline past_visit на полном validation/test

Запуск: `hm_past_visit_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.007816613709866022
  },
  "test_metrics": {
    "map": 0.007946612394759278
  },
  "artifacts": "baseline/results/simple_metrics.json"
}
```

## 2026-10-14T17:23:38+03:00 — discrepancy

Past-visit MAP отличается от опубликованного результата; причина не установлена, параметры и метрики не подгонялись.

## 2026-10-14T17:23:38+03:00 — planned_run

Запланирован полный прогон ID-GNN

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "pending",
  "seed": 42,
  "artifacts": "RelBenchGNN/results/seed_42"
}
```

## 2026-10-14T17:23:38+03:00 — planned_run

Запланирован полный прогон ID-GNN

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "pending",
  "seed": 43,
  "artifacts": "RelBenchGNN/results/seed_43"
}
```

## 2026-10-14T17:23:38+03:00 — planned_run

Запланирован полный прогон ID-GNN

Запуск: `hm_idgnn_last_seed_44_v1`.

```json
{
  "status": "pending",
  "seed": 44,
  "artifacts": "RelBenchGNN/results/seed_44"
}
```

## 2026-10-14T17:23:38+03:00 — planned_run

Запланирован полный прогон ID-GNN

Запуск: `hm_idgnn_last_seed_45_v1`.

```json
{
  "status": "pending",
  "seed": 45,
  "artifacts": "RelBenchGNN/results/seed_45"
}
```

## 2026-10-14T17:23:38+03:00 — planned_run

Запланирован полный прогон ID-GNN

Запуск: `hm_idgnn_last_seed_46_v1`.

```json
{
  "status": "pending",
  "seed": 46,
  "artifacts": "RelBenchGNN/results/seed_46"
}
```

## 2026-10-14T17:23:38+03:00 — smoke_complete

Короткая техническая проверка завершена; метрики не сравниваются со статьёй.

Запуск: `hm_idgnn_smoke_v1`.

```json
{
  "status": "smoke_complete",
  "smoke": true,
  "val_metrics": {
    "map": 0.0
  },
  "test_metrics": {
    "map": 0.03787878787878788
  },
  "artifacts": "RelBenchGNN/results/smoke"
}
```

## 2026-10-14T17:23:38+03:00 — stage

Фоновый конвейер запущен; текущий этап следует сверять с процессом и логами.

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "running",
  "artifacts": "RelBenchGNN/logs"
}
```

## 2026-10-14T17:25:45+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T17:25:45+03:00 — stage

Полный прогон ID-GNN активен; статус подтверждён процессом и логом.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42"
}
```

## 2026-10-14T17:28:22+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T17:28:22+03:00 — progress

Обучение seed 42: эпоха 1, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:28:52+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 1,
  "train_loss": 0.039372240579026274,
  "val_metrics": {
    "map": 0.02562482836509997
  },
  "elapsed_seconds": 462.47408270835876
}
```

## 2026-10-14T17:28:52+03:00 — progress

Обучение seed 42: эпоха 2, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:29:22+03:00 — progress

Обучение seed 42: эпоха 2, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:29:41+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T17:29:41+03:00 — progress

Обучение seed 42: эпоха 2, шаг 302/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 302,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:30:11+03:00 — progress

Обучение seed 42: эпоха 2, шаг 576/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 576,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:30:41+03:00 — progress

Обучение seed 42: эпоха 2, шаг 867/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 867,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:31:12+03:00 — progress

Обучение seed 42: эпоха 2, шаг 1195/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 1195,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:31:42+03:00 — progress

Обучение seed 42: эпоха 2, шаг 1528/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 1528,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:32:12+03:00 — progress

Обучение seed 42: эпоха 2, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:32:42+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 2,
  "train_loss": 0.038005107176781454,
  "val_metrics": {
    "map": 0.025481438635161245
  },
  "elapsed_seconds": 683.2374241352081
}
```

## 2026-10-14T17:32:42+03:00 — progress

Обучение seed 42: эпоха 3, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:33:12+03:00 — progress

Обучение seed 42: эпоха 3, шаг 313/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 313,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:33:42+03:00 — progress

Обучение seed 42: эпоха 3, шаг 624/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 624,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:34:12+03:00 — progress

Обучение seed 42: эпоха 3, шаг 953/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 953,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:34:42+03:00 — progress

Обучение seed 42: эпоха 3, шаг 1264/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 1264,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:35:12+03:00 — progress

Обучение seed 42: эпоха 3, шаг 1595/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 1595,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:35:42+03:00 — progress

Обучение seed 42: эпоха 3, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:36:12+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 3,
  "train_loss": 0.03780345185002036,
  "val_metrics": {
    "map": 0.025961588459098087
  },
  "elapsed_seconds": 895.4003534317017
}
```

## 2026-10-14T17:36:12+03:00 — progress

Обучение seed 42: эпоха 4, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:36:42+03:00 — progress

Обучение seed 42: эпоха 4, шаг 335/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 335,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:37:12+03:00 — progress

Обучение seed 42: эпоха 4, шаг 673/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 673,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:37:42+03:00 — progress

Обучение seed 42: эпоха 4, шаг 1008/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 1008,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:38:12+03:00 — progress

Обучение seed 42: эпоха 4, шаг 1343/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 1343,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:38:42+03:00 — progress

Обучение seed 42: эпоха 4, шаг 1675/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 1675,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:39:12+03:00 — progress

Обучение seed 42: эпоха 4, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:39:43+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 4,
  "train_loss": 0.03784377485009068,
  "val_metrics": {
    "map": 0.025954311586871125
  },
  "elapsed_seconds": 1101.1662678718567
}
```

## 2026-10-14T17:39:43+03:00 — progress

Обучение seed 42: эпоха 5, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:40:13+03:00 — progress

Обучение seed 42: эпоха 5, шаг 320/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 320,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:40:43+03:00 — progress

Обучение seed 42: эпоха 5, шаг 653/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 653,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:41:13+03:00 — progress

Обучение seed 42: эпоха 5, шаг 984/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 984,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:41:43+03:00 — progress

Обучение seed 42: эпоха 5, шаг 1315/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 1315,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:42:13+03:00 — progress

Обучение seed 42: эпоха 5, шаг 1635/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 1635,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:42:43+03:00 — progress

Обучение seed 42: эпоха 5, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:43:13+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 5,
  "train_loss": 0.03755851088701792,
  "val_metrics": {
    "map": 0.02600118901339541
  },
  "elapsed_seconds": 1311.484308719635
}
```

## 2026-10-14T17:43:13+03:00 — progress

Обучение seed 42: эпоха 6, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:43:43+03:00 — progress

Обучение seed 42: эпоха 6, шаг 331/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 331,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:44:13+03:00 — progress

Обучение seed 42: эпоха 6, шаг 662/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 662,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:44:43+03:00 — progress

Обучение seed 42: эпоха 6, шаг 963/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 963,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:45:13+03:00 — progress

Обучение seed 42: эпоха 6, шаг 1286/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 1286,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:45:43+03:00 — progress

Обучение seed 42: эпоха 6, шаг 1613/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 1613,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:46:14+03:00 — progress

Обучение seed 42: эпоха 6, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:46:44+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 6,
  "train_loss": 0.03778821706328578,
  "val_metrics": {
    "map": 0.026088450149124965
  },
  "elapsed_seconds": 1531.5692439079285
}
```

## 2026-10-14T17:46:44+03:00 — progress

Обучение seed 42: эпоха 7, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:47:14+03:00 — progress

Обучение seed 42: эпоха 7, шаг 186/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 186,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:47:44+03:00 — progress

Обучение seed 42: эпоха 7, шаг 500/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 500,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:48:14+03:00 — progress

Обучение seed 42: эпоха 7, шаг 810/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 810,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:48:44+03:00 — progress

Обучение seed 42: эпоха 7, шаг 1134/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 1134,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:49:14+03:00 — progress

Обучение seed 42: эпоха 7, шаг 1456/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 1456,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:49:44+03:00 — progress

Обучение seed 42: эпоха 7, шаг 1781/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 1781,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:50:15+03:00 — progress

Обучение seed 42: эпоха 7, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:50:45+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 7,
  "train_loss": 0.03778481171753794,
  "val_metrics": {
    "map": 0.02594742051566924
  },
  "elapsed_seconds": 1760.6959176063538
}
```

## 2026-10-14T17:50:45+03:00 — progress

Обучение seed 42: эпоха 8, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:51:15+03:00 — progress

Обучение seed 42: эпоха 8, шаг 329/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 329,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:51:45+03:00 — progress

Обучение seed 42: эпоха 8, шаг 662/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 662,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:52:13+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T17:52:15+03:00 — progress

Обучение seed 42: эпоха 8, шаг 950/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 950,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:52:45+03:00 — progress

Обучение seed 42: эпоха 8, шаг 1233/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 1233,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:53:15+03:00 — progress

Обучение seed 42: эпоха 8, шаг 1563/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 1563,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:53:45+03:00 — progress

Обучение seed 42: эпоха 8, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:54:15+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 8,
  "train_loss": 0.037612595190662436,
  "val_metrics": {
    "map": 0.026046786405867047
  },
  "elapsed_seconds": 1978.5040619373322
}
```

## 2026-10-14T17:54:15+03:00 — progress

Обучение seed 42: эпоха 9, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:54:39+03:00 — user_request

Пользователь поручил после обучения проверить инференс и сохранить наглядные таблицы/графики.

## 2026-10-14T17:54:39+03:00 — postprocess_planned

Настроено автоматическое продолжение после всех пяти прогонов: независимая загрузка best.pt, полный validation/test, проверка предсказаний и метрик, время инференса, таблицы и графики.

Запуск: `hm_postprocess_v1`.

```json
{
  "status": "pending",
  "artifacts": "RelBenchGNN/postprocess.py",
  "inference_executed": false,
  "inference_map_tolerance": 1e-06
}
```

## 2026-10-14T17:54:39+03:00 — dependency_pin

При установке matplotlib решатель временно выбрал NumPy 2.5.4; совместимые NumPy 1.26.4 и contourpy 1.3.0 восстановлены и зафиксированы. Текущий процесс обучения продолжил работу; установленные версии проверены.

```json
{
  "numpy": "1.26.4",
  "contourpy": "1.3.0",
  "matplotlib": "3.9.2"
}
```

## 2026-10-14T17:54:40+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T17:54:40+03:00 — progress

Обучение seed 42: эпоха 9, шаг 323/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 323,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:54:45+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T17:55:15+03:00 — progress

Обучение seed 42: эпоха 9, шаг 643/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 643,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:55:45+03:00 — progress

Обучение seed 42: эпоха 9, шаг 971/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 971,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:56:15+03:00 — progress

Обучение seed 42: эпоха 9, шаг 1294/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 1294,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:56:45+03:00 — progress

Обучение seed 42: эпоха 9, шаг 1623/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 1623,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:57:15+03:00 — progress

Обучение seed 42: эпоха 9, шаг 1913/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9,
  "train_step": 1913,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:57:45+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 9,
  "train_loss": 0.037653734502323635,
  "val_metrics": {
    "map": 0.026012076954434003
  },
  "elapsed_seconds": 2194.0815761089325
}
```

## 2026-10-14T17:57:45+03:00 — progress

Обучение seed 42: эпоха 10, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:57:50+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T17:58:21+03:00 — progress

Обучение seed 42: эпоха 10, шаг 327/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 327,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:58:51+03:00 — progress

Обучение seed 42: эпоха 10, шаг 647/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 647,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:59:21+03:00 — progress

Обучение seed 42: эпоха 10, шаг 957/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 957,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T17:59:51+03:00 — progress

Обучение seed 42: эпоха 10, шаг 1268/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 1268,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:00:21+03:00 — progress

Обучение seed 42: эпоха 10, шаг 1596/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 1596,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:00:51+03:00 — progress

Обучение seed 42: эпоха 10, шаг 1917/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10,
  "train_step": 1917,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:01:21+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 10,
  "train_loss": 0.03768445990566308,
  "val_metrics": {
    "map": 0.02599822650773936
  },
  "elapsed_seconds": 2408.6361660957336
}
```

## 2026-10-14T18:01:21+03:00 — progress

Обучение seed 42: эпоха 11, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:01:26+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:01:56+03:00 — progress

Обучение seed 42: эпоха 11, шаг 316/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 316,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:02:26+03:00 — progress

Обучение seed 42: эпоха 11, шаг 639/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 639,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:02:56+03:00 — progress

Обучение seed 42: эпоха 11, шаг 965/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 965,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:03:26+03:00 — progress

Обучение seed 42: эпоха 11, шаг 1285/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 1285,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:03:56+03:00 — progress

Обучение seed 42: эпоха 11, шаг 1597/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 1597,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:04:26+03:00 — progress

Обучение seed 42: эпоха 11, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:04:56+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 11,
  "train_loss": 0.037570915018944294,
  "val_metrics": {
    "map": 0.026052766059659015
  },
  "elapsed_seconds": 2621.618856906891
}
```

## 2026-10-14T18:04:56+03:00 — progress

Обучение seed 42: эпоха 12, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:05:01+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:05:31+03:00 — progress

Обучение seed 42: эпоха 12, шаг 320/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 320,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:06:01+03:00 — progress

Обучение seed 42: эпоха 12, шаг 629/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 629,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:06:31+03:00 — progress

Обучение seed 42: эпоха 12, шаг 950/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 950,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:07:01+03:00 — progress

Обучение seed 42: эпоха 12, шаг 1278/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 1278,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:07:31+03:00 — progress

Обучение seed 42: эпоха 12, шаг 1605/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 1605,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:08:02+03:00 — progress

Обучение seed 42: эпоха 12, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:08:32+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 12,
  "train_loss": 0.037545186372826854,
  "val_metrics": {
    "map": 0.026248229544562154
  },
  "elapsed_seconds": 2835.338489294052
}
```

## 2026-10-14T18:08:32+03:00 — progress

Обучение seed 42: эпоха 13, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:08:37+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:09:07+03:00 — progress

Обучение seed 42: эпоха 13, шаг 320/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 320,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:09:37+03:00 — progress

Обучение seed 42: эпоха 13, шаг 635/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 635,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:10:07+03:00 — progress

Обучение seed 42: эпоха 13, шаг 956/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 956,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:10:37+03:00 — progress

Обучение seed 42: эпоха 13, шаг 1282/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 1282,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:11:07+03:00 — progress

Обучение seed 42: эпоха 13, шаг 1610/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 1610,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:11:37+03:00 — progress

Обучение seed 42: эпоха 13, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:12:07+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 13,
  "train_loss": 0.03723888006672669,
  "val_metrics": {
    "map": 0.026233859436304387
  },
  "elapsed_seconds": 3048.1128895282745
}
```

## 2026-10-14T18:12:07+03:00 — progress

Обучение seed 42: эпоха 14, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:12:12+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:12:42+03:00 — progress

Обучение seed 42: эпоха 14, шаг 324/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 324,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:13:12+03:00 — progress

Обучение seed 42: эпоха 14, шаг 650/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 650,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:13:42+03:00 — progress

Обучение seed 42: эпоха 14, шаг 980/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 980,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:14:12+03:00 — progress

Обучение seed 42: эпоха 14, шаг 1309/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 1309,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:14:42+03:00 — progress

Обучение seed 42: эпоха 14, шаг 1634/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 1634,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:15:12+03:00 — progress

Обучение seed 42: эпоха 14, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:15:43+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 14,
  "train_loss": 0.03748767162777333,
  "val_metrics": {
    "map": 0.02611974468564859
  },
  "elapsed_seconds": 3260.3378026485443
}
```

## 2026-10-14T18:15:43+03:00 — progress

Обучение seed 42: эпоха 15, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:15:47+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:16:17+03:00 — progress

Обучение seed 42: эпоха 15, шаг 309/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 309,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:16:48+03:00 — progress

Обучение seed 42: эпоха 15, шаг 635/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 635,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:17:18+03:00 — progress

Обучение seed 42: эпоха 15, шаг 946/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 946,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:17:48+03:00 — progress

Обучение seed 42: эпоха 15, шаг 1260/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 1260,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:18:18+03:00 — progress

Обучение seed 42: эпоха 15, шаг 1587/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 1587,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:18:48+03:00 — progress

Обучение seed 42: эпоха 15, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:19:18+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 15,
  "train_loss": 0.03744724830122143,
  "val_metrics": {
    "map": 0.02610744510102361
  },
  "elapsed_seconds": 3475.6355917453766
}
```

## 2026-10-14T18:19:18+03:00 — progress

Обучение seed 42: эпоха 16, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:19:23+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:19:53+03:00 — progress

Обучение seed 42: эпоха 16, шаг 322/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 322,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:20:23+03:00 — progress

Обучение seed 42: эпоха 16, шаг 653/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 653,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:20:54+03:00 — progress

Обучение seed 42: эпоха 16, шаг 979/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 979,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:21:24+03:00 — progress

Обучение seed 42: эпоха 16, шаг 1309/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 1309,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:21:54+03:00 — progress

Обучение seed 42: эпоха 16, шаг 1627/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 1627,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:22:24+03:00 — progress

Обучение seed 42: эпоха 16, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:22:54+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 16,
  "train_loss": 0.03720211348090222,
  "val_metrics": {
    "map": 0.02609744260427084
  },
  "elapsed_seconds": 3691.5762147903442
}
```

## 2026-10-14T18:22:54+03:00 — progress

Обучение seed 42: эпоха 17, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:22:59+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:23:29+03:00 — progress

Обучение seed 42: эпоха 17, шаг 320/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 320,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:23:59+03:00 — progress

Обучение seed 42: эпоха 17, шаг 648/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 648,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:24:00+03:00 — user_request

Нужно сравнение ID-GNN с локальной моделью дерева на ручных признаках, а также отдельные значения из статьи и фактические локальные результаты.

## 2026-10-14T18:24:00+03:00 — manual_adaptation

Создано 126 ручных признаков: адаптированное подмножество экспертных user-churn/item-sales SQL плюс признаки пары. Это наша адаптация, не опубликованный экспертный ранжирующий набор.

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "pending",
  "feature_count": 126,
  "artifacts": "baseline/MANUAL_BASELINE.md",
  "train_user_times": 50000,
  "tuning_validation_users": 10000,
  "evaluation": "full validation/test, exact respective GNN candidate pool",
  "published_lightgbm_raw_map_percent": {
    "val": 0.44,
    "test": 0.38
  },
  "published_idgnn_map_percent": {
    "val": 2.64,
    "test": 2.81
  }
}
```

## 2026-10-14T18:24:00+03:00 — feature_tests

Тесты ручных признаков пройдены: cutoff, исключение будущих транзакций, отсутствие ID/метки во входах, одна строка на пару.

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован decision_tree на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_decision_tree_manual_seed_42_v1`.

```json
{
  "status": "pending",
  "seed": 42,
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_42"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован decision_tree на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_decision_tree_manual_seed_43_v1`.

```json
{
  "status": "pending",
  "seed": 43,
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_43"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован decision_tree на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_decision_tree_manual_seed_44_v1`.

```json
{
  "status": "pending",
  "seed": 44,
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_44"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован decision_tree на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_decision_tree_manual_seed_45_v1`.

```json
{
  "status": "pending",
  "seed": 45,
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_45"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован decision_tree на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_decision_tree_manual_seed_46_v1`.

```json
{
  "status": "pending",
  "seed": 46,
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_46"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован lightgbm на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "pending",
  "seed": 42,
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_42"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован lightgbm на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_lightgbm_manual_seed_43_v1`.

```json
{
  "status": "pending",
  "seed": 43,
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_43"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован lightgbm на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_lightgbm_manual_seed_44_v1`.

```json
{
  "status": "pending",
  "seed": 44,
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_44"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован lightgbm на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_lightgbm_manual_seed_45_v1`.

```json
{
  "status": "pending",
  "seed": 45,
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_45"
}
```

## 2026-10-14T18:24:00+03:00 — planned_run

Запланирован lightgbm на ручных признаках после освобождения ресурсов GNN

Запуск: `hm_lightgbm_manual_seed_46_v1`.

```json
{
  "status": "pending",
  "seed": 46,
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_46"
}
```

## 2026-10-14T18:24:01+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T18:24:06+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:24:36+03:00 — progress

Обучение seed 42: эпоха 17, шаг 949/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 949,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:25:07+03:00 — progress

Обучение seed 42: эпоха 17, шаг 1279/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 1279,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:25:37+03:00 — progress

Обучение seed 42: эпоха 17, шаг 1605/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 1605,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:26:07+03:00 — progress

Обучение seed 42: эпоха 17, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:26:37+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 17,
  "train_loss": 0.03734446814736183,
  "val_metrics": {
    "map": 0.026131362114521377
  },
  "elapsed_seconds": 3904.204199552536
}
```

## 2026-10-14T18:26:37+03:00 — progress

Обучение seed 42: эпоха 18, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:26:42+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:27:12+03:00 — progress

Обучение seed 42: эпоха 18, шаг 325/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 325,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:27:30+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T18:27:30+03:00 — progress

Обучение seed 42: эпоха 18, шаг 649/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 649,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:27:35+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:28:05+03:00 — progress

Обучение seed 42: эпоха 18, шаг 952/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 952,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:28:35+03:00 — progress

Обучение seed 42: эпоха 18, шаг 1284/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 1284,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:29:06+03:00 — progress

Обучение seed 42: эпоха 18, шаг 1609/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 1609,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:29:36+03:00 — progress

Обучение seed 42: эпоха 18, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:30:06+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 18,
  "train_loss": 0.03737975380188051,
  "val_metrics": {
    "map": 0.02623191643200536
  },
  "elapsed_seconds": 4118.834531784058
}
```

## 2026-10-14T18:30:06+03:00 — progress

Обучение seed 42: эпоха 19, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:30:11+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:30:41+03:00 — progress

Обучение seed 42: эпоха 19, шаг 329/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 329,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:31:11+03:00 — progress

Обучение seed 42: эпоха 19, шаг 655/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 655,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:31:25+03:00 — manual_model_checks

На маленьком примере проверены обучение, сохранение/повторная загрузка DecisionTree и LightGBM, потоковый top-k и исключение будущих данных. Это техническая проверка, не метрика полного H&M.

```json
{
  "checks_passed": true,
  "feature_count": 126
}
```

## 2026-10-14T18:31:25+03:00 — real_sql_check

126 ручных признаков проверены на настоящем H&M с ограниченной RAM; проверка прошла.

```json
{
  "result": {
    "passed": true,
    "feature_count": 126,
    "pair_rows": 2,
    "cutoff": "2020-09-07",
    "max_used_transaction_date": "2020-09-05 00:00:00",
    "scope": "real-data SQL and memory check; not a trained baseline metric"
  }
}
```

## 2026-10-14T18:31:31+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:31:41+03:00 — progress

Обучение seed 42: эпоха 19, шаг 982/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 982,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:32:11+03:00 — progress

Обучение seed 42: эпоха 19, шаг 1295/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 1295,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:32:41+03:00 — progress

Обучение seed 42: эпоха 19, шаг 1597/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 1597,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:33:11+03:00 — progress

Обучение seed 42: эпоха 19, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:33:41+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 19,
  "train_loss": 0.03742446585596963,
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "elapsed_seconds": 4336.426944494247
}
```

## 2026-10-14T18:33:41+03:00 — progress

Обучение seed 42: эпоха 20, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:33:46+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:34:16+03:00 — progress

Обучение seed 42: эпоха 20, шаг 319/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 319,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:34:47+03:00 — progress

Обучение seed 42: эпоха 20, шаг 628/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 628,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:35:17+03:00 — progress

Обучение seed 42: эпоха 20, шаг 951/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 951,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:35:47+03:00 — progress

Обучение seed 42: эпоха 20, шаг 1264/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 1264,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:36:17+03:00 — progress

Обучение seed 42: эпоха 20, шаг 1555/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 1555,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:36:47+03:00 — progress

Обучение seed 42: эпоха 20, шаг 2000/2000.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20,
  "train_step": 2000,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:37:17+03:00 — epoch

Завершена эпоха ID-GNN; данные прочитаны из history.json.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_42",
  "epoch": 20,
  "train_loss": 0.037264465778146405,
  "val_metrics": {
    "map": 0.026262996975727263
  },
  "elapsed_seconds": 4557.071720600128
}
```

## 2026-10-14T18:37:23+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 0,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:38:23+03:00 — run_complete

Полный прогон ID-GNN завершён; метрики прочитаны из итогового файла.

Запуск: `hm_idgnn_last_seed_42_v1`.

```json
{
  "status": "complete",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "test_metrics": {
    "map": 0.027843150477067403
  },
  "epoch": 20,
  "artifacts": "RelBenchGNN/results/seed_42"
}
```

## 2026-10-14T18:38:28+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:39:01+03:00 — run_start

Начат запуск RelBench ID-GNN

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 43,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_43",
    "run_id": null,
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true
  },
  "artifacts": "RelBenchGNN/results/seed_43"
}
```

## 2026-10-14T18:39:36+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T18:40:34+03:00 — training_start

Начато обучение на GPU

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "epoch": 0
}
```

## 2026-10-14T18:40:58+03:00 — progress

Обучение seed 43: эпоха 1, шаг 0/2000.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 0,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:41:28+03:00 — progress

Обучение seed 43: эпоха 1, шаг 3/2000.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 3,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:41:58+03:00 — progress

Обучение seed 43: эпоха 1, шаг 64/2000.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 64,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:42:29+03:00 — progress

Обучение seed 43: эпоха 1, шаг 179/2000.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 179,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:43:00+03:00 — progress

Обучение seed 43: эпоха 1, шаг 308/2000.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "training",
  "current_epoch": 1,
  "train_step": 308,
  "elapsed_note": "Эпоха считается завершённой только после записи validation метрики."
}
```

## 2026-10-14T18:45:02+03:00 — protocol_change

Пользователь сократил эксперимент до одного seed 42 для ускорения. Готовый ID-GNN сохранён; далее независимый инференс и два ручных baseline только seed 42. Статья: среднее пяти запусков; локальный разброс не оценивается.

```json
{
  "selected_seeds": [
    42
  ],
  "previous_seeds": [
    42,
    43,
    44,
    45,
    46
  ],
  "artifacts": "RelBenchGNN/experiment_plan.json"
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_idgnn_last_seed_43_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_decision_tree_manual_seed_43_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_lightgbm_manual_seed_43_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_idgnn_last_seed_44_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_decision_tree_manual_seed_44_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_lightgbm_manual_seed_44_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_idgnn_last_seed_45_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_decision_tree_manual_seed_45_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:02+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_lightgbm_manual_seed_45_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:03+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_idgnn_last_seed_46_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:03+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_decision_tree_manual_seed_46_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:03+03:00 — run_cancelled

Дополнительный seed отменён пользователем; существующие артефакты сохранены и исключены из итогового сравнения.

Запуск: `hm_lightgbm_manual_seed_46_v1`.

```json
{
  "status": "cancelled",
  "included_in_comparison": false
}
```

## 2026-10-14T18:45:03+03:00 — summary

Обновлена сводка завершённых прогонов ID-GNN

Запуск: `hm_idgnn_last_summary_v1`.

```json
{
  "status": "complete",
  "completed_runs": 1,
  "expected_runs": 1,
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "test_metrics": {
    "map": 0.027843150477067403
  },
  "artifacts": "RelBenchGNN/results/summary.json"
}
```

## 2026-10-14T18:45:07+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:45:19+03:00 — stage

Продолжение по выбранным seeds: готовое обучение повторно не запускается

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "postprocessing"
}
```

## 2026-10-14T18:45:19+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T18:45:19+03:00 — summary

Обновлена сводка завершённых прогонов ID-GNN

Запуск: `hm_idgnn_last_summary_v1`.

```json
{
  "status": "complete",
  "completed_runs": 1,
  "expected_runs": 1,
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "test_metrics": {
    "map": 0.027843150477067403
  },
  "artifacts": "RelBenchGNN/results/summary.json"
}
```

## 2026-10-14T18:45:19+03:00 — postprocess

После обучения выполняются независимый инференс и визуальный отчёт

Запуск: `hm_postprocess_v1`.

```json
{
  "status": "inference"
}
```

## 2026-10-14T18:45:24+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:45:56+03:00 — run_start

Начата независимая проверка инференса из best.pt

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42/inference",
    "run_id": "hm_idgnn_last_seed_42_inference_v1",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": false
  },
  "artifacts": "RelBenchGNN/results/seed_42/inference"
}
```

## 2026-10-14T18:46:25+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T18:47:01+03:00 — inference_start

Веса загружены строго; запущен инференс полного validation/test

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "inference"
}
```

## 2026-10-14T18:47:14+03:00 — error

Запуск ID-GNN завершился ошибкой

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "failed",
  "error_type": "NameError",
  "error": "name 'pd' is not defined"
}
```

## 2026-10-14T18:47:27+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:47:27+03:00 — postprocess_complete

Отчёт сохранён; есть ошибки инференса или ручного baseline

Запуск: `hm_postprocess_v1`.

```json
{
  "status": "failed",
  "failed_seeds": [
    42
  ],
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T18:47:28+03:00 — pipeline_exit

Конвейер завершён с кодом 1

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "failed"
}
```

## 2026-10-14T18:47:55+03:00 — pipeline_exit

Конвейер завершился с кодом 1; статус подтверждён файлом завершения.

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "failed",
  "exit_code": "1"
}
```

## 2026-10-14T19:32:53+03:00 — bug_fix

После перехода на один seed обнаружены и исправлены две ошибки: график ошибочно требовал более одного результата для среднего MAP; генератор инференса добавлял pandas до добавления блока hashlib и импорт не попадал в итоговый код. Готовый seed 42 и его метрики сохранены; инференс возобновляется, деревья пока не обучены.

```json
{
  "artifacts": "RelBenchGNN/build_report.py; RelBenchGNN/prepare_inference.py"
}
```

## 2026-10-14T19:32:56+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:33:00+03:00 — stage

Продолжение по выбранным seeds: готовое обучение повторно не запускается

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "postprocessing"
}
```

## 2026-10-14T19:33:00+03:00 — monitor_start

Запущено автоматическое обновление истории по процессам и артефактам каждые 30 секунд.

## 2026-10-14T19:33:00+03:00 — summary

Обновлена сводка завершённых прогонов ID-GNN

Запуск: `hm_idgnn_last_summary_v1`.

```json
{
  "status": "complete",
  "completed_runs": 1,
  "expected_runs": 1,
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "test_metrics": {
    "map": 0.027843150477067403
  },
  "artifacts": "RelBenchGNN/results/summary.json"
}
```

## 2026-10-14T19:33:00+03:00 — postprocess

После обучения выполняются независимый инференс и визуальный отчёт

Запуск: `hm_postprocess_v1`.

```json
{
  "status": "inference"
}
```

## 2026-10-14T19:33:03+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 0,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:33:34+03:00 — run_start

Начата независимая проверка инференса из best.pt

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/seed_42/inference",
    "run_id": "hm_idgnn_last_seed_42_inference_v1",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": false
  },
  "artifacts": "RelBenchGNN/results/seed_42/inference"
}
```

## 2026-10-14T19:34:05+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T19:34:36+03:00 — inference_start

Веса загружены строго; запущен инференс полного validation/test

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "inference"
}
```

## 2026-10-14T19:36:13+03:00 — inference_complete

Проверка инференса пройдена

Запуск: `hm_idgnn_last_seed_42_inference_v1`.

```json
{
  "status": "verified",
  "val_metrics": {
    "map": 0.02634419239310869
  },
  "test_metrics": {
    "map": 0.027843150477067403
  },
  "checks": {
    "val": {
      "shape": [
        74575,
        12
      ],
      "shape_ok": true,
      "ids_valid": true,
      "unique_ids_per_user": true,
      "predictions_identical": true,
      "same_item_at_same_rank_fraction": 1.0,
      "map_absolute_difference": 0.0,
      "map_tolerance": 1e-06,
      "passed": true
    },
    "test": {
      "shape": [
        67144,
        12
      ],
      "shape_ok": true,
      "ids_valid": true,
      "unique_ids_per_user": true,
      "predictions_identical": true,
      "same_item_at_same_rank_fraction": 1.0,
      "map_absolute_difference": 0.0,
      "map_tolerance": 1e-06,
      "passed": true
    }
  },
  "artifacts": "RelBenchGNN/results/seed_42/inference"
}
```

## 2026-10-14T19:36:18+03:00 — manual_baseline_queue

После проверки ID-GNN запускаются дерево и LightGBM на ручных признаках

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:36+03:00 — manual_baseline_start

Начато построение и обучение дерева и LightGBM на ручных признаках

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features",
  "config": {
    "train_user_times": 50000,
    "tune_users": 10000
  }
}
```

## 2026-10-14T19:36:38+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 1,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:36:40+03:00 — feature_snapshot

Ручные признаки train: дата 2019-09-09, 1/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:41+03:00 — feature_snapshot

Ручные признаки train: дата 2019-09-16, 2/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:42+03:00 — feature_snapshot

Ручные признаки train: дата 2019-09-23, 3/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:43+03:00 — feature_snapshot

Ручные признаки train: дата 2019-09-30, 4/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:44+03:00 — feature_snapshot

Ручные признаки train: дата 2019-10-07, 5/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:45+03:00 — feature_snapshot

Ручные признаки train: дата 2019-10-14, 6/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:46+03:00 — feature_snapshot

Ручные признаки train: дата 2019-10-21, 7/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:47+03:00 — feature_snapshot

Ручные признаки train: дата 2019-10-28, 8/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:48+03:00 — feature_snapshot

Ручные признаки train: дата 2019-11-04, 9/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:49+03:00 — feature_snapshot

Ручные признаки train: дата 2019-11-11, 10/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:50+03:00 — feature_snapshot

Ручные признаки train: дата 2019-11-18, 11/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:51+03:00 — feature_snapshot

Ручные признаки train: дата 2019-11-25, 12/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:52+03:00 — feature_snapshot

Ручные признаки train: дата 2019-12-02, 13/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:54+03:00 — feature_snapshot

Ручные признаки train: дата 2019-12-09, 14/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:55+03:00 — feature_snapshot

Ручные признаки train: дата 2019-12-16, 15/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:56+03:00 — feature_snapshot

Ручные признаки train: дата 2019-12-23, 16/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:57+03:00 — feature_snapshot

Ручные признаки train: дата 2019-12-30, 17/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:36:58+03:00 — feature_snapshot

Ручные признаки train: дата 2020-01-06, 18/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:00+03:00 — feature_snapshot

Ручные признаки train: дата 2020-01-13, 19/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:01+03:00 — feature_snapshot

Ручные признаки train: дата 2020-01-20, 20/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:02+03:00 — feature_snapshot

Ручные признаки train: дата 2020-01-27, 21/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:04+03:00 — feature_snapshot

Ручные признаки train: дата 2020-02-03, 22/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:05+03:00 — feature_snapshot

Ручные признаки train: дата 2020-02-10, 23/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:06+03:00 — feature_snapshot

Ручные признаки train: дата 2020-02-17, 24/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:08+03:00 — feature_snapshot

Ручные признаки train: дата 2020-02-24, 25/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:09+03:00 — feature_snapshot

Ручные признаки train: дата 2020-03-02, 26/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:11+03:00 — feature_snapshot

Ручные признаки train: дата 2020-03-09, 27/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:12+03:00 — feature_snapshot

Ручные признаки train: дата 2020-03-16, 28/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:14+03:00 — feature_snapshot

Ручные признаки train: дата 2020-03-23, 29/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:15+03:00 — feature_snapshot

Ручные признаки train: дата 2020-03-30, 30/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:17+03:00 — feature_snapshot

Ручные признаки train: дата 2020-04-06, 31/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:18+03:00 — feature_snapshot

Ручные признаки train: дата 2020-04-13, 32/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:20+03:00 — feature_snapshot

Ручные признаки train: дата 2020-04-20, 33/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:22+03:00 — feature_snapshot

Ручные признаки train: дата 2020-04-27, 34/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:23+03:00 — feature_snapshot

Ручные признаки train: дата 2020-05-04, 35/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:25+03:00 — feature_snapshot

Ручные признаки train: дата 2020-05-11, 36/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:27+03:00 — feature_snapshot

Ручные признаки train: дата 2020-05-18, 37/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:29+03:00 — feature_snapshot

Ручные признаки train: дата 2020-05-25, 38/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:30+03:00 — feature_snapshot

Ручные признаки train: дата 2020-06-01, 39/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:32+03:00 — feature_snapshot

Ручные признаки train: дата 2020-06-08, 40/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:34+03:00 — feature_snapshot

Ручные признаки train: дата 2020-06-15, 41/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:36+03:00 — feature_snapshot

Ручные признаки train: дата 2020-06-22, 42/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:39+03:00 — feature_snapshot

Ручные признаки train: дата 2020-06-29, 43/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:41+03:00 — feature_snapshot

Ручные признаки train: дата 2020-07-06, 44/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:43+03:00 — feature_snapshot

Ручные признаки train: дата 2020-07-13, 45/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:45+03:00 — feature_snapshot

Ручные признаки train: дата 2020-07-20, 46/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:47+03:00 — feature_snapshot

Ручные признаки train: дата 2020-07-27, 47/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:49+03:00 — feature_snapshot

Ручные признаки train: дата 2020-08-03, 48/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:51+03:00 — feature_snapshot

Ручные признаки train: дата 2020-08-10, 49/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:54+03:00 — feature_snapshot

Ручные признаки train: дата 2020-08-17, 50/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:56+03:00 — feature_snapshot

Ручные признаки train: дата 2020-08-24, 51/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:37:58+03:00 — feature_snapshot

Ручные признаки train: дата 2020-08-31, 52/52

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features"
}
```

## 2026-10-14T19:38:24+03:00 — feature_snapshot

Ручные признаки полного val сохранены

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features",
  "candidate_stats": {
    "mean_candidate_count_union": 28.00647670130741,
    "users_with_relevant_candidate_fraction_union": 0.0892122024807241,
    "candidate_recall_union": 0.04479577709974014,
    "oracle_map_upper_bound_union": 0.044987704737620926
  }
}
```

## 2026-10-14T19:38:46+03:00 — feature_snapshot

Ручные признаки полного test сохранены

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "features",
  "candidate_stats": {
    "mean_candidate_count_union": 28.184275586798524
  }
}
```

## 2026-10-14T19:43:45+03:00 — verification

Проверена работа конвейера: независимый инференс seed 42 прошёл, validation/test предсказания полностью совпали с сохранёнными. Кэш 126 ручных признаков train/val/test готов. Процесс baseline/run_manual_tree.py активен на CPU; итоговые метрики деревьев пока отсутствуют. Новых ошибок в логах нет.

## 2026-10-14T19:44:56+03:00 — manual_baseline_tuned

Параметры выбраны только по validation; тест не использован для подбора

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "training",
  "config": {
    "adapted_expert_features": true,
    "feature_count": 126,
    "train_user_times": 50000,
    "train_pairs": 803377,
    "tuning_validation_users": 10000,
    "decision_tree_depth": 8,
    "decision_tree_min_leaf": 100,
    "lightgbm_num_leaves": 31,
    "lightgbm_rounds": 150,
    "lightgbm_parameters": {
      "objective": "binary",
      "verbosity": -1,
      "num_threads": 2,
      "learning_rate": 0.05,
      "min_data_in_leaf": 100,
      "max_bin": 127,
      "feature_fraction": 0.9,
      "bagging_fraction": 0.8,
      "bagging_freq": 1,
      "deterministic": true,
      "force_col_wise": true,
      "seed": 42
    },
    "trials": [
      {
        "model": "DecisionTree",
        "max_depth": 8,
        "validation_tuning_map": 0.019550728080120934
      },
      {
        "model": "DecisionTree",
        "max_depth": 12,
        "validation_tuning_map": 0.019231839400888913
      },
      {
        "model": "DecisionTree",
        "max_depth": 16,
        "validation_tuning_map": 0.018045682761832924
      },
      {
        "model": "LightGBM",
        "num_leaves": 15,
        "validation_tuning_map": 0.0213171714926788
      },
      {
        "model": "LightGBM",
        "num_leaves": 31,
        "validation_tuning_map": 0.021343242168255425
      }
    ],
    "shared_candidates": "each tree seed is evaluated on the exact respective ID-GNN inference pool; cached features use their union",
    "candidate_stats": {
      "val": {
        "mean_candidate_count_union": 28.00647670130741,
        "users_with_relevant_candidate_fraction_union": 0.0892122024807241,
        "candidate_recall_union": 0.04479577709974014,
        "oracle_map_upper_bound_union": 0.044987704737620926
      },
      "test": {
        "mean_candidate_count_union": 28.184275586798524
      }
    },
    "ties": "descending predicted score, ascending article_id; no target-dependent tie breaking"
  }
}
```

## 2026-10-14T19:44:56+03:00 — manual_model_start

Обучение decision_tree на ручных признаках, seed 42

Запуск: `hm_decision_tree_manual_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "adapted_expert_features": true,
    "feature_count": 126,
    "train_user_times": 50000,
    "train_pairs": 803377,
    "tuning_validation_users": 10000,
    "decision_tree_depth": 8,
    "decision_tree_min_leaf": 100,
    "lightgbm_num_leaves": 31,
    "lightgbm_rounds": 150,
    "lightgbm_parameters": {
      "objective": "binary",
      "verbosity": -1,
      "num_threads": 2,
      "learning_rate": 0.05,
      "min_data_in_leaf": 100,
      "max_bin": 127,
      "feature_fraction": 0.9,
      "bagging_fraction": 0.8,
      "bagging_freq": 1,
      "deterministic": true,
      "force_col_wise": true,
      "seed": 42
    },
    "trials": [
      {
        "model": "DecisionTree",
        "max_depth": 8,
        "validation_tuning_map": 0.019550728080120934
      },
      {
        "model": "DecisionTree",
        "max_depth": 12,
        "validation_tuning_map": 0.019231839400888913
      },
      {
        "model": "DecisionTree",
        "max_depth": 16,
        "validation_tuning_map": 0.018045682761832924
      },
      {
        "model": "LightGBM",
        "num_leaves": 15,
        "validation_tuning_map": 0.0213171714926788
      },
      {
        "model": "LightGBM",
        "num_leaves": 31,
        "validation_tuning_map": 0.021343242168255425
      }
    ],
    "shared_candidates": "each tree seed is evaluated on the exact respective ID-GNN inference pool; cached features use their union",
    "candidate_stats": {
      "val": {
        "mean_candidate_count_union": 28.00647670130741,
        "users_with_relevant_candidate_fraction_union": 0.0892122024807241,
        "candidate_recall_union": 0.04479577709974014,
        "oracle_map_upper_bound_union": 0.044987704737620926
      },
      "test": {
        "mean_candidate_count_union": 28.184275586798524
      }
    },
    "ties": "descending predicted score, ascending article_id; no target-dependent tie breaking"
  }
}
```

## 2026-10-14T19:46:10+03:00 — manual_model_complete

Завершён decision_tree; полный validation/test оценён из сохранённой модели

Запуск: `hm_decision_tree_manual_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.01876612409515324
  },
  "test_metrics": {
    "map": 0.020407610836605028
  },
  "artifacts": "baseline/results/manual_v1/decision_tree/seed_42"
}
```

## 2026-10-14T19:46:10+03:00 — manual_model_start

Обучение lightgbm на ручных признаках, seed 42

Запуск: `hm_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "training",
  "config": {
    "adapted_expert_features": true,
    "feature_count": 126,
    "train_user_times": 50000,
    "train_pairs": 803377,
    "tuning_validation_users": 10000,
    "decision_tree_depth": 8,
    "decision_tree_min_leaf": 100,
    "lightgbm_num_leaves": 31,
    "lightgbm_rounds": 150,
    "lightgbm_parameters": {
      "objective": "binary",
      "verbosity": -1,
      "num_threads": 2,
      "learning_rate": 0.05,
      "min_data_in_leaf": 100,
      "max_bin": 127,
      "feature_fraction": 0.9,
      "bagging_fraction": 0.8,
      "bagging_freq": 1,
      "deterministic": true,
      "force_col_wise": true,
      "seed": 42
    },
    "trials": [
      {
        "model": "DecisionTree",
        "max_depth": 8,
        "validation_tuning_map": 0.019550728080120934
      },
      {
        "model": "DecisionTree",
        "max_depth": 12,
        "validation_tuning_map": 0.019231839400888913
      },
      {
        "model": "DecisionTree",
        "max_depth": 16,
        "validation_tuning_map": 0.018045682761832924
      },
      {
        "model": "LightGBM",
        "num_leaves": 15,
        "validation_tuning_map": 0.0213171714926788
      },
      {
        "model": "LightGBM",
        "num_leaves": 31,
        "validation_tuning_map": 0.021343242168255425
      }
    ],
    "shared_candidates": "each tree seed is evaluated on the exact respective ID-GNN inference pool; cached features use their union",
    "candidate_stats": {
      "val": {
        "mean_candidate_count_union": 28.00647670130741,
        "users_with_relevant_candidate_fraction_union": 0.0892122024807241,
        "candidate_recall_union": 0.04479577709974014,
        "oracle_map_upper_bound_union": 0.044987704737620926
      },
      "test": {
        "mean_candidate_count_union": 28.184275586798524
      }
    },
    "ties": "descending predicted score, ascending article_id; no target-dependent tie breaking"
  }
}
```

## 2026-10-14T19:46:44+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "partial",
  "completed_runs": 1,
  "verified_inference_runs": 1,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:46:54+03:00 — manual_model_complete

Завершён lightgbm; полный validation/test оценён из сохранённой модели

Запуск: `hm_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.02093176718024488
  },
  "test_metrics": {
    "map": 0.022660772508761556
  },
  "artifacts": "baseline/results/manual_v1/lightgbm/seed_42"
}
```

## 2026-10-14T19:46:54+03:00 — manual_baseline_complete

Дерево и LightGBM с ручными признаками завершены по выбранным seeds

Запуск: `hm_manual_tree_pipeline_v1`.

```json
{
  "status": "complete",
  "artifacts": "baseline/results/manual_v1"
}
```

## 2026-10-14T19:46:58+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "complete",
  "completed_runs": 1,
  "verified_inference_runs": 1,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:46:58+03:00 — postprocess_complete

Инференс и ручные baseline проверены, таблицы и графики сохранены

Запуск: `hm_postprocess_v1`.

```json
{
  "status": "complete",
  "failed_seeds": [],
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:46:59+03:00 — pipeline_exit

Конвейер завершён с кодом 0

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "complete"
}
```

## 2026-10-14T19:47:18+03:00 — report_updated

Обновлены таблицы и графики результатов

Запуск: `hm_visual_report_v1`.

```json
{
  "status": "complete",
  "completed_runs": 1,
  "verified_inference_runs": 1,
  "artifacts": "reports/relbench_hm_v1/report.md"
}
```

## 2026-10-14T19:47:18+03:00 — pipeline_exit

Конвейер завершился с кодом 0; статус подтверждён файлом завершения.

Запуск: `hm_reproduction_pipeline_v1`.

```json
{
  "status": "complete",
  "exit_code": "0"
}
```

## 2026-10-14T20:09:05+03:00 — final_verification

Проверено завершение эксперимента seed 42: конвейер exit_code=0, активных процессов нет; независимый инференс GNN passed=true, модели деревьев сохранены и оценены после загрузки. Итоговый comparison.png визуально проверен: все пять методов отображены. Test MAP@12 (%): ID-GNN 2.78432, DecisionTree manual 2.04076, LightGBM manual 2.26608. CONTEXT.md обновлён.

## 2026-10-14T20:20:31+03:00 — embedding_protocol

Новый эксперимент: замороженный best.pt ID-GNN seed 42 → 128 представлений плюс availability → LightGBM. Обучающие пары и evaluation pools совпадают с ручным baseline; адаптация Appendix C.2 для H&M ranking, не результат авторов. In-sample GNN train embeddings; параметры дерева выбираются только на validation.

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "extracting"
}
```

## 2026-10-14T20:21:02+03:00 — run_start

Начата независимая проверка инференса из best.pt

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/baseline/results/gnn_embeddings_v1/extraction",
    "run_id": "hm_idgnn_embeddings_seed_42_v1",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": false
  },
  "artifacts": "baseline/results/gnn_embeddings_v1/extraction"
}
```

## 2026-10-14T20:21:37+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T20:23:50+03:00 — embedding_pipeline_exit

Эксперимент GNN → LightGBM завершил работу с кодом 137

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "failed"
}
```

## 2026-10-14T20:23:50+03:00 — embedding_fix

Исправлена подготовка выбранных train строк: исходные pandas индексы не соответствовали размеру sparse COO в get_link_train_table_input. Для экспорта метки не нужны: удалена целевая колонка из входа loader, индекс сброшен. Метки читаются отдельно из прежних обучающих пар, в граф не попадают. Исходные модели не изменены.

## 2026-10-14T20:23:52+03:00 — embedding_protocol

Новый эксперимент: замороженный best.pt ID-GNN seed 42 → 128 представлений плюс availability → LightGBM. Обучающие пары и evaluation pools совпадают с ручным baseline; адаптация Appendix C.2 для H&M ranking, не результат авторов. In-sample GNN train embeddings; параметры дерева выбираются только на validation.

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "extracting"
}
```

## 2026-10-14T20:25:12+03:00 — run_start

Начата независимая проверка инференса из best.pt

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/baseline/results/gnn_embeddings_v1/extraction",
    "run_id": "hm_idgnn_embeddings_seed_42_v1",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": false
  },
  "artifacts": "baseline/results/gnn_embeddings_v1/extraction"
}
```

## 2026-10-14T20:25:48+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T20:27:16+03:00 — embedding_progress

Экспорт GNN train: 1280 пользователь-время строк, 14772 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 1280,
  "pairs": 14772,
  "missing_embeddings": 14181
}
```

## 2026-10-14T20:27:17+03:00 — embedding_progress

Экспорт GNN train: 2560 пользователь-время строк, 30740 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 2560,
  "pairs": 30740,
  "missing_embeddings": 28772
}
```

## 2026-10-14T20:27:19+03:00 — embedding_progress

Экспорт GNN train: 3840 пользователь-время строк, 47198 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 3840,
  "pairs": 47198,
  "missing_embeddings": 43307
}
```

## 2026-10-14T20:27:21+03:00 — embedding_progress

Экспорт GNN train: 5120 пользователь-время строк, 64217 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 5120,
  "pairs": 64217,
  "missing_embeddings": 57594
}
```

## 2026-10-14T20:27:22+03:00 — embedding_progress

Экспорт GNN train: 6400 пользователь-время строк, 81365 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 6400,
  "pairs": 81365,
  "missing_embeddings": 71387
}
```

## 2026-10-14T20:27:24+03:00 — embedding_progress

Экспорт GNN train: 7680 пользователь-время строк, 98995 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 7680,
  "pairs": 98995,
  "missing_embeddings": 85600
}
```

## 2026-10-14T20:27:26+03:00 — embedding_progress

Экспорт GNN train: 8960 пользователь-время строк, 116722 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 8960,
  "pairs": 116722,
  "missing_embeddings": 99276
}
```

## 2026-10-14T20:27:30+03:00 — embedding_progress

Экспорт GNN train: 10240 пользователь-время строк, 135060 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 10240,
  "pairs": 135060,
  "missing_embeddings": 113039
}
```

## 2026-10-14T20:27:33+03:00 — embedding_progress

Экспорт GNN train: 11520 пользователь-время строк, 153720 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 11520,
  "pairs": 153720,
  "missing_embeddings": 127482
}
```

## 2026-10-14T20:27:36+03:00 — embedding_memory

Экспортер изменён для ограниченной памяти: один NeighborLoader на split, целевые колонки удалены из всех входов. Граф и веса те же, feature/label протокол не меняется; устранено одновременное хранение трёх CSC копий графа.

## 2026-10-14T20:27:52+03:00 — embedding_protocol

Новый эксперимент: замороженный best.pt ID-GNN seed 42 → 128 представлений плюс availability → LightGBM. Обучающие пары и evaluation pools совпадают с ручным baseline; адаптация Appendix C.2 для H&M ranking, не результат авторов. In-sample GNN train embeddings; параметры дерева выбираются только на validation.

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "extracting"
}
```

## 2026-10-14T20:27:55+03:00 — embedding_pipeline_exit

Эксперимент GNN → LightGBM завершил работу с кодом 143

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "failed"
}
```

## 2026-10-14T20:28:39+03:00 — run_start

Начата независимая проверка инференса из best.pt

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 512,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "temporal_strategy": "last",
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/baseline/results/gnn_embeddings_v1/extraction",
    "run_id": "hm_idgnn_embeddings_seed_42_v1",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": false
  },
  "artifacts": "baseline/results/gnn_embeddings_v1/extraction"
}
```

## 2026-10-14T20:29:14+03:00 — graph_ready

Граф и признаки подготовлены

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "preparing_loaders",
  "nodes": {
    "transactions": 15187287,
    "article": 105542,
    "customer": 1371980
  }
}
```

## 2026-10-14T20:30:15+03:00 — embedding_progress

Экспорт GNN train: 1280 пользователь-время строк, 14772 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 1280,
  "pairs": 14772,
  "missing_embeddings": 14181
}
```

## 2026-10-14T20:30:16+03:00 — embedding_progress

Экспорт GNN train: 2560 пользователь-время строк, 30740 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 2560,
  "pairs": 30740,
  "missing_embeddings": 28772
}
```

## 2026-10-14T20:30:18+03:00 — embedding_progress

Экспорт GNN train: 3840 пользователь-время строк, 47198 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 3840,
  "pairs": 47198,
  "missing_embeddings": 43307
}
```

## 2026-10-14T20:30:19+03:00 — embedding_progress

Экспорт GNN train: 5120 пользователь-время строк, 64217 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 5120,
  "pairs": 64217,
  "missing_embeddings": 57594
}
```

## 2026-10-14T20:30:20+03:00 — embedding_progress

Экспорт GNN train: 6400 пользователь-время строк, 81365 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 6400,
  "pairs": 81365,
  "missing_embeddings": 71387
}
```

## 2026-10-14T20:30:22+03:00 — embedding_progress

Экспорт GNN train: 7680 пользователь-время строк, 98995 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 7680,
  "pairs": 98995,
  "missing_embeddings": 85600
}
```

## 2026-10-14T20:30:24+03:00 — embedding_progress

Экспорт GNN train: 8960 пользователь-время строк, 116722 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 8960,
  "pairs": 116722,
  "missing_embeddings": 99276
}
```

## 2026-10-14T20:30:25+03:00 — embedding_progress

Экспорт GNN train: 10240 пользователь-время строк, 135060 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 10240,
  "pairs": 135060,
  "missing_embeddings": 113039
}
```

## 2026-10-14T20:30:27+03:00 — embedding_progress

Экспорт GNN train: 11520 пользователь-время строк, 153720 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 11520,
  "pairs": 153720,
  "missing_embeddings": 127482
}
```

## 2026-10-14T20:30:28+03:00 — embedding_progress

Экспорт GNN train: 12800 пользователь-время строк, 171939 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 12800,
  "pairs": 171939,
  "missing_embeddings": 141089
}
```

## 2026-10-14T20:30:30+03:00 — embedding_progress

Экспорт GNN train: 14080 пользователь-время строк, 190720 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 14080,
  "pairs": 190720,
  "missing_embeddings": 154801
}
```

## 2026-10-14T20:30:32+03:00 — embedding_progress

Экспорт GNN train: 15360 пользователь-время строк, 210146 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 15360,
  "pairs": 210146,
  "missing_embeddings": 168875
}
```

## 2026-10-14T20:30:33+03:00 — embedding_progress

Экспорт GNN train: 16640 пользователь-время строк, 230171 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 16640,
  "pairs": 230171,
  "missing_embeddings": 183053
}
```

## 2026-10-14T20:30:35+03:00 — embedding_progress

Экспорт GNN train: 17920 пользователь-время строк, 250279 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 17920,
  "pairs": 250279,
  "missing_embeddings": 197147
}
```

## 2026-10-14T20:30:37+03:00 — embedding_progress

Экспорт GNN train: 19200 пользователь-время строк, 270620 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 19200,
  "pairs": 270620,
  "missing_embeddings": 211371
}
```

## 2026-10-14T20:30:39+03:00 — embedding_progress

Экспорт GNN train: 20480 пользователь-время строк, 291584 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 20480,
  "pairs": 291584,
  "missing_embeddings": 225647
}
```

## 2026-10-14T20:30:41+03:00 — embedding_progress

Экспорт GNN train: 21760 пользователь-время строк, 311979 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 21760,
  "pairs": 311979,
  "missing_embeddings": 239603
}
```

## 2026-10-14T20:30:43+03:00 — embedding_progress

Экспорт GNN train: 23040 пользователь-время строк, 332904 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 23040,
  "pairs": 332904,
  "missing_embeddings": 253751
}
```

## 2026-10-14T20:30:45+03:00 — embedding_progress

Экспорт GNN train: 24320 пользователь-время строк, 353712 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 24320,
  "pairs": 353712,
  "missing_embeddings": 268105
}
```

## 2026-10-14T20:30:47+03:00 — embedding_progress

Экспорт GNN train: 25600 пользователь-время строк, 375157 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 25600,
  "pairs": 375157,
  "missing_embeddings": 282490
}
```

## 2026-10-14T20:30:49+03:00 — embedding_progress

Экспорт GNN train: 26880 пользователь-время строк, 396671 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 26880,
  "pairs": 396671,
  "missing_embeddings": 297270
}
```

## 2026-10-14T20:30:51+03:00 — embedding_progress

Экспорт GNN train: 28160 пользователь-время строк, 418967 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 28160,
  "pairs": 418967,
  "missing_embeddings": 312999
}
```

## 2026-10-14T20:30:53+03:00 — embedding_progress

Экспорт GNN train: 29440 пользователь-время строк, 440976 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 29440,
  "pairs": 440976,
  "missing_embeddings": 328499
}
```

## 2026-10-14T20:30:55+03:00 — embedding_progress

Экспорт GNN train: 30720 пользователь-время строк, 462804 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 30720,
  "pairs": 462804,
  "missing_embeddings": 343578
}
```

## 2026-10-14T20:30:57+03:00 — embedding_progress

Экспорт GNN train: 32000 пользователь-время строк, 484541 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 32000,
  "pairs": 484541,
  "missing_embeddings": 358263
}
```

## 2026-10-14T20:30:59+03:00 — embedding_progress

Экспорт GNN train: 33280 пользователь-время строк, 506996 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 33280,
  "pairs": 506996,
  "missing_embeddings": 373278
}
```

## 2026-10-14T20:31:01+03:00 — embedding_progress

Экспорт GNN train: 34560 пользователь-время строк, 529448 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 34560,
  "pairs": 529448,
  "missing_embeddings": 388267
}
```

## 2026-10-14T20:31:03+03:00 — embedding_progress

Экспорт GNN train: 35840 пользователь-время строк, 551897 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 35840,
  "pairs": 551897,
  "missing_embeddings": 403178
}
```

## 2026-10-14T20:31:05+03:00 — embedding_progress

Экспорт GNN train: 37120 пользователь-время строк, 574370 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 37120,
  "pairs": 574370,
  "missing_embeddings": 417783
}
```

## 2026-10-14T20:31:07+03:00 — embedding_progress

Экспорт GNN train: 38400 пользователь-время строк, 597462 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 38400,
  "pairs": 597462,
  "missing_embeddings": 433202
}
```

## 2026-10-14T20:31:09+03:00 — embedding_progress

Экспорт GNN train: 39680 пользователь-время строк, 620379 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 39680,
  "pairs": 620379,
  "missing_embeddings": 448503
}
```

## 2026-10-14T20:31:11+03:00 — embedding_progress

Экспорт GNN train: 40960 пользователь-время строк, 642924 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 40960,
  "pairs": 642924,
  "missing_embeddings": 463159
}
```

## 2026-10-14T20:31:14+03:00 — embedding_progress

Экспорт GNN train: 42240 пользователь-время строк, 665606 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 42240,
  "pairs": 665606,
  "missing_embeddings": 477775
}
```

## 2026-10-14T20:31:16+03:00 — embedding_progress

Экспорт GNN train: 43520 пользователь-время строк, 688250 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 43520,
  "pairs": 688250,
  "missing_embeddings": 492196
}
```

## 2026-10-14T20:31:18+03:00 — embedding_progress

Экспорт GNN train: 44800 пользователь-время строк, 711182 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 44800,
  "pairs": 711182,
  "missing_embeddings": 506800
}
```

## 2026-10-14T20:31:20+03:00 — embedding_progress

Экспорт GNN train: 46080 пользователь-время строк, 734008 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 46080,
  "pairs": 734008,
  "missing_embeddings": 521357
}
```

## 2026-10-14T20:31:22+03:00 — embedding_progress

Экспорт GNN train: 47360 пользователь-время строк, 756873 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 47360,
  "pairs": 756873,
  "missing_embeddings": 535728
}
```

## 2026-10-14T20:31:24+03:00 — embedding_progress

Экспорт GNN train: 48640 пользователь-время строк, 779391 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 48640,
  "pairs": 779391,
  "missing_embeddings": 549912
}
```

## 2026-10-14T20:31:26+03:00 — embedding_progress

Экспорт GNN train: 49920 пользователь-время строк, 802015 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 49920,
  "pairs": 802015,
  "missing_embeddings": 564169
}
```

## 2026-10-14T20:31:27+03:00 — embedding_progress

Экспорт GNN train: 50000 пользователь-время строк, 803377 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_train",
  "split": "train",
  "users": 50000,
  "pairs": 803377,
  "missing_embeddings": 565051
}
```

## 2026-10-14T20:31:38+03:00 — embedding_progress

Экспорт GNN val: 1280 пользователь-время строк, 36826 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 1280,
  "pairs": 36826,
  "missing_embeddings": 3806
}
```

## 2026-10-14T20:31:40+03:00 — embedding_progress

Экспорт GNN val: 2560 пользователь-время строк, 72650 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 2560,
  "pairs": 72650,
  "missing_embeddings": 7761
}
```

## 2026-10-14T20:31:42+03:00 — embedding_progress

Экспорт GNN val: 3840 пользователь-время строк, 108808 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 3840,
  "pairs": 108808,
  "missing_embeddings": 11464
}
```

## 2026-10-14T20:31:44+03:00 — embedding_progress

Экспорт GNN val: 5120 пользователь-время строк, 145671 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 5120,
  "pairs": 145671,
  "missing_embeddings": 15338
}
```

## 2026-10-14T20:31:46+03:00 — embedding_progress

Экспорт GNN val: 6400 пользователь-время строк, 181243 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 6400,
  "pairs": 181243,
  "missing_embeddings": 19426
}
```

## 2026-10-14T20:31:47+03:00 — embedding_progress

Экспорт GNN val: 7680 пользователь-время строк, 216754 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 7680,
  "pairs": 216754,
  "missing_embeddings": 23207
}
```

## 2026-10-14T20:31:49+03:00 — embedding_progress

Экспорт GNN val: 8960 пользователь-время строк, 255309 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 8960,
  "pairs": 255309,
  "missing_embeddings": 26864
}
```

## 2026-10-14T20:31:51+03:00 — embedding_progress

Экспорт GNN val: 10240 пользователь-время строк, 292548 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 10240,
  "pairs": 292548,
  "missing_embeddings": 30696
}
```

## 2026-10-14T20:31:53+03:00 — embedding_progress

Экспорт GNN val: 11520 пользователь-время строк, 328658 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 11520,
  "pairs": 328658,
  "missing_embeddings": 34351
}
```

## 2026-10-14T20:31:55+03:00 — embedding_progress

Экспорт GNN val: 12800 пользователь-время строк, 362881 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 12800,
  "pairs": 362881,
  "missing_embeddings": 38287
}
```

## 2026-10-14T20:31:57+03:00 — embedding_progress

Экспорт GNN val: 14080 пользователь-время строк, 398228 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 14080,
  "pairs": 398228,
  "missing_embeddings": 41907
}
```

## 2026-10-14T20:31:59+03:00 — embedding_progress

Экспорт GNN val: 15360 пользователь-время строк, 433614 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 15360,
  "pairs": 433614,
  "missing_embeddings": 45976
}
```

## 2026-10-14T20:32:01+03:00 — embedding_progress

Экспорт GNN val: 16640 пользователь-время строк, 468305 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 16640,
  "pairs": 468305,
  "missing_embeddings": 49893
}
```

## 2026-10-14T20:32:03+03:00 — embedding_progress

Экспорт GNN val: 17920 пользователь-время строк, 503136 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 17920,
  "pairs": 503136,
  "missing_embeddings": 53685
}
```

## 2026-10-14T20:32:05+03:00 — embedding_progress

Экспорт GNN val: 19200 пользователь-время строк, 537961 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 19200,
  "pairs": 537961,
  "missing_embeddings": 57860
}
```

## 2026-10-14T20:32:06+03:00 — embedding_progress

Экспорт GNN val: 20480 пользователь-время строк, 572588 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 20480,
  "pairs": 572588,
  "missing_embeddings": 62017
}
```

## 2026-10-14T20:32:08+03:00 — embedding_progress

Экспорт GNN val: 21760 пользователь-время строк, 608304 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 21760,
  "pairs": 608304,
  "missing_embeddings": 65938
}
```

## 2026-10-14T20:32:10+03:00 — embedding_progress

Экспорт GNN val: 23040 пользователь-время строк, 644069 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 23040,
  "pairs": 644069,
  "missing_embeddings": 69790
}
```

## 2026-10-14T20:32:12+03:00 — embedding_progress

Экспорт GNN val: 24320 пользователь-время строк, 678554 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 24320,
  "pairs": 678554,
  "missing_embeddings": 73898
}
```

## 2026-10-14T20:32:14+03:00 — embedding_progress

Экспорт GNN val: 25600 пользователь-время строк, 715124 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 25600,
  "pairs": 715124,
  "missing_embeddings": 77736
}
```

## 2026-10-14T20:32:16+03:00 — embedding_progress

Экспорт GNN val: 26880 пользователь-время строк, 751633 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 26880,
  "pairs": 751633,
  "missing_embeddings": 81472
}
```

## 2026-10-14T20:32:18+03:00 — embedding_progress

Экспорт GNN val: 28160 пользователь-время строк, 788189 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 28160,
  "pairs": 788189,
  "missing_embeddings": 85120
}
```

## 2026-10-14T20:32:19+03:00 — embedding_progress

Экспорт GNN val: 29440 пользователь-время строк, 826224 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 29440,
  "pairs": 826224,
  "missing_embeddings": 88939
}
```

## 2026-10-14T20:32:21+03:00 — embedding_progress

Экспорт GNN val: 30720 пользователь-время строк, 861822 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 30720,
  "pairs": 861822,
  "missing_embeddings": 93016
}
```

## 2026-10-14T20:32:23+03:00 — embedding_progress

Экспорт GNN val: 32000 пользователь-время строк, 897907 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 32000,
  "pairs": 897907,
  "missing_embeddings": 96579
}
```

## 2026-10-14T20:32:25+03:00 — embedding_progress

Экспорт GNN val: 33280 пользователь-время строк, 934274 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 33280,
  "pairs": 934274,
  "missing_embeddings": 100288
}
```

## 2026-10-14T20:32:27+03:00 — embedding_progress

Экспорт GNN val: 34560 пользователь-время строк, 969898 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 34560,
  "pairs": 969898,
  "missing_embeddings": 104206
}
```

## 2026-10-14T20:32:29+03:00 — embedding_progress

Экспорт GNN val: 35840 пользователь-время строк, 1006373 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 35840,
  "pairs": 1006373,
  "missing_embeddings": 107911
}
```

## 2026-10-14T20:32:31+03:00 — embedding_progress

Экспорт GNN val: 37120 пользователь-время строк, 1043035 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 37120,
  "pairs": 1043035,
  "missing_embeddings": 111612
}
```

## 2026-10-14T20:32:32+03:00 — embedding_progress

Экспорт GNN val: 38400 пользователь-время строк, 1078609 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 38400,
  "pairs": 1078609,
  "missing_embeddings": 115336
}
```

## 2026-10-14T20:32:34+03:00 — embedding_progress

Экспорт GNN val: 39680 пользователь-время строк, 1113612 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 39680,
  "pairs": 1113612,
  "missing_embeddings": 119164
}
```

## 2026-10-14T20:32:36+03:00 — embedding_progress

Экспорт GNN val: 40960 пользователь-время строк, 1151223 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 40960,
  "pairs": 1151223,
  "missing_embeddings": 122821
}
```

## 2026-10-14T20:32:38+03:00 — embedding_progress

Экспорт GNN val: 42240 пользователь-время строк, 1186862 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 42240,
  "pairs": 1186862,
  "missing_embeddings": 126706
}
```

## 2026-10-14T20:32:41+03:00 — embedding_progress

Экспорт GNN val: 43520 пользователь-время строк, 1222219 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 43520,
  "pairs": 1222219,
  "missing_embeddings": 130505
}
```

## 2026-10-14T20:32:42+03:00 — embedding_progress

Экспорт GNN val: 44800 пользователь-время строк, 1259178 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 44800,
  "pairs": 1259178,
  "missing_embeddings": 134343
}
```

## 2026-10-14T20:32:44+03:00 — embedding_progress

Экспорт GNN val: 46080 пользователь-время строк, 1294674 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 46080,
  "pairs": 1294674,
  "missing_embeddings": 138252
}
```

## 2026-10-14T20:32:46+03:00 — embedding_progress

Экспорт GNN val: 47360 пользователь-время строк, 1331140 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 47360,
  "pairs": 1331140,
  "missing_embeddings": 142089
}
```

## 2026-10-14T20:32:48+03:00 — embedding_progress

Экспорт GNN val: 48640 пользователь-время строк, 1367130 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 48640,
  "pairs": 1367130,
  "missing_embeddings": 146064
}
```

## 2026-10-14T20:32:50+03:00 — embedding_progress

Экспорт GNN val: 49920 пользователь-время строк, 1401459 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 49920,
  "pairs": 1401459,
  "missing_embeddings": 150035
}
```

## 2026-10-14T20:32:52+03:00 — embedding_progress

Экспорт GNN val: 51200 пользователь-время строк, 1436904 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 51200,
  "pairs": 1436904,
  "missing_embeddings": 153989
}
```

## 2026-10-14T20:32:54+03:00 — embedding_progress

Экспорт GNN val: 52480 пользователь-время строк, 1471813 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 52480,
  "pairs": 1471813,
  "missing_embeddings": 157995
}
```

## 2026-10-14T20:32:56+03:00 — embedding_progress

Экспорт GNN val: 53760 пользователь-время строк, 1506095 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 53760,
  "pairs": 1506095,
  "missing_embeddings": 161887
}
```

## 2026-10-14T20:32:58+03:00 — embedding_progress

Экспорт GNN val: 55040 пользователь-время строк, 1542283 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 55040,
  "pairs": 1542283,
  "missing_embeddings": 165595
}
```

## 2026-10-14T20:33:00+03:00 — embedding_progress

Экспорт GNN val: 56320 пользователь-время строк, 1578663 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 56320,
  "pairs": 1578663,
  "missing_embeddings": 169432
}
```

## 2026-10-14T20:33:01+03:00 — embedding_progress

Экспорт GNN val: 57600 пользователь-время строк, 1612613 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 57600,
  "pairs": 1612613,
  "missing_embeddings": 173478
}
```

## 2026-10-14T20:33:03+03:00 — embedding_progress

Экспорт GNN val: 58880 пользователь-время строк, 1649113 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 58880,
  "pairs": 1649113,
  "missing_embeddings": 177266
}
```

## 2026-10-14T20:33:05+03:00 — embedding_progress

Экспорт GNN val: 60160 пользователь-время строк, 1686158 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 60160,
  "pairs": 1686158,
  "missing_embeddings": 181001
}
```

## 2026-10-14T20:33:07+03:00 — embedding_progress

Экспорт GNN val: 61440 пользователь-время строк, 1722701 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 61440,
  "pairs": 1722701,
  "missing_embeddings": 184799
}
```

## 2026-10-14T20:33:09+03:00 — embedding_progress

Экспорт GNN val: 62720 пользователь-время строк, 1758694 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 62720,
  "pairs": 1758694,
  "missing_embeddings": 188681
}
```

## 2026-10-14T20:33:11+03:00 — embedding_progress

Экспорт GNN val: 64000 пользователь-время строк, 1794915 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 64000,
  "pairs": 1794915,
  "missing_embeddings": 192275
}
```

## 2026-10-14T20:33:14+03:00 — embedding_progress

Экспорт GNN val: 65280 пользователь-время строк, 1829516 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 65280,
  "pairs": 1829516,
  "missing_embeddings": 196159
}
```

## 2026-10-14T20:33:15+03:00 — embedding_progress

Экспорт GNN val: 66560 пользователь-время строк, 1865704 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 66560,
  "pairs": 1865704,
  "missing_embeddings": 200157
}
```

## 2026-10-14T20:33:17+03:00 — embedding_progress

Экспорт GNN val: 67840 пользователь-время строк, 1901401 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 67840,
  "pairs": 1901401,
  "missing_embeddings": 203795
}
```

## 2026-10-14T20:33:19+03:00 — embedding_progress

Экспорт GNN val: 69120 пользователь-время строк, 1937468 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 69120,
  "pairs": 1937468,
  "missing_embeddings": 207494
}
```

## 2026-10-14T20:33:21+03:00 — embedding_progress

Экспорт GNN val: 70400 пользователь-время строк, 1972789 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 70400,
  "pairs": 1972789,
  "missing_embeddings": 211356
}
```

## 2026-10-14T20:33:23+03:00 — embedding_progress

Экспорт GNN val: 71680 пользователь-время строк, 2008759 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 71680,
  "pairs": 2008759,
  "missing_embeddings": 215105
}
```

## 2026-10-14T20:33:25+03:00 — embedding_progress

Экспорт GNN val: 72960 пользователь-время строк, 2043548 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 72960,
  "pairs": 2043548,
  "missing_embeddings": 218749
}
```

## 2026-10-14T20:33:27+03:00 — embedding_progress

Экспорт GNN val: 74240 пользователь-время строк, 2079125 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 74240,
  "pairs": 2079125,
  "missing_embeddings": 222446
}
```

## 2026-10-14T20:33:28+03:00 — embedding_progress

Экспорт GNN val: 74575 пользователь-время строк, 2088583 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_val",
  "split": "val",
  "users": 74575,
  "pairs": 2088583,
  "missing_embeddings": 223414
}
```

## 2026-10-14T20:33:38+03:00 — embedding_progress

Экспорт GNN test: 1280 пользователь-время строк, 37436 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 1280,
  "pairs": 37436,
  "missing_embeddings": 3845
}
```

## 2026-10-14T20:33:40+03:00 — embedding_progress

Экспорт GNN test: 2560 пользователь-время строк, 74368 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 2560,
  "pairs": 74368,
  "missing_embeddings": 7595
}
```

## 2026-10-14T20:33:42+03:00 — embedding_progress

Экспорт GNN test: 3840 пользователь-время строк, 111331 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 3840,
  "pairs": 111331,
  "missing_embeddings": 11426
}
```

## 2026-10-14T20:33:44+03:00 — embedding_progress

Экспорт GNN test: 5120 пользователь-время строк, 148927 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 5120,
  "pairs": 148927,
  "missing_embeddings": 15112
}
```

## 2026-10-14T20:33:45+03:00 — embedding_progress

Экспорт GNN test: 6400 пользователь-время строк, 184657 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 6400,
  "pairs": 184657,
  "missing_embeddings": 18975
}
```

## 2026-10-14T20:33:47+03:00 — embedding_progress

Экспорт GNN test: 7680 пользователь-время строк, 221374 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 7680,
  "pairs": 221374,
  "missing_embeddings": 22847
}
```

## 2026-10-14T20:33:49+03:00 — embedding_progress

Экспорт GNN test: 8960 пользователь-время строк, 259120 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 8960,
  "pairs": 259120,
  "missing_embeddings": 26477
}
```

## 2026-10-14T20:33:51+03:00 — embedding_progress

Экспорт GNN test: 10240 пользователь-время строк, 294521 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 10240,
  "pairs": 294521,
  "missing_embeddings": 30360
}
```

## 2026-10-14T20:33:52+03:00 — embedding_progress

Экспорт GNN test: 11520 пользователь-время строк, 330126 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 11520,
  "pairs": 330126,
  "missing_embeddings": 34358
}
```

## 2026-10-14T20:33:54+03:00 — embedding_progress

Экспорт GNN test: 12800 пользователь-время строк, 367332 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 12800,
  "pairs": 367332,
  "missing_embeddings": 37861
}
```

## 2026-10-14T20:33:56+03:00 — embedding_progress

Экспорт GNN test: 14080 пользователь-время строк, 404532 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 14080,
  "pairs": 404532,
  "missing_embeddings": 41806
}
```

## 2026-10-14T20:33:58+03:00 — embedding_progress

Экспорт GNN test: 15360 пользователь-время строк, 440181 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 15360,
  "pairs": 440181,
  "missing_embeddings": 45649
}
```

## 2026-10-14T20:34:00+03:00 — embedding_progress

Экспорт GNN test: 16640 пользователь-время строк, 475044 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 16640,
  "pairs": 475044,
  "missing_embeddings": 49469
}
```

## 2026-10-14T20:34:01+03:00 — embedding_progress

Экспорт GNN test: 17920 пользователь-время строк, 511300 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 17920,
  "pairs": 511300,
  "missing_embeddings": 53255
}
```

## 2026-10-14T20:34:03+03:00 — embedding_progress

Экспорт GNN test: 19200 пользователь-время строк, 546947 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 19200,
  "pairs": 546947,
  "missing_embeddings": 57160
}
```

## 2026-10-14T20:34:05+03:00 — embedding_progress

Экспорт GNN test: 20480 пользователь-время строк, 582820 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 20480,
  "pairs": 582820,
  "missing_embeddings": 61043
}
```

## 2026-10-14T20:34:07+03:00 — embedding_progress

Экспорт GNN test: 21760 пользователь-время строк, 618289 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 21760,
  "pairs": 618289,
  "missing_embeddings": 64823
}
```

## 2026-10-14T20:34:09+03:00 — embedding_progress

Экспорт GNN test: 23040 пользователь-время строк, 654404 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 23040,
  "pairs": 654404,
  "missing_embeddings": 68773
}
```

## 2026-10-14T20:34:10+03:00 — embedding_progress

Экспорт GNN test: 24320 пользователь-время строк, 688883 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 24320,
  "pairs": 688883,
  "missing_embeddings": 72910
}
```

## 2026-10-14T20:34:12+03:00 — embedding_progress

Экспорт GNN test: 25600 пользователь-время строк, 724354 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 25600,
  "pairs": 724354,
  "missing_embeddings": 77015
}
```

## 2026-10-14T20:34:14+03:00 — embedding_progress

Экспорт GNN test: 26880 пользователь-время строк, 761129 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 26880,
  "pairs": 761129,
  "missing_embeddings": 80736
}
```

## 2026-10-14T20:34:16+03:00 — embedding_progress

Экспорт GNN test: 28160 пользователь-время строк, 797399 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 28160,
  "pairs": 797399,
  "missing_embeddings": 84443
}
```

## 2026-10-14T20:34:17+03:00 — embedding_progress

Экспорт GNN test: 29440 пользователь-время строк, 834140 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 29440,
  "pairs": 834140,
  "missing_embeddings": 88009
}
```

## 2026-10-14T20:34:19+03:00 — embedding_progress

Экспорт GNN test: 30720 пользователь-время строк, 869919 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 30720,
  "pairs": 869919,
  "missing_embeddings": 91810
}
```

## 2026-10-14T20:34:21+03:00 — embedding_progress

Экспорт GNN test: 32000 пользователь-время строк, 906620 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 32000,
  "pairs": 906620,
  "missing_embeddings": 95579
}
```

## 2026-10-14T20:34:23+03:00 — embedding_progress

Экспорт GNN test: 33280 пользователь-время строк, 942652 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 33280,
  "pairs": 942652,
  "missing_embeddings": 99463
}
```

## 2026-10-14T20:34:25+03:00 — embedding_progress

Экспорт GNN test: 34560 пользователь-время строк, 977475 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 34560,
  "pairs": 977475,
  "missing_embeddings": 103341
}
```

## 2026-10-14T20:34:27+03:00 — embedding_progress

Экспорт GNN test: 35840 пользователь-время строк, 1013013 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 35840,
  "pairs": 1013013,
  "missing_embeddings": 107308
}
```

## 2026-10-14T20:34:29+03:00 — embedding_progress

Экспорт GNN test: 37120 пользователь-время строк, 1049917 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 37120,
  "pairs": 1049917,
  "missing_embeddings": 110904
}
```

## 2026-10-14T20:34:31+03:00 — embedding_progress

Экспорт GNN test: 38400 пользователь-время строк, 1085448 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 38400,
  "pairs": 1085448,
  "missing_embeddings": 114631
}
```

## 2026-10-14T20:34:34+03:00 — embedding_progress

Экспорт GNN test: 39680 пользователь-время строк, 1122529 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 39680,
  "pairs": 1122529,
  "missing_embeddings": 118401
}
```

## 2026-10-14T20:34:36+03:00 — embedding_progress

Экспорт GNN test: 40960 пользователь-время строк, 1158495 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 40960,
  "pairs": 1158495,
  "missing_embeddings": 122211
}
```

## 2026-10-14T20:34:38+03:00 — embedding_progress

Экспорт GNN test: 42240 пользователь-время строк, 1194810 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 42240,
  "pairs": 1194810,
  "missing_embeddings": 126272
}
```

## 2026-10-14T20:34:40+03:00 — embedding_progress

Экспорт GNN test: 43520 пользователь-время строк, 1229779 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 43520,
  "pairs": 1229779,
  "missing_embeddings": 130096
}
```

## 2026-10-14T20:34:42+03:00 — embedding_progress

Экспорт GNN test: 44800 пользователь-время строк, 1264736 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 44800,
  "pairs": 1264736,
  "missing_embeddings": 134097
}
```

## 2026-10-14T20:34:43+03:00 — embedding_progress

Экспорт GNN test: 46080 пользователь-время строк, 1298597 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 46080,
  "pairs": 1298597,
  "missing_embeddings": 138015
}
```

## 2026-10-14T20:34:45+03:00 — embedding_progress

Экспорт GNN test: 47360 пользователь-время строк, 1334860 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 47360,
  "pairs": 1334860,
  "missing_embeddings": 141563
}
```

## 2026-10-14T20:34:46+03:00 — embedding_progress

Экспорт GNN test: 48640 пользователь-время строк, 1369426 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 48640,
  "pairs": 1369426,
  "missing_embeddings": 145425
}
```

## 2026-10-14T20:34:48+03:00 — embedding_progress

Экспорт GNN test: 49920 пользователь-время строк, 1405804 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 49920,
  "pairs": 1405804,
  "missing_embeddings": 149176
}
```

## 2026-10-14T20:34:50+03:00 — embedding_progress

Экспорт GNN test: 51200 пользователь-время строк, 1442604 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 51200,
  "pairs": 1442604,
  "missing_embeddings": 152756
}
```

## 2026-10-14T20:34:52+03:00 — embedding_progress

Экспорт GNN test: 52480 пользователь-время строк, 1478174 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 52480,
  "pairs": 1478174,
  "missing_embeddings": 156989
}
```

## 2026-10-14T20:34:54+03:00 — embedding_progress

Экспорт GNN test: 53760 пользователь-время строк, 1514088 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 53760,
  "pairs": 1514088,
  "missing_embeddings": 160754
}
```

## 2026-10-14T20:34:56+03:00 — embedding_progress

Экспорт GNN test: 55040 пользователь-время строк, 1550922 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 55040,
  "pairs": 1550922,
  "missing_embeddings": 164602
}
```

## 2026-10-14T20:34:58+03:00 — embedding_progress

Экспорт GNN test: 56320 пользователь-время строк, 1587507 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 56320,
  "pairs": 1587507,
  "missing_embeddings": 168669
}
```

## 2026-10-14T20:34:59+03:00 — embedding_progress

Экспорт GNN test: 57600 пользователь-время строк, 1624056 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 57600,
  "pairs": 1624056,
  "missing_embeddings": 172491
}
```

## 2026-10-14T20:35:01+03:00 — embedding_progress

Экспорт GNN test: 58880 пользователь-время строк, 1660278 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 58880,
  "pairs": 1660278,
  "missing_embeddings": 176037
}
```

## 2026-10-14T20:35:03+03:00 — embedding_progress

Экспорт GNN test: 60160 пользователь-время строк, 1696337 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 60160,
  "pairs": 1696337,
  "missing_embeddings": 179849
}
```

## 2026-10-14T20:35:04+03:00 — embedding_progress

Экспорт GNN test: 61440 пользователь-время строк, 1732900 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 61440,
  "pairs": 1732900,
  "missing_embeddings": 183852
}
```

## 2026-10-14T20:35:06+03:00 — embedding_progress

Экспорт GNN test: 62720 пользователь-время строк, 1767956 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 62720,
  "pairs": 1767956,
  "missing_embeddings": 188055
}
```

## 2026-10-14T20:35:08+03:00 — embedding_progress

Экспорт GNN test: 64000 пользователь-время строк, 1805521 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 64000,
  "pairs": 1805521,
  "missing_embeddings": 191920
}
```

## 2026-10-14T20:35:10+03:00 — embedding_progress

Экспорт GNN test: 65280 пользователь-время строк, 1840641 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 65280,
  "pairs": 1840641,
  "missing_embeddings": 195785
}
```

## 2026-10-14T20:35:12+03:00 — embedding_progress

Экспорт GNN test: 66560 пользователь-время строк, 1876423 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 66560,
  "pairs": 1876423,
  "missing_embeddings": 199508
}
```

## 2026-10-14T20:35:12+03:00 — embedding_progress

Экспорт GNN test: 67144 пользователь-время строк, 1892405 пар

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "export_test",
  "split": "test",
  "users": 67144,
  "pairs": 1892405,
  "missing_embeddings": 201178
}
```

## 2026-10-14T20:35:12+03:00 — embedding_export_complete

128 представлений GNN экспортированы; пары обучения совпадают с ручным baseline, val/test сверены с предсказаниями GNN

Запуск: `hm_idgnn_embeddings_seed_42_v1`.

```json
{
  "status": "complete",
  "config": {
    "features": [
      "gnn_000",
      "gnn_001",
      "gnn_002",
      "gnn_003",
      "gnn_004",
      "gnn_005",
      "gnn_006",
      "gnn_007",
      "gnn_008",
      "gnn_009",
      "gnn_010",
      "gnn_011",
      "gnn_012",
      "gnn_013",
      "gnn_014",
      "gnn_015",
      "gnn_016",
      "gnn_017",
      "gnn_018",
      "gnn_019",
      "gnn_020",
      "gnn_021",
      "gnn_022",
      "gnn_023",
      "gnn_024",
      "gnn_025",
      "gnn_026",
      "gnn_027",
      "gnn_028",
      "gnn_029",
      "gnn_030",
      "gnn_031",
      "gnn_032",
      "gnn_033",
      "gnn_034",
      "gnn_035",
      "gnn_036",
      "gnn_037",
      "gnn_038",
      "gnn_039",
      "gnn_040",
      "gnn_041",
      "gnn_042",
      "gnn_043",
      "gnn_044",
      "gnn_045",
      "gnn_046",
      "gnn_047",
      "gnn_048",
      "gnn_049",
      "gnn_050",
      "gnn_051",
      "gnn_052",
      "gnn_053",
      "gnn_054",
      "gnn_055",
      "gnn_056",
      "gnn_057",
      "gnn_058",
      "gnn_059",
      "gnn_060",
      "gnn_061",
      "gnn_062",
      "gnn_063",
      "gnn_064",
      "gnn_065",
      "gnn_066",
      "gnn_067",
      "gnn_068",
      "gnn_069",
      "gnn_070",
      "gnn_071",
      "gnn_072",
      "gnn_073",
      "gnn_074",
      "gnn_075",
      "gnn_076",
      "gnn_077",
      "gnn_078",
      "gnn_079",
      "gnn_080",
      "gnn_081",
      "gnn_082",
      "gnn_083",
      "gnn_084",
      "gnn_085",
      "gnn_086",
      "gnn_087",
      "gnn_088",
      "gnn_089",
      "gnn_090",
      "gnn_091",
      "gnn_092",
      "gnn_093",
      "gnn_094",
      "gnn_095",
      "gnn_096",
      "gnn_097",
      "gnn_098",
      "gnn_099",
      "gnn_100",
      "gnn_101",
      "gnn_102",
      "gnn_103",
      "gnn_104",
      "gnn_105",
      "gnn_106",
      "gnn_107",
      "gnn_108",
      "gnn_109",
      "gnn_110",
      "gnn_111",
      "gnn_112",
      "gnn_113",
      "gnn_114",
      "gnn_115",
      "gnn_116",
      "gnn_117",
      "gnn_118",
      "gnn_119",
      "gnn_120",
      "gnn_121",
      "gnn_122",
      "gnn_123",
      "gnn_124",
      "gnn_125",
      "gnn_126",
      "gnn_127",
      "gnn_available"
    ],
    "checkpoint_sha256": "f5439416aeeb6f0f2dedab20aabb14ea541b4bd98b70f21334986dc03a05abc4",
    "seed": 42,
    "train_user_times": 50000,
    "files": {
      "train": [
        "baseline/cache/gnn_embeddings_v1/train/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0039.parquet"
      ],
      "val": [
        "baseline/cache/gnn_embeddings_v1/val/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0039.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0040.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0041.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0042.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0043.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0044.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0045.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0046.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0047.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0048.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0049.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0050.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0051.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0052.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0053.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0054.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0055.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0056.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0057.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0058.parquet"
      ],
      "test": [
        "baseline/cache/gnn_embeddings_v1/test/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0039.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0040.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0041.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0042.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0043.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0044.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0045.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0046.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0047.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0048.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0049.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0050.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0051.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0052.parquet"
      ]
    },
    "counts": {
      "train": {
        "user_times": 50000,
        "pairs": 803377,
        "missing_embeddings": 565051
      },
      "val": {
        "user_times": 74575,
        "pairs": 2088583,
        "missing_embeddings": 223414
      },
      "test": {
        "user_times": 67144,
        "pairs": 1892405,
        "missing_embeddings": 201178
      }
    },
    "missing_policy": "Zero vector plus gnn_available=0 for pairs outside sampled graph; no head logits in features"
  },
  "artifacts": "baseline/cache/gnn_embeddings_v1/manifest.json"
}
```

## 2026-10-14T20:35:31+03:00 — embedding_tree_start

LightGBM обучается на замороженных представлениях ID-GNN; tuning только validation

Запуск: `hm_idgnn_lightgbm_embeddings_seed_42_v1`.

```json
{
  "status": "tuning",
  "config": {
    "features": [
      "gnn_000",
      "gnn_001",
      "gnn_002",
      "gnn_003",
      "gnn_004",
      "gnn_005",
      "gnn_006",
      "gnn_007",
      "gnn_008",
      "gnn_009",
      "gnn_010",
      "gnn_011",
      "gnn_012",
      "gnn_013",
      "gnn_014",
      "gnn_015",
      "gnn_016",
      "gnn_017",
      "gnn_018",
      "gnn_019",
      "gnn_020",
      "gnn_021",
      "gnn_022",
      "gnn_023",
      "gnn_024",
      "gnn_025",
      "gnn_026",
      "gnn_027",
      "gnn_028",
      "gnn_029",
      "gnn_030",
      "gnn_031",
      "gnn_032",
      "gnn_033",
      "gnn_034",
      "gnn_035",
      "gnn_036",
      "gnn_037",
      "gnn_038",
      "gnn_039",
      "gnn_040",
      "gnn_041",
      "gnn_042",
      "gnn_043",
      "gnn_044",
      "gnn_045",
      "gnn_046",
      "gnn_047",
      "gnn_048",
      "gnn_049",
      "gnn_050",
      "gnn_051",
      "gnn_052",
      "gnn_053",
      "gnn_054",
      "gnn_055",
      "gnn_056",
      "gnn_057",
      "gnn_058",
      "gnn_059",
      "gnn_060",
      "gnn_061",
      "gnn_062",
      "gnn_063",
      "gnn_064",
      "gnn_065",
      "gnn_066",
      "gnn_067",
      "gnn_068",
      "gnn_069",
      "gnn_070",
      "gnn_071",
      "gnn_072",
      "gnn_073",
      "gnn_074",
      "gnn_075",
      "gnn_076",
      "gnn_077",
      "gnn_078",
      "gnn_079",
      "gnn_080",
      "gnn_081",
      "gnn_082",
      "gnn_083",
      "gnn_084",
      "gnn_085",
      "gnn_086",
      "gnn_087",
      "gnn_088",
      "gnn_089",
      "gnn_090",
      "gnn_091",
      "gnn_092",
      "gnn_093",
      "gnn_094",
      "gnn_095",
      "gnn_096",
      "gnn_097",
      "gnn_098",
      "gnn_099",
      "gnn_100",
      "gnn_101",
      "gnn_102",
      "gnn_103",
      "gnn_104",
      "gnn_105",
      "gnn_106",
      "gnn_107",
      "gnn_108",
      "gnn_109",
      "gnn_110",
      "gnn_111",
      "gnn_112",
      "gnn_113",
      "gnn_114",
      "gnn_115",
      "gnn_116",
      "gnn_117",
      "gnn_118",
      "gnn_119",
      "gnn_120",
      "gnn_121",
      "gnn_122",
      "gnn_123",
      "gnn_124",
      "gnn_125",
      "gnn_126",
      "gnn_127",
      "gnn_available"
    ],
    "checkpoint_sha256": "f5439416aeeb6f0f2dedab20aabb14ea541b4bd98b70f21334986dc03a05abc4",
    "seed": 42,
    "train_user_times": 50000,
    "files": {
      "train": [
        "baseline/cache/gnn_embeddings_v1/train/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/train/part_0039.parquet"
      ],
      "val": [
        "baseline/cache/gnn_embeddings_v1/val/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0039.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0040.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0041.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0042.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0043.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0044.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0045.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0046.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0047.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0048.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0049.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0050.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0051.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0052.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0053.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0054.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0055.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0056.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0057.parquet",
        "baseline/cache/gnn_embeddings_v1/val/part_0058.parquet"
      ],
      "test": [
        "baseline/cache/gnn_embeddings_v1/test/part_0000.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0001.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0002.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0003.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0004.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0005.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0006.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0007.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0008.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0009.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0010.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0011.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0012.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0013.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0014.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0015.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0016.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0017.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0018.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0019.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0020.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0021.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0022.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0023.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0024.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0025.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0026.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0027.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0028.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0029.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0030.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0031.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0032.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0033.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0034.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0035.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0036.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0037.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0038.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0039.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0040.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0041.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0042.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0043.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0044.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0045.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0046.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0047.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0048.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0049.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0050.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0051.parquet",
        "baseline/cache/gnn_embeddings_v1/test/part_0052.parquet"
      ]
    },
    "counts": {
      "train": {
        "user_times": 50000,
        "pairs": 803377,
        "missing_embeddings": 565051
      },
      "val": {
        "user_times": 74575,
        "pairs": 2088583,
        "missing_embeddings": 223414
      },
      "test": {
        "user_times": 67144,
        "pairs": 1892405,
        "missing_embeddings": 201178
      }
    },
    "missing_policy": "Zero vector plus gnn_available=0 for pairs outside sampled graph; no head logits in features"
  }
}
```

## 2026-10-14T20:35:44+03:00 — embedding_tree_trial

LightGBM embeddings: num_leaves=15, tuning MAP=0.020222546754652272

Запуск: `hm_idgnn_lightgbm_embeddings_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 15,
    "val_tuning_map": 0.020222546754652272
  }
}
```

## 2026-10-14T20:35:52+03:00 — embedding_tree_trial

LightGBM embeddings: num_leaves=31, tuning MAP=0.01985744579465548

Запуск: `hm_idgnn_lightgbm_embeddings_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 31,
    "val_tuning_map": 0.01985744579465548
  }
}
```

## 2026-10-14T20:36:08+03:00 — embedding_tree_complete

LightGBM на представлениях GNN обучен и оценён после загрузки сохранённой модели

Запуск: `hm_idgnn_lightgbm_embeddings_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.019711562867923985
  },
  "test_metrics": {
    "map": 0.021245096686483916
  },
  "config": {
    "model": "ID-GNN embeddings + LightGBM",
    "seed": 42,
    "feature_count": 129,
    "features": [
      "gnn_000",
      "gnn_001",
      "gnn_002",
      "gnn_003",
      "gnn_004",
      "gnn_005",
      "gnn_006",
      "gnn_007",
      "gnn_008",
      "gnn_009",
      "gnn_010",
      "gnn_011",
      "gnn_012",
      "gnn_013",
      "gnn_014",
      "gnn_015",
      "gnn_016",
      "gnn_017",
      "gnn_018",
      "gnn_019",
      "gnn_020",
      "gnn_021",
      "gnn_022",
      "gnn_023",
      "gnn_024",
      "gnn_025",
      "gnn_026",
      "gnn_027",
      "gnn_028",
      "gnn_029",
      "gnn_030",
      "gnn_031",
      "gnn_032",
      "gnn_033",
      "gnn_034",
      "gnn_035",
      "gnn_036",
      "gnn_037",
      "gnn_038",
      "gnn_039",
      "gnn_040",
      "gnn_041",
      "gnn_042",
      "gnn_043",
      "gnn_044",
      "gnn_045",
      "gnn_046",
      "gnn_047",
      "gnn_048",
      "gnn_049",
      "gnn_050",
      "gnn_051",
      "gnn_052",
      "gnn_053",
      "gnn_054",
      "gnn_055",
      "gnn_056",
      "gnn_057",
      "gnn_058",
      "gnn_059",
      "gnn_060",
      "gnn_061",
      "gnn_062",
      "gnn_063",
      "gnn_064",
      "gnn_065",
      "gnn_066",
      "gnn_067",
      "gnn_068",
      "gnn_069",
      "gnn_070",
      "gnn_071",
      "gnn_072",
      "gnn_073",
      "gnn_074",
      "gnn_075",
      "gnn_076",
      "gnn_077",
      "gnn_078",
      "gnn_079",
      "gnn_080",
      "gnn_081",
      "gnn_082",
      "gnn_083",
      "gnn_084",
      "gnn_085",
      "gnn_086",
      "gnn_087",
      "gnn_088",
      "gnn_089",
      "gnn_090",
      "gnn_091",
      "gnn_092",
      "gnn_093",
      "gnn_094",
      "gnn_095",
      "gnn_096",
      "gnn_097",
      "gnn_098",
      "gnn_099",
      "gnn_100",
      "gnn_101",
      "gnn_102",
      "gnn_103",
      "gnn_104",
      "gnn_105",
      "gnn_106",
      "gnn_107",
      "gnn_108",
      "gnn_109",
      "gnn_110",
      "gnn_111",
      "gnn_112",
      "gnn_113",
      "gnn_114",
      "gnn_115",
      "gnn_116",
      "gnn_117",
      "gnn_118",
      "gnn_119",
      "gnn_120",
      "gnn_121",
      "gnn_122",
      "gnn_123",
      "gnn_124",
      "gnn_125",
      "gnn_126",
      "gnn_127",
      "gnn_available"
    ],
    "trials": [
      {
        "num_leaves": 15,
        "val_tuning_map": 0.020222546754652272
      },
      {
        "num_leaves": 31,
        "val_tuning_map": 0.01985744579465548
      }
    ],
    "best_num_leaves": 15,
    "train_pairs": 803377,
    "train_user_times": 50000,
    "rounds": 150,
    "checkpoint_sha256": "f5439416aeeb6f0f2dedab20aabb14ea541b4bd98b70f21334986dc03a05abc4",
    "inference_from_saved_model": true,
    "embedding_counts": {
      "train": {
        "user_times": 50000,
        "pairs": 803377,
        "missing_embeddings": 565051
      },
      "val": {
        "user_times": 74575,
        "pairs": 2088583,
        "missing_embeddings": 223414
      },
      "test": {
        "user_times": 67144,
        "pairs": 1892405,
        "missing_embeddings": 201178
      }
    },
    "protocol": "Adaptation of RelBench Appendix C.2 to H&M ranking; 128 frozen embeddings plus availability flag; same pairs/budget as manual tree; in-sample GNN train representations",
    "val_metrics": {
      "map": 0.019711562867923985
    },
    "val_inference_seconds": 7.192994180004462,
    "test_metrics": {
      "map": 0.021245096686483916
    },
    "test_inference_seconds": 6.244760037996457
  },
  "artifacts": "baseline/results/gnn_embeddings_v1"
}
```

## 2026-10-14T20:36:12+03:00 — embedding_report

Отчёт GNN → LightGBM сохранён отдельно; предыдущие результаты не заменены

Запуск: `hm_gnn_embedding_report_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/gnn_embeddings_v1"
}
```

## 2026-10-14T20:36:13+03:00 — embedding_pipeline_exit

Эксперимент GNN → LightGBM завершил работу с кодом 0

Запуск: `hm_gnn_embedding_pipeline_v1`.

```json
{
  "status": "complete"
}
```

## 2026-10-14T20:37:32+03:00 — embedding_final_verification

Метрики независимо пересчитаны из сохранённых предсказаний; shape, уникальность и диапазон ID, имена признаков сохранённого LightGBM и SHA весов GNN проверены. График проверен визуально.

Запуск: `hm_idgnn_lightgbm_embeddings_seed_42_v1`.

```json
{
  "status": "complete",
  "checks": {
    "val": {
      "shape": [
        74575,
        12
      ],
      "map": 0.019711562867923985,
      "passed": true
    },
    "test": {
      "shape": [
        67144,
        12
      ],
      "map": 0.021245096686483916,
      "passed": true
    }
  },
  "val_metrics": {
    "map": 0.019711562867923985
  },
  "test_metrics": {
    "map": 0.021245096686483916
  },
  "artifacts": "baseline/results/gnn_embeddings_v1"
}
```

## 2026-10-14T21:35:39+03:00 — gitignore_updated

Updated .gitignore: local environments, datasets, caches, upstream clones, runtime files and large binary artifacts excluded; metrics, manifests, reports and experiment history retained. Existing Git index unchanged.

## 2026-10-14T21:41:26+03:00 — artifact_restore_documented

Added root README with exact external snapshots, upstream commits, local checkpoint paths and SHA256, and explicit absence of a public trained-weight download. Preserved GloVe manifest in Git; added pinned restore_downloads.py. Verified sizes and SHA256 for all 18 dataset files and 8 GloVe files locally; no downloads or training performed.

## 2026-10-14T21:50:05+03:00 — two_tower_start

Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss

Запуск: `hm_twotower_sage_smoke_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 1,
    "eval_epochs_interval": 1,
    "batch_size": 32,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "gnn": "sage",
    "gat_heads": 4,
    "gat_dropout": 0.0,
    "temporal_strategy": "uniform",
    "share_same_time": true,
    "use_shallow": true,
    "max_steps_per_epoch": 1,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "RelBenchGNN/results/two_tower_smoke",
    "eval_batch_size": 32,
    "smoke": true,
    "resume": false,
    "inference_only": false
  },
  "artifacts": "RelBenchGNN/results/two_tower_smoke"
}
```

## 2026-10-14T21:50:47+03:00 — two_tower_protocol

Пользователь поручил двухбашенную модель: официальный shared-backbone GraphSAGE, отдельные forward пользователя/товара, dot product, BPR, shallow товары, full-catalog retrieval. Новый seed42 эксперимент: batch256, 20epochs, uniform, точно2000steps. Добавлены best/last checkpoint, независимый инференс, все user/item вектора, отдельные отчёты и прогресс100шагов. В smoke подготовке исправлены UTF-8 генератора и относительный путь output. Полный запуск пока ожидает smoke.

Запуск: `hm_twotower_pipeline_v1`.

```json
{
  "status": "smoke"
}
```

## 2026-10-14T21:51:10+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 1/1

Запуск: `hm_twotower_sage_smoke_v1`.

```json
{
  "status": "training",
  "current_epoch": 1
}
```

## 2026-10-14T21:51:31+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_smoke_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 1.5412867069244385,
  "val_metrics": {
    "map": 0.0
  },
  "elapsed_seconds": 83.8145649433136
}
```

## 2026-10-14T21:51:33+03:00 — two_tower_complete

Двухбашенная GNN: smoke forward/backward/eval пройден, метрики не сопоставимы с полным тестом

Запуск: `hm_twotower_sage_smoke_v1`.

```json
{
  "status": "smoke_complete",
  "epoch": 1,
  "val_metrics": {
    "map": 0.0
  },
  "test_metrics": {
    "map": 0.0
  },
  "artifacts": "RelBenchGNN/results/two_tower_smoke"
}
```

## 2026-10-14T21:52:13+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T21:52:38+03:00 — two_tower_start

Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss

Запуск: `hm_twotower_sage_smoke_v1_inference`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 1,
    "eval_epochs_interval": 1,
    "batch_size": 32,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "gnn": "sage",
    "gat_heads": 4,
    "gat_dropout": 0.0,
    "temporal_strategy": "uniform",
    "share_same_time": true,
    "use_shallow": true,
    "max_steps_per_epoch": 1,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "RelBenchGNN/results/two_tower_smoke",
    "eval_batch_size": 32,
    "smoke": true,
    "resume": false,
    "inference_only": true
  },
  "artifacts": "RelBenchGNN/results/two_tower_smoke"
}
```

## 2026-10-14T21:53:47+03:00 — two_tower_inference

Независимый инференс двухбашенной GNN проверен

Запуск: `hm_twotower_sage_smoke_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "passed": true,
    "checks": {
      "val": {
        "predictions_identical": true,
        "map_absolute_difference": 0.0,
        "passed": true
      },
      "test": {
        "predictions_identical": true,
        "map_absolute_difference": 0.0,
        "passed": true
      }
    },
    "checkpoint_sha256": "34fb5398ceecea2314cb29e7c2f7e36c6babcf400bcffe35137b531c5cdaae4d"
  },
  "artifacts": "RelBenchGNN/results/two_tower_smoke"
}
```

## 2026-10-14T21:54:44+03:00 — two_tower_start

Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 256,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "gnn": "sage",
    "gat_heads": 4,
    "gat_dropout": 0.0,
    "temporal_strategy": "uniform",
    "share_same_time": true,
    "use_shallow": true,
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/two_tower_seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true,
    "inference_only": false
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-14T21:54:44+03:00 — two_tower_launch

Двухбашенная модель создана; smoke BPR forward/backward/eval и независимая загрузка best.pt пройдены, предсказания val/test совпали полностью. Полный seed42 запуск 20эпох стартовал hidden WSL launcher PID1608, отдельный конвейер продолжит полный инференс и отчёт. Итоговых full метрик пока нет.

Запуск: `hm_twotower_pipeline_v1`.

```json
{
  "status": "preparing"
}
```

## 2026-10-14T21:55:38+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 1/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 1
}
```

## 2026-10-14T21:56:32+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T21:56:57+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T21:57:20+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T21:57:41+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T21:58:02+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T21:58:23+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T21:58:45+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T21:59:07+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T21:59:28+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T21:59:52+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:00:13+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:00:35+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:00:55+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:01:17+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:01:41+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:02:05+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:02:11+03:00 — hypothesis_added

По просьбе пользователя создан HYPOTHESES.md: H001, двухбашенная GNN с независимыми весами пользовательского и товарного энкодеров. Зафиксированы гипотеза, контроль shared-backbone, будущий уникальный run_id, протокол MAP@12, сохранение артефактов и ограничения числа параметров/одного seed. Эксперимент не запущен; текущий запуск не изменён.

## 2026-10-14T22:02:30+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:02:55+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:03:18+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:03:44+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:04:40+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.11198035415634514,
  "val_metrics": {
    "map": 0.0057429049364308045
  },
  "elapsed_seconds": 594.8764209747314
}
```

## 2026-10-14T22:04:43+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:04:43+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 2/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 2
}
```

## 2026-10-14T22:05:04+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:05:23+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:05:44+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:06:05+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:06:29+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:06:52+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:07:17+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:07:41+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:08:02+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:08:25+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:08:47+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:09:08+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:09:29+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:09:52+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:10:13+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:10:35+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:10:57+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:11:19+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:11:40+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:12:02+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:12:55+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.09265107665024698,
  "val_metrics": {
    "map": 0.0047890965412890505
  },
  "elapsed_seconds": 1089.5350096225739
}
```

## 2026-10-14T22:12:57+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:12:57+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 3/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 3
}
```

## 2026-10-14T22:13:21+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:13:42+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:14:03+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:14:24+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:14:46+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:15:07+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:15:29+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:15:51+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:16:13+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:16:35+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:16:57+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:17:19+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:17:40+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:18:02+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:18:24+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:18:46+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:19:08+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:19:30+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:19:53+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:20:17+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:21:24+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.07268015710450709,
  "val_metrics": {
    "map": 0.0038984466117935644
  },
  "elapsed_seconds": 1598.6979293823242
}
```

## 2026-10-14T22:21:27+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:21:27+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 4/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 4
}
```

## 2026-10-14T22:21:55+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:22:20+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:22:45+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:23:12+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:23:41+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:24:01+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:24:21+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:24:43+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:25:02+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:25:24+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:25:44+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:26:04+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:26:24+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:26:44+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:27:04+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:27:24+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:27:44+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:28:04+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:28:23+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:28:42+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:29:29+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.0543516638786532,
  "val_metrics": {
    "map": 0.0024878573952055645
  },
  "elapsed_seconds": 2083.9084668159485
}
```

## 2026-10-14T22:29:31+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:29:31+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 5/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 5
}
```

## 2026-10-14T22:29:50+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:30:09+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:30:29+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:30:48+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:31:07+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:31:25+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:31:45+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:32:04+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:32:22+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:32:42+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:33:01+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:33:20+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:33:38+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:33:57+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:34:20+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:34:39+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:34:59+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:35:19+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:35:37+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:35:56+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:36:43+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 0.03622457931935787,
  "val_metrics": {
    "map": 0.0019701034929627908
  },
  "elapsed_seconds": 2518.2518815994263
}
```

## 2026-10-14T22:36:45+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:36:45+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 6/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 6
}
```

## 2026-10-14T22:37:04+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:37:23+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:37:42+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:38:01+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:38:20+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:38:39+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:38:58+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:39:18+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:39:36+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:39:55+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:40:14+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:40:33+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:40:52+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:41:11+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:41:30+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:41:49+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:42:08+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:42:27+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:42:45+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:43:05+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:43:50+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 0.02299862293736078,
  "val_metrics": {
    "map": 0.0015408236748669475
  },
  "elapsed_seconds": 2945.203561067581
}
```

## 2026-10-14T22:43:52+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:43:52+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 7/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 7
}
```

## 2026-10-14T22:44:11+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:44:30+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:44:50+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:45:10+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:45:30+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:45:50+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:46:11+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:46:31+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:46:52+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:47:12+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:47:33+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:47:55+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:48:15+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:48:37+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:48:59+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:49:20+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:49:42+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:50:04+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:50:25+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:50:47+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T22:51:45+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 0.01606847740197554,
  "val_metrics": {
    "map": 0.0010109718962401841
  },
  "elapsed_seconds": 3419.8694157600403
}
```

## 2026-10-14T22:51:47+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T22:51:47+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 8/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 8
}
```

## 2026-10-14T22:52:06+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T22:52:27+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T22:52:48+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T22:53:08+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T22:53:35+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T22:53:56+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T22:54:17+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T22:54:39+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T22:55:01+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T22:55:22+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T22:55:44+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T22:56:06+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T22:56:27+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T22:56:49+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T22:57:11+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T22:57:33+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T22:57:55+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T22:58:18+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T22:58:40+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T22:59:02+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:00:00+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 8,
  "train_loss": 0.012174643606180325,
  "val_metrics": {
    "map": 0.0009382148177132164
  },
  "elapsed_seconds": 3914.6995565891266
}
```

## 2026-10-14T23:00:02+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:00:02+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 9/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 9
}
```

## 2026-10-14T23:00:22+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:00:42+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:01:03+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:01:22+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:01:42+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:02:01+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:02:20+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:02:40+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:02:58+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:03:18+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:03:37+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:03:57+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:04:16+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:04:34+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:04:54+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:05:13+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:05:32+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:05:51+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:06:10+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:06:29+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:07:19+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 9,
  "train_loss": 0.010294270628248342,
  "val_metrics": {
    "map": 0.0009771209003905323
  },
  "elapsed_seconds": 4354.4426918029785
}
```

## 2026-10-14T23:07:21+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:07:21+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 10/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 10
}
```

## 2026-10-14T23:07:41+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:07:59+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:08:19+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:08:42+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:09:01+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:09:20+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:09:39+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:09:58+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:10:17+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:10:36+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:10:55+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:11:14+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:11:33+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:11:52+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:12:12+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:12:32+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:12:51+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:13:12+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:13:31+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:13:52+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:14:46+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 10,
  "train_loss": 0.009191992744861637,
  "val_metrics": {
    "map": 0.0009025397228235678
  },
  "elapsed_seconds": 4801.507330417633
}
```

## 2026-10-14T23:14:48+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:14:48+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 11/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 11
}
```

## 2026-10-14T23:15:08+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:15:28+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:15:49+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:16:09+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:16:29+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:16:50+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:17:11+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:17:32+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:17:53+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:18:14+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:18:36+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:18:57+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:19:18+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:19:40+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:20:01+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:20:23+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:20:45+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:21:06+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:21:28+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:21:49+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:22:47+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 11,
  "train_loss": 0.007495485727093182,
  "val_metrics": {
    "map": 0.001086409799752254
  },
  "elapsed_seconds": 5281.9778525829315
}
```

## 2026-10-14T23:22:50+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:22:50+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 12/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 12
}
```

## 2026-10-14T23:23:09+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:23:30+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:23:54+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:24:16+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:24:37+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:24:59+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:25:20+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:25:41+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:26:02+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:26:24+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:26:46+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:27:08+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:27:28+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:27:50+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:28:12+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:28:34+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:28:56+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:29:19+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:29:40+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:30:02+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:30:54+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 12,
  "train_loss": 0.00609492240997497,
  "val_metrics": {
    "map": 0.0012828753988669195
  },
  "elapsed_seconds": 5769.1190140247345
}
```

## 2026-10-14T23:30:56+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:30:56+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 13/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 13
}
```

## 2026-10-14T23:31:15+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:31:35+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:31:55+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:32:15+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:32:34+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:32:54+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:33:13+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:33:32+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:33:51+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:34:10+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:34:29+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:34:49+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:35:07+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:35:26+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:35:45+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:36:04+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:36:24+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:36:43+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:37:01+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:37:20+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:38:12+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 13,
  "train_loss": 0.00543211716474616,
  "val_metrics": {
    "map": 0.0017266225355550432
  },
  "elapsed_seconds": 6206.97042298317
}
```

## 2026-10-14T23:38:13+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:38:13+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 14/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 14
}
```

## 2026-10-14T23:38:32+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:38:54+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:39:13+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:39:32+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:39:51+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:40:11+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:40:30+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:40:49+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:41:08+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:41:27+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:41:45+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:42:04+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:42:23+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:42:42+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:43:01+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:43:20+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:43:39+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:43:58+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:44:17+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:44:35+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:45:25+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 14,
  "train_loss": 0.005087600154598477,
  "val_metrics": {
    "map": 0.0009725269851546385
  },
  "elapsed_seconds": 6640.748001813889
}
```

## 2026-10-14T23:45:27+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:45:27+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 15/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 15
}
```

## 2026-10-14T23:45:46+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:46:05+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:46:23+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:46:42+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:47:01+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:47:20+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:47:39+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:47:59+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:48:18+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:48:38+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:48:58+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:49:18+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:49:37+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:49:58+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:50:18+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:50:39+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:50:59+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:51:21+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:51:41+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-14T23:52:02+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-14T23:52:58+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 15,
  "train_loss": 0.004692768007866107,
  "val_metrics": {
    "map": 0.0017061930475183497
  },
  "elapsed_seconds": 7093.362394332886
}
```

## 2026-10-14T23:53:00+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-14T23:53:00+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 16/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 16
}
```

## 2026-10-14T23:53:20+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-14T23:53:40+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-14T23:54:04+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-14T23:54:24+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-14T23:54:46+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-14T23:55:06+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-14T23:55:27+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-14T23:55:49+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-14T23:56:09+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-14T23:56:31+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-14T23:56:52+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-14T23:57:14+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-14T23:57:34+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-14T23:57:56+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-14T23:58:17+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-14T23:58:39+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-14T23:59:02+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-14T23:59:23+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-14T23:59:45+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-15T00:00:07+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-15T00:01:04+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 16,
  "train_loss": 0.00424751581120654,
  "val_metrics": {
    "map": 0.002262501987712379
  },
  "elapsed_seconds": 7579.551252365112
}
```

## 2026-10-15T00:01:06+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:01:07+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 17/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 17
}
```

## 2026-10-15T00:01:27+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-15T00:01:47+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-15T00:02:07+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-15T00:02:28+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-15T00:02:50+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-15T00:03:10+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-15T00:03:32+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-15T00:03:55+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-15T00:04:15+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-15T00:04:37+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-15T00:04:58+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-15T00:05:20+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-15T00:05:41+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-15T00:06:02+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-15T00:06:24+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-15T00:06:46+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-15T00:07:08+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-15T00:07:30+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-15T00:07:52+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-15T00:08:14+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-15T00:09:11+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 17,
  "train_loss": 0.003934520246064494,
  "val_metrics": {
    "map": 0.0011031379828122698
  },
  "elapsed_seconds": 8066.598598003387
}
```

## 2026-10-15T00:09:13+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:09:13+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 18/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 18
}
```

## 2026-10-15T00:09:33+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-15T00:09:52+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-15T00:10:13+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-15T00:10:33+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-15T00:10:53+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-15T00:11:14+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-15T00:11:34+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-15T00:11:47+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:11:48+03:00 — learning_curves_added

По просьбе пользователя добавлены PNG/SVG и CSV кривых обучения двухбашенной GNN: средний BPR loss и полный validation MAP@12 по завершённым эпохам. График встроен в reports/two_tower_v1/report.md и автоматически обновляется после каждой эпохи. Генерация отчёта защищена flock от конкурентных запусков.

## 2026-10-15T00:11:58+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-15T00:12:18+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-15T00:12:37+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-15T00:12:56+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-15T00:13:17+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-15T00:13:36+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-15T00:13:56+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-15T00:14:16+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-15T00:14:37+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-15T00:14:57+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-15T00:15:18+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-15T00:15:38+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-15T00:15:57+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-15T00:16:49+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 18,
  "train_loss": 0.003412049475889944,
  "val_metrics": {
    "map": 0.0013787295704988751
  },
  "elapsed_seconds": 8523.813731908798
}
```

## 2026-10-15T00:16:51+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:16:51+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 19/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 19
}
```

## 2026-10-15T00:17:11+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-15T00:17:31+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-15T00:17:51+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-15T00:18:09+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-15T00:18:29+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-15T00:18:49+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-15T00:19:09+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-15T00:19:30+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-15T00:19:50+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-15T00:20:09+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-15T00:20:29+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-15T00:20:49+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-15T00:21:10+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-15T00:21:30+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-15T00:21:52+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-15T00:22:13+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-15T00:22:35+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-15T00:22:55+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-15T00:23:14+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-15T00:23:34+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-15T00:24:25+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 19,
  "train_loss": 0.0029281466680113224,
  "val_metrics": {
    "map": 0.0021894386571767272
  },
  "elapsed_seconds": 8980.677268743515
}
```

## 2026-10-15T00:24:28+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:24:28+03:00 — two_tower_epoch_start

Обучение двухбашенной GNN: эпоха 20/20

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "current_epoch": 20
}
```

## 2026-10-15T00:24:47+03:00 — two_tower_progress

Двухбашенная GNN: 100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 100
}
```

## 2026-10-15T00:25:05+03:00 — two_tower_progress

Двухбашенная GNN: 200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 200
}
```

## 2026-10-15T00:25:26+03:00 — two_tower_progress

Двухбашенная GNN: 300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 300
}
```

## 2026-10-15T00:25:45+03:00 — two_tower_progress

Двухбашенная GNN: 400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 400
}
```

## 2026-10-15T00:26:05+03:00 — two_tower_progress

Двухбашенная GNN: 500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 500
}
```

## 2026-10-15T00:26:25+03:00 — two_tower_progress

Двухбашенная GNN: 600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 600
}
```

## 2026-10-15T00:26:45+03:00 — two_tower_progress

Двухбашенная GNN: 700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 700
}
```

## 2026-10-15T00:27:04+03:00 — two_tower_progress

Двухбашенная GNN: 800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 800
}
```

## 2026-10-15T00:27:23+03:00 — two_tower_progress

Двухбашенная GNN: 900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 900
}
```

## 2026-10-15T00:27:43+03:00 — two_tower_progress

Двухбашенная GNN: 1000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1000
}
```

## 2026-10-15T00:28:02+03:00 — two_tower_progress

Двухбашенная GNN: 1100/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1100
}
```

## 2026-10-15T00:28:22+03:00 — two_tower_progress

Двухбашенная GNN: 1200/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1200
}
```

## 2026-10-15T00:28:41+03:00 — two_tower_progress

Двухбашенная GNN: 1300/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1300
}
```

## 2026-10-15T00:29:00+03:00 — two_tower_progress

Двухбашенная GNN: 1400/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1400
}
```

## 2026-10-15T00:29:19+03:00 — two_tower_progress

Двухбашенная GNN: 1500/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1500
}
```

## 2026-10-15T00:29:38+03:00 — two_tower_progress

Двухбашенная GNN: 1600/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1600
}
```

## 2026-10-15T00:29:58+03:00 — two_tower_progress

Двухбашенная GNN: 1700/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1700
}
```

## 2026-10-15T00:30:18+03:00 — two_tower_progress

Двухбашенная GNN: 1800/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1800
}
```

## 2026-10-15T00:30:36+03:00 — two_tower_progress

Двухбашенная GNN: 1900/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 1900
}
```

## 2026-10-15T00:30:56+03:00 — two_tower_progress

Двухбашенная GNN: 2000/2000 шагов текущей эпохи

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "train_step": 2000
}
```

## 2026-10-15T00:31:48+03:00 — two_tower_epoch

Завершена эпоха двухбашенной GNN

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 20,
  "train_loss": 0.0027485086652086466,
  "val_metrics": {
    "map": 0.0009148587620313039
  },
  "elapsed_seconds": 9422.936126470566
}
```

## 2026-10-15T00:31:51+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "partial",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T00:33:29+03:00 — two_tower_complete

Двухбашенная GNN завершила обучение и полную оценку

Запуск: `hm_twotower_sage_seed_42_v1`.

```json
{
  "status": "complete",
  "epoch": 20,
  "val_metrics": {
    "map": 0.005743128425088755
  },
  "test_metrics": {
    "map": 0.005430130288149388
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-15T00:34:32+03:00 — two_tower_start

Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss

Запуск: `hm_twotower_sage_seed_42_v1_inference`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 256,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "gnn": "sage",
    "gat_heads": 4,
    "gat_dropout": 0.0,
    "temporal_strategy": "uniform",
    "share_same_time": true,
    "use_shallow": true,
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/two_tower_seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true,
    "inference_only": true
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-15T00:38:41+03:00 — two_tower_inference

Независимый инференс двухбашенной GNN проверен

Запуск: `hm_twotower_sage_seed_42_v1_inference`.

```json
{
  "status": "failed",
  "checks": {
    "passed": false,
    "checks": {
      "val": {
        "predictions_identical": false,
        "map_absolute_difference": 0.0,
        "passed": false
      },
      "test": {
        "predictions_identical": false,
        "map_absolute_difference": 0.0,
        "passed": false
      }
    },
    "checkpoint_sha256": "8541fc534edb0ed2d930789a8075b200474f344df38b161e2d1759be762c53c5"
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-15T00:38:41+03:00 — two_tower_error

Ошибка двухбашенного запуска

Запуск: `hm_twotower_sage_seed_42_v1_inference`.

```json
{
  "status": "failed",
  "error": "Two-tower inference mismatch"
}
```

## 2026-10-15T10:45:00+03:00 — two_tower_resume

После остановки пользователем активных процессов нет. Обнаружен завершённый независимый инференс с точным совпадением MAP, но strict проверка отклонила разные ID. Векторы отличаются максимум на 4.77e-7. Добавлена отдельная проверка numerical_ties_v2: близость всех векторов, оценок рекомендаций по рангам, shape/ID/уникальности и MAP; точное совпадение ID фиксируется отдельно. Старые strict-check и лог сохранены. Возобновляется только инференс, обучение не повторяется.

Запуск: `hm_twotower_pipeline_v1`.

```json
{
  "status": "resuming"
}
```

## 2026-10-15T10:45:58+03:00 — two_tower_start

Начат двухбашенный GraphSAGE: отдельные forward пользователя и товара, общие веса, BPR loss

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm",
    "task": "user-item-purchase",
    "lr": 0.001,
    "epochs": 20,
    "eval_epochs_interval": 1,
    "batch_size": 256,
    "channels": 128,
    "aggr": "sum",
    "num_layers": 2,
    "num_neighbors": 128,
    "gnn": "sage",
    "gat_heads": 4,
    "gat_dropout": 0.0,
    "temporal_strategy": "uniform",
    "share_same_time": true,
    "use_shallow": true,
    "max_steps_per_epoch": 2000,
    "num_workers": 0,
    "seed": 42,
    "cache_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/cache",
    "pred_dir": "/tmp/relbench_preds",
    "output_dir": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/RelBenchGNN/results/two_tower_seed_42",
    "eval_batch_size": 128,
    "smoke": false,
    "resume": true,
    "inference_only": true
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-15T10:47:17+03:00 — two_tower_encoding

Кодирование val/article: 100/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 100,
  "total_batches": 825
}
```

## 2026-10-15T10:47:20+03:00 — two_tower_encoding

Кодирование val/article: 200/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 200,
  "total_batches": 825
}
```

## 2026-10-15T10:47:23+03:00 — two_tower_encoding

Кодирование val/article: 300/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 300,
  "total_batches": 825
}
```

## 2026-10-15T10:47:26+03:00 — two_tower_encoding

Кодирование val/article: 400/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 400,
  "total_batches": 825
}
```

## 2026-10-15T10:47:31+03:00 — two_tower_encoding

Кодирование val/article: 500/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 500,
  "total_batches": 825
}
```

## 2026-10-15T10:47:35+03:00 — two_tower_encoding

Кодирование val/article: 600/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 600,
  "total_batches": 825
}
```

## 2026-10-15T10:47:39+03:00 — two_tower_encoding

Кодирование val/article: 700/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 700,
  "total_batches": 825
}
```

## 2026-10-15T10:47:43+03:00 — two_tower_encoding

Кодирование val/article: 800/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "article",
  "batches": 800,
  "total_batches": 825
}
```

## 2026-10-15T10:47:49+03:00 — two_tower_encoding

Кодирование val/customer: 100/583 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "customer",
  "batches": 100,
  "total_batches": 583
}
```

## 2026-10-15T10:47:53+03:00 — two_tower_encoding

Кодирование val/customer: 200/583 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "customer",
  "batches": 200,
  "total_batches": 583
}
```

## 2026-10-15T10:47:57+03:00 — two_tower_encoding

Кодирование val/customer: 300/583 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "customer",
  "batches": 300,
  "total_batches": 583
}
```

## 2026-10-15T10:48:04+03:00 — two_tower_encoding

Кодирование val/customer: 400/583 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "customer",
  "batches": 400,
  "total_batches": 583
}
```

## 2026-10-15T10:48:08+03:00 — two_tower_encoding

Кодирование val/customer: 500/583 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "val",
  "node_type": "customer",
  "batches": 500,
  "total_batches": 583
}
```

## 2026-10-15T10:48:21+03:00 — two_tower_encoding

Кодирование test/article: 100/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 100,
  "total_batches": 825
}
```

## 2026-10-15T10:48:23+03:00 — two_tower_encoding

Кодирование test/article: 200/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 200,
  "total_batches": 825
}
```

## 2026-10-15T10:48:24+03:00 — two_tower_encoding

Кодирование test/article: 300/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 300,
  "total_batches": 825
}
```

## 2026-10-15T10:48:26+03:00 — two_tower_encoding

Кодирование test/article: 400/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 400,
  "total_batches": 825
}
```

## 2026-10-15T10:48:28+03:00 — two_tower_encoding

Кодирование test/article: 500/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 500,
  "total_batches": 825
}
```

## 2026-10-15T10:48:30+03:00 — two_tower_encoding

Кодирование test/article: 600/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 600,
  "total_batches": 825
}
```

## 2026-10-15T10:48:33+03:00 — two_tower_encoding

Кодирование test/article: 700/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 700,
  "total_batches": 825
}
```

## 2026-10-15T10:48:39+03:00 — two_tower_encoding

Кодирование test/article: 800/825 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "article",
  "batches": 800,
  "total_batches": 825
}
```

## 2026-10-15T10:48:42+03:00 — two_tower_encoding

Кодирование test/customer: 100/525 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "customer",
  "batches": 100,
  "total_batches": 525
}
```

## 2026-10-15T10:48:45+03:00 — two_tower_encoding

Кодирование test/customer: 200/525 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "customer",
  "batches": 200,
  "total_batches": 525
}
```

## 2026-10-15T10:48:49+03:00 — two_tower_encoding

Кодирование test/customer: 300/525 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "customer",
  "batches": 300,
  "total_batches": 525
}
```

## 2026-10-15T10:48:52+03:00 — two_tower_encoding

Кодирование test/customer: 400/525 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "customer",
  "batches": 400,
  "total_batches": 525
}
```

## 2026-10-15T10:48:55+03:00 — two_tower_encoding

Кодирование test/customer: 500/525 batches

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "inference",
  "split": "test",
  "node_type": "customer",
  "batches": 500,
  "total_batches": 525
}
```

## 2026-10-15T10:49:01+03:00 — two_tower_inference

Независимый инференс двухбашенной GNN проверен; сравниваются векторы, оценки по рангам и MAP с допуском для численных ties

Запуск: `hm_twotower_sage_seed_42_v1_inference_v2`.

```json
{
  "status": "verified",
  "checks": {
    "passed": true,
    "checks": {
      "val": {
        "verification_protocol": "numerical_ties_v2",
        "shape_ok": true,
        "unique_ids": true,
        "ids_valid": true,
        "predictions_identical": false,
        "same_item_at_same_rank_fraction": 0.9999687115878869,
        "embeddings_close": true,
        "embedding_atol": 1e-06,
        "embedding_rtol": 1e-06,
        "max_embedding_absolute_difference": 4.76837158203125e-07,
        "ranked_scores_close": true,
        "score_atol": 1e-05,
        "score_rtol": 1e-06,
        "max_ranked_score_absolute_difference": 9.613452567336367e-06,
        "map_absolute_difference": 0.0,
        "map_tolerance": 1e-06,
        "passed": true
      },
      "test": {
        "verification_protocol": "numerical_ties_v2",
        "shape_ok": true,
        "unique_ids": true,
        "ids_valid": true,
        "predictions_identical": false,
        "same_item_at_same_rank_fraction": 0.9999677310457127,
        "embeddings_close": true,
        "embedding_atol": 1e-06,
        "embedding_rtol": 1e-06,
        "max_embedding_absolute_difference": 4.76837158203125e-07,
        "ranked_scores_close": true,
        "score_atol": 1e-05,
        "score_rtol": 1e-06,
        "max_ranked_score_absolute_difference": 4.566560530605557e-06,
        "map_absolute_difference": 0.0,
        "map_tolerance": 1e-06,
        "passed": true
      }
    },
    "checkpoint_sha256": "8541fc534edb0ed2d930789a8075b200474f344df38b161e2d1759be762c53c5",
    "inference_seconds": 117.29978087999996,
    "verification_protocol": "numerical_ties_v2"
  },
  "artifacts": "RelBenchGNN/results/two_tower_seed_42"
}
```

## 2026-10-15T10:49:09+03:00 — two_tower_report

Обновлён отдельный отчёт двухбашенной модели

Запуск: `hm_twotower_report_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/two_tower_v1"
}
```

## 2026-10-15T10:49:10+03:00 — two_tower_pipeline_exit

Двухбашенный конвейер завершён с кодом 0

Запуск: `hm_twotower_pipeline_v1`.

```json
{
  "status": "complete"
}
```

## 2026-10-15T10:56:50+03:00 — two_tower_final_audit

Повторный запрос восстановления: проверено, что возобновлённый конвейер уже завершился в 10:49 МСК с exitcode=0; inference_check passed=true, report final=true, активных процессов нет. Повторный запуск не создавался. Итоговый test MAP@12 0.54301%; CONTEXT.md обновлён.
