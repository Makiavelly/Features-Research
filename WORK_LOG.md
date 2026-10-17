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

## 2026-10-15T11:05:13+03:00 — project_review

Reviewed project context, experiment history, model and tree code, saved reports and inference checks before discussing the next experiment. WSL process audit found no active experiment processes. No training started. Open questions: research priority, next hypothesis, candidate protocol, compute budget, and success criteria.

## 2026-10-15T11:12:28+03:00 — research_direction

User selected a new direction: feature construction by a local LLM, evaluated separately from manual and GNN features. Evaluate recommendations over the full catalog, seed 42, no time budget limit; primary success criterion is higher MAP@12. Detailed idea will follow in the next user message. No implementation or training started. Independent-tower hypothesis deferred; previous results preserved.

## 2026-10-15T11:23:14+03:00 — llmfe_literature_review

Reviewed arXiv 2503.14434v3 and official nikhilsab/LLMFE source: main, sampler, evaluator, buffer, config, and balance-scale specification. Method searches feature-transformation programs using downstream validation and multi-island memory; local HTTP LLM supported. H&M temporal ranking/full-catalog MAP requires adaptation, not direct use of random CV. Noted differences between paper and code defaults and unenforced sandbox timeout in examined implementation. Context updated; no dependencies installed or experiment launched.

## 2026-10-15T11:39:02+03:00 — scoring_protocol_clarification

User requires valid scoring comparison against ID-GNN. Source audit: ID-GNN constructs full-catalog zero scores and fills sigmoid scores for sampled items; saved pool contains sampled items plus top-k zero-score fillers. Keep full-catalog end-to-end evaluation with identical users, targets, cutoffs, and MAP@12 evaluator; additionally use identical saved ID-GNN pools for both models to isolate reranking. Report protocols separately, preserve native ID-GNN behavior and old results. No experiment launched.

## 2026-10-15T11:43:32+03:00 — llm_model_options

User prefers local hardware first and permits a later Kaggle experiment using the study model if local results are poor. GPU confirmed RTX 3060 Laptop 6144 MiB, driver 528.02. Recommended, not selected or tested: Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M (4.68 GB file), llama.cpp, 4096-token initial context, sequential generations, optional CPU layer offload. Compact alternative Qwen3-4B-Instruct-2507 Q4_K_M; study comparison Llama-3.1-8B-Instruct on Kaggle subject to available GPU. No downloads, installs, or experiment launches.

## 2026-10-15T11:48:43+03:00 — llmfe_model_setup

Загрузка Qwen2.5-Coder-7B-Instruct Q4_K_M в отдельное хранилище проекта

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "setup"
}
```

## 2026-10-15T11:58:46+03:00 — llmfe_protocol_ready

LLM-FE implementation and background pipeline prepared. Three tests passed: temporal cutoff/future invariance, label/ID isolation, exact full-catalog top-k including ties. Reused exactly 803377 supervised pairs / 50000 user-times (selection seed2026); no old feature columns read. Qwen GGUF downloaded and verified; initial loading underway. Search/confirmation/test protocols documented in LLMFeatures/README.md; no final metrics yet.

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "setup"
}
```

## 2026-10-15T11:59:32+03:00 — llmfe_model_ready

Локальная Qwen загрузилась и выполнила тестовую генерацию

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "preparing",
  "model": {
    "name": "qwen2.5-coder:7b-instruct-q4_K_M",
    "model": "qwen2.5-coder:7b-instruct-q4_K_M",
    "modified_at": "2026-10-15T11:57:18.3867895+03:00",
    "size": 4683087561,
    "digest": "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364",
    "details": {
      "parent_model": "",
      "format": "gguf",
      "family": "qwen2",
      "families": [
        "qwen2"
      ],
      "parameter_size": "7.6B",
      "quantization_level": "Q4_K_M"
    }
  },
  "runtime": {
    "models": [
      {
        "name": "qwen2.5-coder:7b-instruct-q4_K_M",
        "model": "qwen2.5-coder:7b-instruct-q4_K_M",
        "size": 4924207104,
        "digest": "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364",
        "details": {
          "parent_model": "",
          "format": "gguf",
          "family": "qwen2",
          "families": [
            "qwen2"
          ],
          "parameter_size": "7.6B",
          "quantization_level": "Q4_K_M"
        },
        "expires_at": "2026-10-15T12:29:31.992758199+03:00",
        "size_vram": 4924207104,
        "context_length": 4096
      }
    ]
  }
}
```

## 2026-10-15T11:59:52+03:00 — llmfe_start

Начат поиск LLM-признаков Qwen2.5-Coder-7B с полным каталогом

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "preparing",
  "config": {
    "schema_version": 1,
    "run_id": "hm_llmfe_qwen25coder7b_seed42_v1",
    "seed": 42,
    "llm": "qwen2.5-coder:7b-instruct-q4_K_M",
    "backend": "Ollama 0.21.0 (llama.cpp runner)",
    "quantization": "Q4_K_M",
    "context_tokens": 4096,
    "generation_tokens": 1800,
    "temperature": 0.8,
    "islands": 3,
    "llm_samples": 20,
    "memory_programs_per_prompt": 1,
    "train_user_times": 50000,
    "negative_sampling": "same saved pairs as manual_v1; only IDs/time/labels reused",
    "pair_selection_seed": 2026,
    "search_validation_users": 256,
    "confirmation_validation_users": 1024,
    "confirmation_candidates": 3,
    "search_objective": "full-catalog MAP@12",
    "final": "all validation and test users; full catalog and saved ID-GNN pools",
    "downstream": "LightGBM binary, 31 leaves, 150 rounds, same fixed settings for every program",
    "inputs": "raw static fields plus LLM SQL aggregates/derived features; no manual/GNN features",
    "feature_program": "restricted SQL expression AST-equivalent interface, not arbitrary Python",
    "cutoff": "t_dat <= prediction timestamp",
    "search_timeout_seconds": 21600,
    "final_timeout_seconds": 604800,
    "training_embeddings": false,
    "paper_deviations": [
      "temporal relational ranking, MAP@12, LightGBM",
      "SQL expression programs and controlled host joins instead of Python",
      "one prior program per prompt, 3 islands, 20 LLM proposals",
      "256 search users, disjoint 1024 confirmation users; complete catalog",
      "50k user-times, fixed seed42, no ensemble"
    ]
  },
  "artifacts": "LLMFeatures/results/qwen25coder7b_seed42_v1"
}
```

## 2026-10-15T12:00:32+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:00:57+03:00 — llmfe_generating

Локальная LLM предлагает программу 1/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "generating",
  "candidate": 1
}
```

## 2026-10-15T12:05:12+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:05:12+03:00 — llmfe_control

Контроль сырых признаков оценён на search validation по всему каталогу

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "searching",
  "raw_search_val_metrics": {
    "map": 0.001095920138888889
  }
}
```

## 2026-10-15T12:05:12+03:00 — llmfe_trial

LLM-FE программа 1/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "searching",
  "completed_proposals": 1,
  "trial": {
    "candidate": 1,
    "island": 0,
    "status": "rejected",
    "error": "Identifiers/statement keywords outside the feature interface",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v1/candidates/candidate_01"
  }
}
```

## 2026-10-15T12:05:12+03:00 — llmfe_generating

Локальная LLM предлагает программу 2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "generating",
  "candidate": 2
}
```

## 2026-10-15T12:05:27+03:00 — llmfe_trial

LLM-FE программа 2/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "searching",
  "completed_proposals": 2,
  "trial": {
    "candidate": 2,
    "island": 1,
    "status": "rejected",
    "error": "Identifiers/statement keywords outside the feature interface",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v1/candidates/candidate_02"
  }
}
```

## 2026-10-15T12:05:27+03:00 — llmfe_generating

Локальная LLM предлагает программу 3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "generating",
  "candidate": 3
}
```

## 2026-10-15T12:05:37+03:00 — llmfe_trial

LLM-FE программа 3/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "searching",
  "completed_proposals": 3,
  "trial": {
    "candidate": 3,
    "island": 2,
    "status": "rejected",
    "error": "Identifiers/statement keywords outside the feature interface",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v1/candidates/candidate_03"
  }
}
```

## 2026-10-15T12:05:37+03:00 — llmfe_generating

Локальная LLM предлагает программу 4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "generating",
  "candidate": 4
}
```

## 2026-10-15T12:05:46+03:00 — llmfe_trial

LLM-FE программа 4/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "searching",
  "completed_proposals": 4,
  "trial": {
    "candidate": 4,
    "island": 0,
    "status": "rejected",
    "error": "Identifiers/statement keywords outside the feature interface",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v1/candidates/candidate_04"
  }
}
```

## 2026-10-15T12:05:46+03:00 — llmfe_generating

Локальная LLM предлагает программу 5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "generating",
  "candidate": 5
}
```

## 2026-10-15T12:08:32+03:00 — llmfe_interface_superseded

v1 stopped and preserved: initial host interface incorrectly rejected valid unique-ID counts and global article-category aggregation. No valid LLM feature quality result obtained. Raw control full-catalog search MAP=0.001095920138888889 on 256 validation users; unchanged control may be reused in v2. Source/proposals saved under v1; new interface/prompt gets a new run_id v2.

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "superseded"
}
```

## 2026-10-15T12:08:44+03:00 — llmfe_start

Начат поиск LLM-признаков Qwen2.5-Coder-7B с полным каталогом

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "preparing",
  "config": {
    "schema_version": 1,
    "run_id": "hm_llmfe_qwen25coder7b_seed42_v2",
    "seed": 42,
    "llm": "qwen2.5-coder:7b-instruct-q4_K_M",
    "backend": "Ollama 0.21.0 (llama.cpp runner)",
    "quantization": "Q4_K_M",
    "context_tokens": 4096,
    "generation_tokens": 1800,
    "temperature": 0.8,
    "islands": 3,
    "llm_samples": 20,
    "memory_programs_per_prompt": 1,
    "train_user_times": 50000,
    "negative_sampling": "same saved pairs as manual_v1; only IDs/time/labels reused",
    "pair_selection_seed": 2026,
    "search_validation_users": 256,
    "confirmation_validation_users": 1024,
    "confirmation_candidates": 3,
    "search_objective": "full-catalog MAP@12",
    "final": "all validation and test users; full catalog and saved ID-GNN pools",
    "downstream": "LightGBM binary, 31 leaves, 150 rounds, same fixed settings for every program",
    "inputs": "raw static fields plus LLM SQL aggregates/derived features; no manual/GNN features",
    "feature_program": "v2 SQL expressions; global item/category and user/category groups; ID counts allowed, ID values excluded",
    "cutoff": "t_dat <= prediction timestamp",
    "search_timeout_seconds": 21600,
    "final_timeout_seconds": 604800,
    "training_embeddings": false,
    "paper_deviations": [
      "temporal relational ranking, MAP@12, LightGBM",
      "SQL expression programs and controlled host joins instead of Python",
      "one prior program per prompt, 3 islands, 20 LLM proposals",
      "256 search users, disjoint 1024 confirmation users; complete catalog",
      "50k user-times, fixed seed42, no ensemble"
    ]
  },
  "artifacts": "LLMFeatures/results/qwen25coder7b_seed42_v2"
}
```

## 2026-10-15T12:08:45+03:00 — llmfe_control

Контроль сырых признаков оценён на search validation по всему каталогу

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "raw_search_val_metrics": {
    "map": 0.001095920138888889
  }
}
```

## 2026-10-15T12:08:45+03:00 — llmfe_generating

Локальная LLM предлагает программу 1/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 1
}
```

## 2026-10-15T12:09:03+03:00 — llmfe_trial

LLM-FE программа 1/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 1,
  "trial": {
    "candidate": 1,
    "island": 0,
    "status": "rejected",
    "error": "Function outside allowlist: GROUP",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_01"
  }
}
```

## 2026-10-15T12:09:03+03:00 — llmfe_generating

Локальная LLM предлагает программу 2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 2
}
```

## 2026-10-15T12:09:26+03:00 — llmfe_trial

LLM-FE программа 2/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 2,
  "trial": {
    "candidate": 2,
    "island": 1,
    "status": "rejected",
    "error": "Evaluator exited 1: Traceback (most recent call last):\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 210, in <module>\n    main()\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 177, in main\n    model = fit(engine, program, destination, smoke)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 61, in fit\n    parts.append((engine.matrix(frame), frame.label.to_numpy(dtype=np.int8)))\n                  ^^^^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/features.py\", line 175, in matrix\n    values = self.frame(pairs).to_numpy(dtype=np.float32)\n             ^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/features.py\", line 164, in frame\n    frame = self.con.sql(f\"SELECT {ordered} FROM ({query}) ORDER BY rid\").df()\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nduckdb.duckdb.BinderException: Binder Error: Referenced column \"days_ago\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.raw_u_age\", \"unnamed_subquery.raw_i_index_group_no\", \"unnamed_subquery.raw_i_garment_group_no\", \"unnamed_subquery.raw_u_active\", \"unnamed_subquery.raw_u_fashion_news_frequency\"\n",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_02"
  }
}
```

## 2026-10-15T12:09:26+03:00 — llmfe_generating

Локальная LLM предлагает программу 3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 3
}
```

## 2026-10-15T12:09:29+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v1`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:09:39+03:00 — llmfe_trial

LLM-FE программа 3/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 3,
  "trial": {
    "candidate": 3,
    "island": 2,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_03"
  }
}
```

## 2026-10-15T12:09:39+03:00 — llmfe_generating

Локальная LLM предлагает программу 4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 4
}
```

## 2026-10-15T12:09:45+03:00 — llmfe_trial

LLM-FE программа 4/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 4,
  "trial": {
    "candidate": 4,
    "island": 0,
    "status": "rejected",
    "error": "Forbidden token 'select': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_04"
  }
}
```

## 2026-10-15T12:09:45+03:00 — llmfe_generating

Локальная LLM предлагает программу 5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 5
}
```

## 2026-10-15T12:09:55+03:00 — llmfe_trial

LLM-FE программа 5/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 5,
  "trial": {
    "candidate": 5,
    "island": 1,
    "status": "rejected",
    "error": "Unknown program keys",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_05"
  }
}
```

## 2026-10-15T12:09:55+03:00 — llmfe_generating

Локальная LLM предлагает программу 6/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 6
}
```

## 2026-10-15T12:10:08+03:00 — llmfe_trial

LLM-FE программа 6/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 6,
  "trial": {
    "candidate": 6,
    "island": 2,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_06"
  }
}
```

## 2026-10-15T12:10:09+03:00 — llmfe_generating

Локальная LLM предлагает программу 7/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 7
}
```

## 2026-10-15T12:10:18+03:00 — llmfe_trial

LLM-FE программа 7/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 7,
  "trial": {
    "candidate": 7,
    "island": 0,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_07"
  }
}
```

## 2026-10-15T12:10:18+03:00 — llmfe_generating

Локальная LLM предлагает программу 8/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 8
}
```

## 2026-10-15T12:10:44+03:00 — llmfe_scoring

LLM-FE smoke/val: 8/8 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "smoke",
  "split": "val",
  "scored_users": 8,
  "total_users": 8,
  "catalog_size": 105542
}
```

## 2026-10-15T12:10:44+03:00 — llmfe_smoke

LLM-программа прошла SQL/train/full-catalog smoke; это не итоговые метрики

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "smoke": {
    "stage": "smoke",
    "smoke": true,
    "seed": 42,
    "inference_from_saved_model": true,
    "program_sha256": "5684fa7984e884db2033084bad96fc55aec2199124c8c35f5dc86efaa65f591f",
    "val_metrics": {
      "map": 0.0
    },
    "val_users": 8,
    "val_seconds": 1.9085834739998973,
    "elapsed_seconds": 9.129123668999455,
    "features": [
      "raw_u_age",
      "raw_u_fn",
      "raw_u_active",
      "raw_u_club_member_status",
      "raw_u_fashion_news_frequency",
      "raw_i_product_code",
      "raw_i_product_type_no",
      "raw_i_graphical_appearance_no",
      "raw_i_colour_group_code",
      "raw_i_perceived_colour_value_id",
      "raw_i_perceived_colour_master_id",
      "raw_i_department_no",
      "raw_i_index_group_no",
      "raw_i_section_no",
      "raw_i_garment_group_no",
      "f_customer_product_frequency",
      "f_customer_department_frequency",
      "f_product_sales_count",
      "f_product_days_since_last_purchase",
      "f_customer_past_purchases",
      "f_product_popularity_score",
      "f_combined_frequency"
    ]
  }
}
```

## 2026-10-15T12:11:37+03:00 — llmfe_verified_start

v2 verified running. Four protocol tests passed. Candidate08 generated entirely by local Qwen passed real SQL feature computation, LightGBM train/reload and complete-catalog smoke on 8 validation users (2000 train pairs, 10 rounds; not a full result). Its full 803377-pair / 150-round search evaluation is underway. First seven rejected proposals/errors preserved, no hand-edited feature formulas. v1 orphan evaluator stopped; only v2 remains active. GPU model size_vram=4924207104 bytes. No final metrics yet.

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching"
}
```

## 2026-10-15T12:12:49+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:15:47+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:15:47+03:00 — llmfe_trial

LLM-FE программа 8/20: valid

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 8,
  "trial": {
    "candidate": 8,
    "island": 1,
    "status": "valid",
    "score": 0.005149974446849447,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_08",
    "program_sha256": "5684fa7984e884db2033084bad96fc55aec2199124c8c35f5dc86efaa65f591f",
    "metrics": {
      "stage": "search",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "5684fa7984e884db2033084bad96fc55aec2199124c8c35f5dc86efaa65f591f",
      "val_metrics": {
        "map": 0.005149974446849447
      },
      "val_users": 256,
      "val_seconds": 183.41708184899926,
      "elapsed_seconds": 297.7150652959999,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_product_frequency",
        "f_customer_department_frequency",
        "f_product_sales_count",
        "f_product_days_since_last_purchase",
        "f_customer_past_purchases",
        "f_product_popularity_score",
        "f_combined_frequency"
      ]
    }
  }
}
```

## 2026-10-15T12:15:47+03:00 — llmfe_generating

Локальная LLM предлагает программу 9/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 9
}
```

## 2026-10-15T12:15:54+03:00 — llmfe_trial

LLM-FE программа 9/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 9,
  "trial": {
    "candidate": 9,
    "island": 2,
    "status": "rejected",
    "error": "Forbidden token 'over': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_09"
  }
}
```

## 2026-10-15T12:15:54+03:00 — llmfe_generating

Локальная LLM предлагает программу 10/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 10
}
```

## 2026-10-15T12:17:09+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:21:04+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:21:05+03:00 — llmfe_trial

LLM-FE программа 10/20: valid

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 10,
  "trial": {
    "candidate": 10,
    "island": 0,
    "status": "valid",
    "score": 0.0014026284045815295,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_10",
    "program_sha256": "c51423ce95929bbae6c31fe27d779d55928241f0aeb8644a42c01e8fac8f1601",
    "metrics": {
      "stage": "search",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "c51423ce95929bbae6c31fe27d779d55928241f0aeb8644a42c01e8fac8f1601",
      "val_metrics": {
        "map": 0.0014026284045815295
      },
      "val_users": 256,
      "val_seconds": 242.33417243700023,
      "elapsed_seconds": 296.50358244400013,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_purchase_count",
        "f_article_diversity",
        "f_last_purchase_age",
        "f_avg_article_price",
        "f_recent_purchase_ratio",
        "f_purchase_diversity_per_article"
      ]
    }
  }
}
```

## 2026-10-15T12:21:05+03:00 — llmfe_generating

Локальная LLM предлагает программу 11/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 11
}
```

## 2026-10-15T12:21:18+03:00 — llmfe_trial

LLM-FE программа 11/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 11,
  "trial": {
    "candidate": 11,
    "island": 1,
    "status": "rejected",
    "error": "Evaluator exited 1: Traceback (most recent call last):\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 210, in <module>\n    main()\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 177, in main\n    model = fit(engine, program, destination, smoke)\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/evaluate.py\", line 61, in fit\n    parts.append((engine.matrix(frame), frame.label.to_numpy(dtype=np.int8)))\n                  ^^^^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/features.py\", line 175, in matrix\n    values = self.frame(pairs).to_numpy(dtype=np.float32)\n             ^^^^^^^^^^^^^^^^^\n  File \"/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/features.py\", line 164, in frame\n    frame = self.con.sql(f\"SELECT {ordered} FROM ({query}) ORDER BY rid\").df()\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nduckdb.duckdb.BinderException: Binder Error: Referenced column \"days_ago\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.raw_u_age\", \"unnamed_subquery.raw_i_index_group_no\", \"unnamed_subquery.raw_i_garment_group_no\", \"unnamed_subquery.raw_u_active\", \"unnamed_subquery.raw_u_fashion_news_frequency\"\n",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_11"
  }
}
```

## 2026-10-15T12:21:18+03:00 — llmfe_generating

Локальная LLM предлагает программу 12/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 12
}
```

## 2026-10-15T12:21:29+03:00 — llmfe_trial

LLM-FE программа 12/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 12,
  "trial": {
    "candidate": 12,
    "island": 2,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_12"
  }
}
```

## 2026-10-15T12:21:29+03:00 — llmfe_generating

Локальная LLM предлагает программу 13/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 13
}
```

## 2026-10-15T12:22:48+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:26:56+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:26:56+03:00 — llmfe_trial

LLM-FE программа 13/20: valid

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 13,
  "trial": {
    "candidate": 13,
    "island": 0,
    "status": "valid",
    "score": 0.0013601181081649833,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_13",
    "program_sha256": "2d6be1557488d0d3988b075fdfd455f3c3e3663ff3f25fcaec578c2c3a36287b",
    "metrics": {
      "stage": "search",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "2d6be1557488d0d3988b075fdfd455f3c3e3663ff3f25fcaec578c2c3a36287b",
      "val_metrics": {
        "map": 0.0013601181081649833
      },
      "val_users": 256,
      "val_seconds": 255.7989371599997,
      "elapsed_seconds": 310.97695134100013,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_purchase_count",
        "f_article_diversity",
        "f_last_purchase_age",
        "f_avg_article_price",
        "f_total_spent",
        "f_recent_purchase_ratio",
        "f_purchase_diversity_per_article",
        "f_avg_price_per_purchase"
      ]
    }
  }
}
```

## 2026-10-15T12:26:56+03:00 — llmfe_generating

Локальная LLM предлагает программу 14/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 14
}
```

## 2026-10-15T12:27:11+03:00 — llmfe_trial

LLM-FE программа 14/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 14,
  "trial": {
    "candidate": 14,
    "island": 1,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_14"
  }
}
```

## 2026-10-15T12:27:11+03:00 — llmfe_generating

Локальная LLM предлагает программу 15/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 15
}
```

## 2026-10-15T12:27:21+03:00 — llmfe_trial

LLM-FE программа 15/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 15,
  "trial": {
    "candidate": 15,
    "island": 2,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_15"
  }
}
```

## 2026-10-15T12:27:21+03:00 — llmfe_generating

Локальная LLM предлагает программу 16/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 16
}
```

## 2026-10-15T12:27:35+03:00 — llmfe_trial

LLM-FE программа 16/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 16,
  "trial": {
    "candidate": 16,
    "island": 0,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_16"
  }
}
```

## 2026-10-15T12:27:35+03:00 — llmfe_generating

Локальная LLM предлагает программу 17/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 17
}
```

## 2026-10-15T12:27:50+03:00 — llmfe_trial

LLM-FE программа 17/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 17,
  "trial": {
    "candidate": 17,
    "island": 1,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_17"
  }
}
```

## 2026-10-15T12:27:50+03:00 — llmfe_generating

Локальная LLM предлагает программу 18/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 18
}
```

## 2026-10-15T12:27:56+03:00 — llmfe_trial

LLM-FE программа 18/20: rejected

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 18,
  "trial": {
    "candidate": 18,
    "island": 2,
    "status": "rejected",
    "error": "Unknown feature keys",
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_18"
  }
}
```

## 2026-10-15T12:27:56+03:00 — llmfe_generating

Локальная LLM предлагает программу 19/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 19
}
```

## 2026-10-15T12:29:13+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:33:08+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:33:08+03:00 — llmfe_trial

LLM-FE программа 19/20: valid

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 19,
  "trial": {
    "candidate": 19,
    "island": 0,
    "status": "valid",
    "score": 0.0014026284045815295,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_19",
    "program_sha256": "f31eba31a7b9e709289137295b1afeec154a21a5a8590c4d46b629e790a114b0",
    "metrics": {
      "stage": "search",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "f31eba31a7b9e709289137295b1afeec154a21a5a8590c4d46b629e790a114b0",
      "val_metrics": {
        "map": 0.0014026284045815295
      },
      "val_users": 256,
      "val_seconds": 242.81208010200044,
      "elapsed_seconds": 299.82846100999996,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_purchase_count",
        "f_article_diversity",
        "f_last_purchase_age",
        "f_avg_article_price",
        "f_recent_purchase_ratio",
        "f_purchase_diversity_per_article"
      ]
    }
  }
}
```

## 2026-10-15T12:33:09+03:00 — llmfe_generating

Локальная LLM предлагает программу 20/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "generating",
  "candidate": 20
}
```

## 2026-10-15T12:35:15+03:00 — llmfe_scoring

LLM-FE search/val: 8/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 8,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:38:10+03:00 — llmfe_scoring

LLM-FE search/val: 256/256 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "search",
  "split": "val",
  "scored_users": 256,
  "total_users": 256,
  "catalog_size": 105542
}
```

## 2026-10-15T12:38:10+03:00 — llmfe_trial

LLM-FE программа 20/20: valid

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "searching",
  "completed_proposals": 20,
  "trial": {
    "candidate": 20,
    "island": 1,
    "status": "valid",
    "score": 0.005149974446849447,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_20",
    "program_sha256": "cc87ddf376849522746c08cf5966cd4202f07f078e9805cd206cbc74a575591c",
    "metrics": {
      "stage": "search",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "cc87ddf376849522746c08cf5966cd4202f07f078e9805cd206cbc74a575591c",
      "val_metrics": {
        "map": 0.005149974446849447
      },
      "val_users": 256,
      "val_seconds": 180.72306248399946,
      "elapsed_seconds": 285.97743342299964,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_product_frequency",
        "f_customer_department_frequency",
        "f_product_sales_count",
        "f_product_days_since_last_purchase",
        "f_customer_past_purchases",
        "f_product_popularity_score",
        "f_combined_frequency"
      ]
    }
  }
}
```

## 2026-10-15T12:38:27+03:00 — llmfe_scoring

LLM-FE confirm/val: 8/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 8,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:41:04+03:00 — llmfe_scoring

LLM-FE confirm/val: 264/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 264,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:43:42+03:00 — llmfe_scoring

LLM-FE confirm/val: 520/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 520,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:46:26+03:00 — llmfe_scoring

LLM-FE confirm/val: 776/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 776,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:48:59+03:00 — llmfe_scoring

LLM-FE confirm/val: 1024/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 1024,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:49:12+03:00 — llmfe_scoring

LLM-FE confirm/val: 8/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 8,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:51:48+03:00 — llmfe_scoring

LLM-FE confirm/val: 264/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 264,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:54:23+03:00 — llmfe_scoring

LLM-FE confirm/val: 520/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 520,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:56:59+03:00 — llmfe_scoring

LLM-FE confirm/val: 776/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 776,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:59:30+03:00 — llmfe_scoring

LLM-FE confirm/val: 1024/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 1024,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T12:59:43+03:00 — llmfe_scoring

LLM-FE confirm/val: 8/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 8,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T13:03:20+03:00 — llmfe_scoring

LLM-FE confirm/val: 264/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 264,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T13:07:04+03:00 — llmfe_scoring

LLM-FE confirm/val: 520/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 520,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T13:10:46+03:00 — llmfe_scoring

LLM-FE confirm/val: 776/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 776,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T13:14:18+03:00 — llmfe_scoring

LLM-FE confirm/val: 1024/1024 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "confirm",
  "split": "val",
  "scored_users": 1024,
  "total_users": 1024,
  "catalog_size": 105542
}
```

## 2026-10-15T13:14:18+03:00 — llmfe_selected

Программа выбрана по отдельной confirmation validation; начата полная оценка

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "selection": {
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_08",
    "score": 0.002461205244408369,
    "metrics": {
      "stage": "confirm",
      "smoke": false,
      "seed": 42,
      "inference_from_saved_model": true,
      "program_sha256": "5684fa7984e884db2033084bad96fc55aec2199124c8c35f5dc86efaa65f591f",
      "val_metrics": {
        "map": 0.002461205244408369
      },
      "val_users": 1024,
      "val_seconds": 637.2611580519997,
      "elapsed_seconds": 643.7302280969998,
      "features": [
        "raw_u_age",
        "raw_u_fn",
        "raw_u_active",
        "raw_u_club_member_status",
        "raw_u_fashion_news_frequency",
        "raw_i_product_code",
        "raw_i_product_type_no",
        "raw_i_graphical_appearance_no",
        "raw_i_colour_group_code",
        "raw_i_perceived_colour_value_id",
        "raw_i_perceived_colour_master_id",
        "raw_i_department_no",
        "raw_i_index_group_no",
        "raw_i_section_no",
        "raw_i_garment_group_no",
        "f_customer_product_frequency",
        "f_customer_department_frequency",
        "f_product_sales_count",
        "f_product_days_since_last_purchase",
        "f_customer_past_purchases",
        "f_product_popularity_score",
        "f_combined_frequency"
      ]
    }
  }
}
```

## 2026-10-15T13:14:31+03:00 — llmfe_scoring

LLM-FE final/val: 8/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 8,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:17:07+03:00 — llmfe_scoring

LLM-FE final/val: 264/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 264,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:18:00+03:00 — llmfe_progress_plots

Built read-only progress plots from saved v2 artifacts: search/confirmation MAP, valid/rejected proposal histogram, feature gain and confirmation per-user AP histogram. All 20 proposals processed: 5 valid, 15 rejected. Selected candidate08; confirmation MAP=0.002461205244408369 on 1024 users, not full validation/test. Per-user AP mean matches saved MAP exactly. Full evaluator still active; no training/protocol change. Training loss by boosting round was not recorded.

## 2026-10-15T13:19:47+03:00 — llmfe_scoring

LLM-FE final/val: 520/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 520,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:22:18+03:00 — llmfe_scoring

LLM-FE final/val: 776/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 776,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:24:48+03:00 — llmfe_scoring

LLM-FE final/val: 1032/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 1032,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:27:17+03:00 — llmfe_scoring

LLM-FE final/val: 1288/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 1288,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:29:46+03:00 — llmfe_scoring

LLM-FE final/val: 1544/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 1544,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:32:15+03:00 — llmfe_scoring

LLM-FE final/val: 1800/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 1800,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:34:47+03:00 — llmfe_scoring

LLM-FE final/val: 2056/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 2056,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:35:57+03:00 — llmfe_rejection_audit

Audited all 15 v2 rejections (first recorded reasons): unsupported OVER 6; days_ago out of derived-feature scope 2; unsupported grouping keys 2; malformed program/feature structure 2; SELECT subquery 1; string-valued feature 1; validator misclassifying WITHIN GROUP SQL syntax as a function 1. Candidate01 also contains other invalid references/strings; fixing that parser issue alone would not validate it. These are execution/interface failures, not low-MAP results. Only 5/20 programs were evaluated, limiting conclusions about LLM feature quality. Audit saved; current experiment unchanged.

## 2026-10-15T13:37:24+03:00 — llmfe_scoring

LLM-FE final/val: 2312/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 2312,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:39:57+03:00 — llmfe_scoring

LLM-FE final/val: 2568/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 2568,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:41:49+03:00 — hypothesis_added

Added H002 at user request: maximize distinct successfully evaluated LLM feature sets by separating successful-set target from total generation/repair-call budget and adding LLM program repair. Discussion reference 20 evaluated sets / up to 100 calls; final limits to be fixed before a new run. Track failures, duplicates, repairs, cost and MAP curves; keep temporal validation/confirmation and untouched test. Current v2 unchanged; H002 not launched.

## 2026-10-15T13:42:37+03:00 — llmfe_scoring

LLM-FE final/val: 2824/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 2824,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:45:22+03:00 — llmfe_scoring

LLM-FE final/val: 3080/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 3080,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:46:03+03:00 — llmfe_scoring_profile

Profiled saved candidate08 on 8 already-scored validation users/full catalog while live evaluator continues: features 0.852s, prediction 2 threads 5.364s / 6 threads 3.219s / 12 threads 2.704s, top-k 0.016s; all prediction arrays bit-identical across thread counts and top12 identical to live saved outputs. Main bottleneck is CPU tree inference; 12 logical CPUs available. Measurements under concurrent load, not a production speed guarantee. GPU LightGBM inference via separate forest runtime is an option requiring compatibility/equivalence validation. Benchmark saved; active evaluator not changed.

## 2026-10-15T13:48:01+03:00 — llmfe_scoring

LLM-FE final/val: 3336/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 3336,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:50:34+03:00 — llmfe_scoring

LLM-FE final/val: 3592/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 3592,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:55:10+03:00 — llmfe_resume

Продолжена финальная оценка сохранённой модели; поиск и обучение не повторяются

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "artifacts": "LLMFeatures/results/qwen25coder7b_seed42_v2/candidates/candidate_08"
}
```

## 2026-10-15T13:56:23+03:00 — llmfe_scoring

LLM-FE final/val: 3848/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 3848,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:56:31+03:00 — llmfe_cpu_acceleration_applied

Verified and applied CPU inference acceleration. Isolated benchmark: 32 validation users, complete catalog, 3377344 pairs per pass, 8 timing repeats per setting. All scores bit-identical for 2/6/8/12 threads; all top12 identical to saved predictions. Chose 8 threads: median prediction 2.162s vs 4.440s, expected end-to-end 1.65x. Resumed from 3680 completed users; already 3776 after 35.84s, preserved prefix checksum verified. Model/program hashes unchanged, no training/search repeated. Execution ID hm_llmfe_qwen25coder7b_seed42_v2_cpu8_inference_v1, proof/settings/source hashes saved separately. Active final evaluator uses 8 threads.

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-15T13:57:57+03:00 — llmfe_scoring

LLM-FE final/val: 4104/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 4104,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T13:59:29+03:00 — llmfe_scoring

LLM-FE final/val: 4360/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 4360,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:01:02+03:00 — llmfe_scoring

LLM-FE final/val: 4616/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 4616,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:02:39+03:00 — llmfe_scoring

LLM-FE final/val: 4872/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 4872,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:04:15+03:00 — llmfe_scoring

LLM-FE final/val: 5128/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 5128,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:04:56+03:00 — llmfe_training_comparability_audit

Compared saved training code/configs: manual LightGBM and LLM LightGBM use identical 803377 pairs / 50000 user-times, binary objective, 150 rounds, winning 31 leaves, lr0.05 and main sampling/leaf/bin settings. Exact controls differ: manual tuned 15/31 leaves on 10000 validation users/ID-GNN pools; LLM fixed31 leaves and selected feature programs on256 full-catalog users then1024 confirmation. LLM explicitly sets feature_fraction_seed/bagging_seed/data_random_seed=42; manual supplies global seed42 only. Prior wording identical parameters was too broad. Final evaluation pools also differ unless using shared-candidate results. No current experiment changes.

## 2026-10-15T14:05:49+03:00 — llmfe_scoring

LLM-FE final/val: 5384/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 5384,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:07:23+03:00 — llmfe_scoring

LLM-FE final/val: 5640/74575 пользователей, полный каталог

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "evaluating",
  "stage": "final",
  "split": "val",
  "scored_users": 5640,
  "total_users": 74575,
  "catalog_size": 105542
}
```

## 2026-10-15T14:11:00+03:00 — llmfe_shared_start

Начата отдельная оценка выбранного LLM-LightGBM на общих кандидатах ID-GNN

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "evaluating",
  "artifacts": "LLMFeatures/results/qwen25coder7b_seed42_v2/shared_idgnn"
}
```

## 2026-10-15T14:11:31+03:00 — llmfe_full_catalog_paused

User explicitly requested pause full catalog and evaluate shared ID-GNN candidates. Supervisor and evaluator stopped, checkpoint/predictions retained at5840/74575 validation users. full_catalog_paused.json blocks automatic resume. New frozen-model shared evaluation has separate run_id hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1, complete val/test and independent full replay; no new feature selection or training.

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2`.

```json
{
  "status": "paused"
}
```

## 2026-10-15T14:11:36+03:00 — candidate_pool_audit

По запросу пользователя проверены фактические candidate pools: пары val/test ручных признаков точно совпадают с экспортом ID-GNN seed42; все top12 ID-GNN/LightGBM manual/DecisionTree manual внутри того же pool. Важное уточнение: ID-GNN вычисляет sigmoid для sampled товаров и ноль остальному каталогу; экспорт добавляет zero-score fallback top12.

```json
{
  "checks": {
    "val": {
      "users": 74575,
      "candidate_pairs": 2088583,
      "mean_candidates": 28.00647670130741,
      "feature_pairs_exactly_match_pool": true,
      "candidate_file_sha256": "f36065a102faed41465a7aae93d7f5f994452ebb18b1045938b7db5019cda9c1",
      "methods": {
        "idgnn": {
          "recommendations": 894900,
          "outside_pool": 0
        },
        "lightgbm_manual": {
          "recommendations": 894900,
          "outside_pool": 0
        },
        "decision_tree_manual": {
          "recommendations": 894900,
          "outside_pool": 0
        }
      }
    },
    "test": {
      "users": 67144,
      "candidate_pairs": 1892405,
      "mean_candidates": 28.184275586798524,
      "feature_pairs_exactly_match_pool": true,
      "candidate_file_sha256": "023cfbb8126cdaaa73083bcc9709b4af369d63e2c2f5717ea98b5388b4080d9b",
      "methods": {
        "idgnn": {
          "recommendations": 805728,
          "outside_pool": 0
        },
        "lightgbm_manual": {
          "recommendations": 805728,
          "outside_pool": 0
        },
        "decision_tree_manual": {
          "recommendations": 805728,
          "outside_pool": 0
        }
      }
    }
  },
  "artifacts": "reports/relbench_hm_v1/candidate_audit.json"
}
```

## 2026-10-15T14:11:37+03:00 — llmfe_shared_split

LLM-FE общие кандидаты: val оценён

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "evaluating",
  "split": "val",
  "split_result": {
    "users": 74575,
    "pairs": 2088583,
    "candidate_file_sha256": "f36065a102faed41465a7aae93d7f5f994452ebb18b1045938b7db5019cda9c1",
    "metrics": {
      "map": 0.008542810038877146
    },
    "idgnn_metrics_recomputed": {
      "map": 0.02634419239310869
    },
    "seconds": 28.584748388000662
  }
}
```

## 2026-10-15T14:12:09+03:00 — llmfe_shared_split

LLM-FE общие кандидаты: test оценён

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "evaluating",
  "split": "test",
  "split_result": {
    "users": 67144,
    "pairs": 1892405,
    "candidate_file_sha256": "023cfbb8126cdaaa73083bcc9709b4af369d63e2c2f5717ea98b5388b4080d9b",
    "metrics": {
      "map": 0.008117509149461
    },
    "idgnn_metrics_recomputed": {
      "map": 0.027843150477067403
    },
    "seconds": 27.029122043000825
  }
}
```

## 2026-10-15T14:12:58+03:00 — llmfe_shared_split

LLM-FE общие кандидаты: val перепроверен

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "verifying",
  "split": "val",
  "split_result": {
    "users": 74575,
    "pairs": 2088583,
    "candidate_file_sha256": "f36065a102faed41465a7aae93d7f5f994452ebb18b1045938b7db5019cda9c1",
    "metrics": {
      "map": 0.008542810038877146
    },
    "idgnn_metrics_recomputed": {
      "map": 0.02634419239310869
    },
    "seconds": 38.21661010899879,
    "predictions_identical": true
  }
}
```

## 2026-10-15T14:13:37+03:00 — llmfe_shared_split

LLM-FE общие кандидаты: test перепроверен

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "verifying",
  "split": "test",
  "split_result": {
    "users": 67144,
    "pairs": 1892405,
    "candidate_file_sha256": "023cfbb8126cdaaa73083bcc9709b4af369d63e2c2f5717ea98b5388b4080d9b",
    "metrics": {
      "map": 0.008117509149461
    },
    "idgnn_metrics_recomputed": {
      "map": 0.027843150477067403
    },
    "seconds": 34.29561228999955,
    "predictions_identical": true
  }
}
```

## 2026-10-15T14:13:38+03:00 — llmfe_shared_complete

LLM-LightGBM оценён на общих кандидатах ID-GNN; полный повтор подтвердил предсказания

Запуск: `hm_llmfe_qwen25coder7b_seed42_v2_shared_idgnn_inference_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.008542810038877146
  },
  "test_metrics": {
    "map": 0.008117509149461
  },
  "artifacts": "reports/llmfe_qwen25coder7b_v2/shared_idgnn"
}
```

## 2026-10-15T14:16:38+03:00 — llmfe_shared_report_verified

Shared ID-GNN-pool evaluation completed exitcode0, independent full val/test replay identical. LLM-LightGBM val/test MAP=0.008542810038877146 /0.008117509149461 on2088583/1892405 pairs. ID-GNN metrics recomputed exactly; manual LightGBM previous metrics use same pools. Comparison chart plus per-user AP histograms, first-hit rank and paired LLM/manual comparison saved under reports/llmfe_qwen25coder7b_v2/shared_idgnn. AP means for all four models match saved MAP; source hashes and per-user CSV retained. LLM beats manual for821 test users, ties61741, loses4582. Full catalog remains user-paused at5840 validation users; no retraining or test-driven selection.

## 2026-10-15T14:33:21+03:00 — h002_start

H002: 20 различных оценённых наборов, до100 запросов, до2 исправлений; поиск на общих кандидатах, LightGBM8 потоков

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "preparing",
  "config": {
    "run_id": "hm_llmfe_qwen25coder7b_seed42_h002_shared_v1",
    "hypothesis": "H002",
    "seed": 42,
    "llm": "qwen2.5-coder:7b-instruct-q4_K_M",
    "model_digest": "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364",
    "target_successful_distinct": 20,
    "max_llm_calls": 100,
    "max_repairs_per_proposal": 2,
    "islands": 3,
    "memory_programs": 1,
    "context_tokens": 4096,
    "generation_tokens": 1800,
    "temperature": 0.8,
    "train_pairs": 803377,
    "train_user_times": 50000,
    "pair_selection_seed": 2026,
    "training_threads": 8,
    "prediction_threads": 8,
    "rounds": 150,
    "search_users": 256,
    "confirmation_users": 1024,
    "confirmation_candidates": 3,
    "search_protocol": "fixed saved ID-GNN candidates; same user selections as v2",
    "final_protocol": "all val/test users, exact saved ID-GNN candidate pools, independent full replay",
    "full_catalog": false,
    "validator": "h002: WITHIN GROUP syntax false rejection fixed",
    "control": "v2 five measured sets; different search pool, increased calls, repair and prompt changes confound isolated attribution",
    "downstream": "same binary LightGBM150/leaves31/seeds42 as v2, 8 threads",
    "test_policy": "test only after selection frozen on disjoint validation confirmation"
  },
  "artifacts": "LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1"
}
```

## 2026-10-15T14:33:43+03:00 — h002_generating

H002 запрос1/100, оценено0/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 1,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:36:21+03:00 — h002_trial

H002 запрос1: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 1,
  "evaluated_distinct": 0,
  "trial": {
    "call": 1,
    "proposal": 0,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_001",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 406,
    "llm_seconds": 155.767390629,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 155.83275660599975
  }
}
```

## 2026-10-15T14:36:21+03:00 — h002_generating

H002 запрос2/100, оценено0/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 2,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:36:36+03:00 — h002_trial

H002 запрос2: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 2,
  "evaluated_distinct": 0,
  "trial": {
    "call": 2,
    "proposal": 0,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_002",
    "parent_call": 1,
    "prompt_tokens": 1656,
    "generated_tokens": 357,
    "llm_seconds": 14.490521363,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 14.543034296999394
  }
}
```

## 2026-10-15T14:36:36+03:00 — h002_generating

H002 запрос3/100, оценено0/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 3,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:36:52+03:00 — h002_trial

H002 запрос3: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 3,
  "evaluated_distinct": 0,
  "trial": {
    "call": 3,
    "proposal": 0,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_003",
    "parent_call": 2,
    "prompt_tokens": 1597,
    "generated_tokens": 357,
    "llm_seconds": 14.666633251,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 14.713737014999424
  }
}
```

## 2026-10-15T14:36:52+03:00 — h002_generating

H002 запрос4/100, оценено0/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 4,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:37:02+03:00 — h002_trial

H002 запрос4: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 4,
  "evaluated_distinct": 0,
  "trial": {
    "call": 4,
    "proposal": 1,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_004",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 214,
    "llm_seconds": 9.319630334,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 9.3735292270012
  }
}
```

## 2026-10-15T14:37:02+03:00 — h002_generating

H002 запрос5/100, оценено0/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 5,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:37:13+03:00 — h002_trial

H002 запрос5: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 5,
  "evaluated_distinct": 0,
  "trial": {
    "call": 5,
    "proposal": 1,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_005",
    "parent_call": 4,
    "prompt_tokens": 1464,
    "generated_tokens": 221,
    "llm_seconds": 9.477230243,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 9.537248406999424
  }
}
```

## 2026-10-15T14:37:13+03:00 — h002_generating

H002 запрос6/100, оценено0/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 6,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:37:25+03:00 — h002_trial

H002 запрос6: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 6,
  "evaluated_distinct": 0,
  "trial": {
    "call": 6,
    "proposal": 1,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_006",
    "parent_call": 5,
    "prompt_tokens": 1471,
    "generated_tokens": 217,
    "llm_seconds": 9.38651196,
    "program_sha256": "086d56601b75586942afc63011e98c63af5a0b0aaf0f131d6a1b5c229462ae0e",
    "status": "rejected",
    "error": "Binder Error: column \"rid\" must appear in the GROUP BY clause or must be part of an aggregate function.\nEither add it to the GROUP BY list, or use \"ANY_VALUE(rid)\" if the exact value of \"rid\" is not important.",
    "elapsed_seconds": 11.786141193999356
  }
}
```

## 2026-10-15T14:37:25+03:00 — h002_generating

H002 запрос7/100, оценено0/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 7,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:37:39+03:00 — h002_trial

H002 запрос7: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 7,
  "evaluated_distinct": 0,
  "trial": {
    "call": 7,
    "proposal": 2,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_007",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 282,
    "llm_seconds": 12.491845254,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 12.548587232999125
  }
}
```

## 2026-10-15T14:37:39+03:00 — h002_generating

H002 запрос8/100, оценено0/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 8,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:37:52+03:00 — h002_trial

H002 запрос8: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 8,
  "evaluated_distinct": 0,
  "trial": {
    "call": 8,
    "proposal": 2,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_008",
    "parent_call": 7,
    "prompt_tokens": 1532,
    "generated_tokens": 282,
    "llm_seconds": 11.977134299,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 12.045711405000475
  }
}
```

## 2026-10-15T14:37:52+03:00 — h002_generating

H002 запрос9/100, оценено0/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 9,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:38:05+03:00 — h002_trial

H002 запрос9: rejected; различных оценённых0/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 9,
  "evaluated_distinct": 0,
  "trial": {
    "call": 9,
    "proposal": 2,
    "island": 2,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_009",
    "parent_call": 8,
    "prompt_tokens": 1532,
    "generated_tokens": 282,
    "llm_seconds": 12.231773261,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 12.306921006000266
  }
}
```

## 2026-10-15T14:38:05+03:00 — h002_generating

H002 запрос10/100, оценено0/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 10,
  "evaluated_distinct": 0
}
```

## 2026-10-15T14:40:36+03:00 — h002_trial

H002 запрос10: valid; различных оценённых1/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 10,
  "evaluated_distinct": 1,
  "trial": {
    "call": 10,
    "proposal": 3,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_010",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 385,
    "llm_seconds": 16.979883295,
    "program_sha256": "01f1762e124c835462c85fa1865ca92c17a0b2c9d7d2f9338145f634e14f5b06",
    "status": "valid",
    "score": 0.010144469246031747,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "bffbf9ad3b35d7b0352dacbe8d09f31cc4bbdd2fd2b5ad11677e4fd8579bfff6",
      "program_sha256": "bbd26fc091c32c90ce76b5055fda42f398882a689ff38718e16867ea69c06f11",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.010144469246031747
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 3.976385306999873,
      "elapsed_seconds": 120.65982826100117,
      "passed": true
    },
    "elapsed_seconds": 149.41507942799944
  }
}
```

## 2026-10-15T14:40:36+03:00 — h002_generating

H002 запрос11/100, оценено1/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 11,
  "evaluated_distinct": 1
}
```

## 2026-10-15T14:41:11+03:00 — h002_launch_verified

H002 выполняется: первый набор полностью обучен и оценён; CPU8 проверен, живые графики созданы. Итоговых метрик пока нет.

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "first_score_seconds": 3.976385306999873,
  "tests_passed": 6,
  "training_threads_check": {
    "checked_pairs": 2048,
    "old_threads": 2,
    "new_threads": 8,
    "scores_bit_identical": true
  },
  "full_catalog_resumed": false,
  "experiment_complete": false,
  "first_evaluated_candidate": 10,
  "search_pairs": 6594,
  "first_search_map": 0.010144469246031747,
  "graphs": "reports/llmfe_h002_shared_v1/progress.md",
  "first_train_and_score_seconds": 120.65982826100117
}
```

## 2026-10-15T14:42:14+03:00 — h002_trial

H002 запрос11: valid; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 11,
  "evaluated_distinct": 2,
  "trial": {
    "call": 11,
    "proposal": 4,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_011",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 236,
    "llm_seconds": 9.874659547,
    "program_sha256": "2edba69d0d40b1b78ee7aa7cbaf181c22d92caed46b17154d93f0c5f29becfec",
    "status": "valid",
    "score": 0.008225213913690476,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "b3d97aa52e3a0bea3bea9b0825da617651c3d781ad008eeaebc04873c92feb84",
      "program_sha256": "dd836a5d24c9db7b5118aa2bded361d8b54c4775a74e27a3a97be4e70ecce190",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.008225213913690476
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 2.2115401359988027,
      "elapsed_seconds": 79.83291100399947,
      "passed": true
    },
    "elapsed_seconds": 97.00829434799925
  }
}
```

## 2026-10-15T14:42:14+03:00 — h002_generating

H002 запрос12/100, оценено2/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 12,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:42:27+03:00 — h002_trial

H002 запрос12: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 12,
  "evaluated_distinct": 2,
  "trial": {
    "call": 12,
    "proposal": 5,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_012",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 284,
    "llm_seconds": 11.374309155,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 11.433930460001648
  }
}
```

## 2026-10-15T14:42:27+03:00 — h002_generating

H002 запрос13/100, оценено2/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 13,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:42:37+03:00 — h002_trial

H002 запрос13: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 13,
  "evaluated_distinct": 2,
  "trial": {
    "call": 13,
    "proposal": 5,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_013",
    "parent_call": 12,
    "prompt_tokens": 1534,
    "generated_tokens": 230,
    "llm_seconds": 9.266519088,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 9.324338119000458
  }
}
```

## 2026-10-15T14:42:37+03:00 — h002_generating

H002 запрос14/100, оценено2/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 14,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:42:48+03:00 — h002_trial

H002 запрос14: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 14,
  "evaluated_distinct": 2,
  "trial": {
    "call": 14,
    "proposal": 5,
    "island": 2,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_014",
    "parent_call": 13,
    "prompt_tokens": 1480,
    "generated_tokens": 234,
    "llm_seconds": 9.763807785,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 9.831693531999917
  }
}
```

## 2026-10-15T14:42:48+03:00 — h002_generating

H002 запрос15/100, оценено2/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 15,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:43:00+03:00 — h002_trial

H002 запрос15: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 15,
  "evaluated_distinct": 2,
  "trial": {
    "call": 15,
    "proposal": 6,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_015",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 269,
    "llm_seconds": 10.980338993,
    "status": "rejected",
    "error": "Forbidden token 'customer_id': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 11.034838135999962
  }
}
```

## 2026-10-15T14:43:00+03:00 — h002_generating

H002 запрос16/100, оценено2/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 16,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:43:12+03:00 — h002_trial

H002 запрос16: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 16,
  "evaluated_distinct": 2,
  "trial": {
    "call": 16,
    "proposal": 6,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_016",
    "parent_call": 15,
    "prompt_tokens": 1520,
    "generated_tokens": 269,
    "llm_seconds": 10.786486608,
    "status": "rejected",
    "error": "Forbidden token 'customer_id': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.838368501999867
  }
}
```

## 2026-10-15T14:43:12+03:00 — h002_generating

H002 запрос17/100, оценено2/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 17,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:43:25+03:00 — h002_trial

H002 запрос17: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 17,
  "evaluated_distinct": 2,
  "trial": {
    "call": 17,
    "proposal": 6,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_017",
    "parent_call": 16,
    "prompt_tokens": 1520,
    "generated_tokens": 269,
    "llm_seconds": 10.829752033,
    "status": "rejected",
    "error": "Forbidden token 'customer_id': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.88201111700073
  }
}
```

## 2026-10-15T14:43:25+03:00 — h002_generating

H002 запрос18/100, оценено2/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 18,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:43:36+03:00 — h002_trial

H002 запрос18: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 18,
  "evaluated_distinct": 2,
  "trial": {
    "call": 18,
    "proposal": 7,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_018",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 258,
    "llm_seconds": 10.439437453,
    "status": "rejected",
    "error": "Forbidden token 'over': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.49631864299954
  }
}
```

## 2026-10-15T14:43:36+03:00 — h002_generating

H002 запрос19/100, оценено2/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 19,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:43:49+03:00 — h002_trial

H002 запрос19: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 19,
  "evaluated_distinct": 2,
  "trial": {
    "call": 19,
    "proposal": 7,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_019",
    "parent_call": 18,
    "prompt_tokens": 1508,
    "generated_tokens": 273,
    "llm_seconds": 11.366825294,
    "status": "rejected",
    "error": "Forbidden token 'select': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 11.430184884999107
  }
}
```

## 2026-10-15T14:43:49+03:00 — h002_generating

H002 запрос20/100, оценено2/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 20,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:44:01+03:00 — h002_trial

H002 запрос20: rejected; различных оценённых2/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 20,
  "evaluated_distinct": 2,
  "trial": {
    "call": 20,
    "proposal": 7,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_020",
    "parent_call": 19,
    "prompt_tokens": 1523,
    "generated_tokens": 238,
    "llm_seconds": 10.286174775,
    "status": "rejected",
    "error": "Forbidden token 'select': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.343985827999859
  }
}
```

## 2026-10-15T14:44:01+03:00 — h002_generating

H002 запрос21/100, оценено2/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 21,
  "evaluated_distinct": 2
}
```

## 2026-10-15T14:45:27+03:00 — h002_trial

H002 запрос21: valid; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 21,
  "evaluated_distinct": 3,
  "trial": {
    "call": 21,
    "proposal": 8,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_021",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 394,
    "llm_seconds": 16.265797549,
    "program_sha256": "12bbc7f3055039a81ecfe78f2d42d90971bfe629001cc5eb3931d7daa92c78d3",
    "status": "valid",
    "score": 0.011892722800925924,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "f161b42affd55c783735f775c7d46a811ceaecbdcbf174255e5ee33683250659",
      "program_sha256": "266618136da8f17ae918f5027b0db8d07433ea830c7ad31ee838f86fe15f5503",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.011892722800925924
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.5458278890000656,
      "elapsed_seconds": 60.68760718199883,
      "passed": true
    },
    "elapsed_seconds": 84.62969901699944
  }
}
```

## 2026-10-15T14:45:27+03:00 — h002_generating

H002 запрос22/100, оценено3/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 22,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:45:39+03:00 — h002_trial

H002 запрос22: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 22,
  "evaluated_distinct": 3,
  "trial": {
    "call": 22,
    "proposal": 9,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_022",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 258,
    "llm_seconds": 10.65246111,
    "status": "rejected",
    "error": "Forbidden token 'FROM': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.699750110999958
  }
}
```

## 2026-10-15T14:45:39+03:00 — h002_generating

H002 запрос23/100, оценено3/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 23,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:45:51+03:00 — h002_trial

H002 запрос23: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 23,
  "evaluated_distinct": 3,
  "trial": {
    "call": 23,
    "proposal": 9,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_023",
    "parent_call": 22,
    "prompt_tokens": 1508,
    "generated_tokens": 254,
    "llm_seconds": 10.566564509,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "elapsed_seconds": 10.625161283000125
  }
}
```

## 2026-10-15T14:45:51+03:00 — h002_generating

H002 запрос24/100, оценено3/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 24,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:46:03+03:00 — h002_trial

H002 запрос24: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 24,
  "evaluated_distinct": 3,
  "trial": {
    "call": 24,
    "proposal": 9,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_024",
    "parent_call": 23,
    "prompt_tokens": 1485,
    "generated_tokens": 254,
    "llm_seconds": 10.463120549,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "elapsed_seconds": 10.5215167009992
  }
}
```

## 2026-10-15T14:46:03+03:00 — h002_generating

H002 запрос25/100, оценено3/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 25,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:46:19+03:00 — h002_trial

H002 запрос25: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 25,
  "evaluated_distinct": 3,
  "trial": {
    "call": 25,
    "proposal": 10,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_025",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 365,
    "llm_seconds": 14.898098018,
    "status": "rejected",
    "error": "Forbidden token 'over': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 14.956065180000223
  }
}
```

## 2026-10-15T14:46:19+03:00 — h002_generating

H002 запрос26/100, оценено3/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 26,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:46:36+03:00 — h002_trial

H002 запрос26: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 26,
  "evaluated_distinct": 3,
  "trial": {
    "call": 26,
    "proposal": 10,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_026",
    "parent_call": 25,
    "prompt_tokens": 1615,
    "generated_tokens": 370,
    "llm_seconds": 15.550052016,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 15.604626846999963
  }
}
```

## 2026-10-15T14:46:36+03:00 — h002_generating

H002 запрос27/100, оценено3/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 27,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:46:53+03:00 — h002_trial

H002 запрос27: rejected; различных оценённых3/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 27,
  "evaluated_distinct": 3,
  "trial": {
    "call": 27,
    "proposal": 10,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_027",
    "parent_call": 26,
    "prompt_tokens": 1610,
    "generated_tokens": 370,
    "llm_seconds": 15.864490005,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 15.928403313999297
  }
}
```

## 2026-10-15T14:46:54+03:00 — h002_generating

H002 запрос28/100, оценено3/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 28,
  "evaluated_distinct": 3
}
```

## 2026-10-15T14:48:23+03:00 — h002_trial

H002 запрос28: valid; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 28,
  "evaluated_distinct": 4,
  "trial": {
    "call": 28,
    "proposal": 11,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_028",
    "parent_call": null,
    "prompt_tokens": 1512,
    "generated_tokens": 325,
    "llm_seconds": 15.012155684,
    "program_sha256": "ecd6e7ed240794fff8466f1b4ad46d7aa4bbc650bb3f8fd4554ae84ea969d892",
    "status": "valid",
    "score": 0.01142588458994709,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "adfa901654f8bf663160bee5e0505c55ce1598394376754edc5a3195f8d57bd5",
      "program_sha256": "a5ffde247c6d80aa82ce0e3cc3d2a8031a99beff1a89171c58b8a188c5e9d00d",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.01142588458994709
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.6548595449985442,
      "elapsed_seconds": 65.45012916799897,
      "passed": true
    },
    "elapsed_seconds": 88.58125004199974
  }
}
```

## 2026-10-15T14:48:23+03:00 — h002_generating

H002 запрос29/100, оценено4/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 29,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:48:40+03:00 — h002_trial

H002 запрос29: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 29,
  "evaluated_distinct": 4,
  "trial": {
    "call": 29,
    "proposal": 12,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_029",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 381,
    "llm_seconds": 15.71060135,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 15.774429115999737
  }
}
```

## 2026-10-15T14:48:40+03:00 — h002_generating

H002 запрос30/100, оценено4/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 30,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:48:57+03:00 — h002_trial

H002 запрос30: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 30,
  "evaluated_distinct": 4,
  "trial": {
    "call": 30,
    "proposal": 12,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_030",
    "parent_call": 29,
    "prompt_tokens": 1631,
    "generated_tokens": 381,
    "llm_seconds": 15.485629753,
    "status": "rejected",
    "error": "Forbidden token 'customer_id': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 15.55581468499986
  }
}
```

## 2026-10-15T14:48:57+03:00 — h002_generating

H002 запрос31/100, оценено4/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 31,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:49:09+03:00 — h002_trial

H002 запрос31: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 31,
  "evaluated_distinct": 4,
  "trial": {
    "call": 31,
    "proposal": 12,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_031",
    "parent_call": 30,
    "prompt_tokens": 1632,
    "generated_tokens": 249,
    "llm_seconds": 10.107022438,
    "status": "rejected",
    "error": "Forbidden token 'customer_id': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 10.161265599001126
  }
}
```

## 2026-10-15T14:49:09+03:00 — h002_generating

H002 запрос32/100, оценено4/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 32,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:49:28+03:00 — h002_trial

H002 запрос32: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 32,
  "evaluated_distinct": 4,
  "trial": {
    "call": 32,
    "proposal": 13,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_032",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 370,
    "llm_seconds": 15.192960652,
    "program_sha256": "09df8f350ecd1a7eb122075242a7ccca3791045f9f69192f7a971d97cb66af50",
    "status": "rejected",
    "error": "Binder Error: column \"rid\" must appear in the GROUP BY clause or must be part of an aggregate function.\nEither add it to the GROUP BY list, or use \"ANY_VALUE(rid)\" if the exact value of \"rid\" is not important.",
    "elapsed_seconds": 18.27060540000093
  }
}
```

## 2026-10-15T14:49:28+03:00 — h002_generating

H002 запрос33/100, оценено4/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 33,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:49:48+03:00 — h002_trial

H002 запрос33: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 33,
  "evaluated_distinct": 4,
  "trial": {
    "call": 33,
    "proposal": 13,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_033",
    "parent_call": 32,
    "prompt_tokens": 1650,
    "generated_tokens": 373,
    "llm_seconds": 15.676219331,
    "program_sha256": "09df8f350ecd1a7eb122075242a7ccca3791045f9f69192f7a971d97cb66af50",
    "status": "rejected",
    "error": "Binder Error: column \"rid\" must appear in the GROUP BY clause or must be part of an aggregate function.\nEither add it to the GROUP BY list, or use \"ANY_VALUE(rid)\" if the exact value of \"rid\" is not important.",
    "elapsed_seconds": 18.659464397998818
  }
}
```

## 2026-10-15T14:49:48+03:00 — h002_generating

H002 запрос34/100, оценено4/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 34,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:50:09+03:00 — h002_trial

H002 запрос34: rejected; различных оценённых4/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 34,
  "evaluated_distinct": 4,
  "trial": {
    "call": 34,
    "proposal": 13,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_034",
    "parent_call": 33,
    "prompt_tokens": 1653,
    "generated_tokens": 373,
    "llm_seconds": 15.753047938,
    "program_sha256": "09df8f350ecd1a7eb122075242a7ccca3791045f9f69192f7a971d97cb66af50",
    "status": "rejected",
    "error": "Binder Error: column \"rid\" must appear in the GROUP BY clause or must be part of an aggregate function.\nEither add it to the GROUP BY list, or use \"ANY_VALUE(rid)\" if the exact value of \"rid\" is not important.",
    "elapsed_seconds": 18.9262218519998
  }
}
```

## 2026-10-15T14:50:09+03:00 — h002_generating

H002 запрос35/100, оценено4/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 35,
  "evaluated_distinct": 4
}
```

## 2026-10-15T14:51:33+03:00 — h002_trial

H002 запрос35: valid; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 35,
  "evaluated_distinct": 5,
  "trial": {
    "call": 35,
    "proposal": 14,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_035",
    "parent_call": null,
    "prompt_tokens": 1512,
    "generated_tokens": 321,
    "llm_seconds": 13.534074223,
    "program_sha256": "c73c9d733d44c07292a8f4a51ff742ad0fca788257352f4c2523c6d4325d7cfb",
    "status": "valid",
    "score": 0.010669224800084174,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "abc6de31f8a506094fb78c1c5bd0f8ad8f8efea8d81db952ce3d4d6d3c1a1c1a",
      "program_sha256": "ed68bad216fa982916f4257087d9358e18bf4457d88673c7ca7218759010416b",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.010669224800084174
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.6155201789988496,
      "elapsed_seconds": 62.19711509700028,
      "passed": true
    },
    "elapsed_seconds": 83.00535299999865
  }
}
```

## 2026-10-15T14:51:33+03:00 — h002_generating

H002 запрос36/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 36,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:51:49+03:00 — h002_trial

H002 запрос36: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 36,
  "evaluated_distinct": 5,
  "trial": {
    "call": 36,
    "proposal": 15,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_036",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 374,
    "llm_seconds": 15.498338132,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "elapsed_seconds": 15.550237174000358
  }
}
```

## 2026-10-15T14:51:50+03:00 — h002_generating

H002 запрос37/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 37,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:52:06+03:00 — h002_trial

H002 запрос37: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 37,
  "evaluated_distinct": 5,
  "trial": {
    "call": 37,
    "proposal": 15,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_037",
    "parent_call": 36,
    "prompt_tokens": 1605,
    "generated_tokens": 374,
    "llm_seconds": 15.329918427,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "elapsed_seconds": 15.393024156001047
  }
}
```

## 2026-10-15T14:52:06+03:00 — h002_generating

H002 запрос38/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 38,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:52:23+03:00 — h002_trial

H002 запрос38: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 38,
  "evaluated_distinct": 5,
  "trial": {
    "call": 38,
    "proposal": 15,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_038",
    "parent_call": 37,
    "prompt_tokens": 1605,
    "generated_tokens": 374,
    "llm_seconds": 15.033861804,
    "status": "rejected",
    "error": "Invalid grouping keys",
    "elapsed_seconds": 15.091258722999555
  }
}
```

## 2026-10-15T14:52:23+03:00 — h002_generating

H002 запрос39/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 39,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:52:44+03:00 — h002_trial

H002 запрос39: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 39,
  "evaluated_distinct": 5,
  "trial": {
    "call": 39,
    "proposal": 16,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_039",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 415,
    "llm_seconds": 17.478129477,
    "program_sha256": "a31ab50ea24c4281021f24dba74c536ab05764519761181fb8882fd54662b0dc",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"days_ago\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.f_avg_days_ago\", \"unnamed_subquery.raw_u_age\", \"unnamed_subquery.raw_i_index_group_no\", \"unnamed_subquery.raw_i_garment_group_no\", \"unnamed_subquery.raw_u_active\"",
    "elapsed_seconds": 19.821644376999757
  }
}
```

## 2026-10-15T14:52:44+03:00 — h002_generating

H002 запрос40/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 40,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:53:04+03:00 — h002_trial

H002 запрос40: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 40,
  "evaluated_distinct": 5,
  "trial": {
    "call": 40,
    "proposal": 16,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_040",
    "parent_call": 39,
    "prompt_tokens": 1716,
    "generated_tokens": 420,
    "llm_seconds": 18.536547617,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 18.60408442699918
  }
}
```

## 2026-10-15T14:53:04+03:00 — h002_generating

H002 запрос41/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 41,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:53:24+03:00 — h002_trial

H002 запрос41: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 41,
  "evaluated_distinct": 5,
  "trial": {
    "call": 41,
    "proposal": 16,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_041",
    "parent_call": 40,
    "prompt_tokens": 1660,
    "generated_tokens": 424,
    "llm_seconds": 17.874212533,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 17.940174714000023
  }
}
```

## 2026-10-15T14:53:24+03:00 — h002_generating

H002 запрос42/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 42,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:53:41+03:00 — h002_trial

H002 запрос42: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 42,
  "evaluated_distinct": 5,
  "trial": {
    "call": 42,
    "proposal": 17,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_042",
    "parent_call": null,
    "prompt_tokens": 1512,
    "generated_tokens": 346,
    "llm_seconds": 15.37441443,
    "program_sha256": "946aa6b3230fede0fdecfdab2945998f1bd835f374e06c755d0d92ce20b787ce",
    "status": "rejected",
    "error": "Parser Error: syntax error at or near \"AS\"",
    "elapsed_seconds": 16.028668697001194
  }
}
```

## 2026-10-15T14:53:42+03:00 — h002_generating

H002 запрос43/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 43,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:53:59+03:00 — h002_trial

H002 запрос43: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 43,
  "evaluated_distinct": 5,
  "trial": {
    "call": 43,
    "proposal": 17,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_043",
    "parent_call": 42,
    "prompt_tokens": 1585,
    "generated_tokens": 346,
    "llm_seconds": 15.451263014,
    "program_sha256": "946aa6b3230fede0fdecfdab2945998f1bd835f374e06c755d0d92ce20b787ce",
    "status": "rejected",
    "error": "Parser Error: syntax error at or near \"AS\"",
    "elapsed_seconds": 16.139252783999837
  }
}
```

## 2026-10-15T14:53:59+03:00 — h002_generating

H002 запрос44/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 44,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:54:17+03:00 — h002_trial

H002 запрос44: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 44,
  "evaluated_distinct": 5,
  "trial": {
    "call": 44,
    "proposal": 17,
    "island": 2,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_044",
    "parent_call": 43,
    "prompt_tokens": 1585,
    "generated_tokens": 346,
    "llm_seconds": 15.681787191,
    "program_sha256": "946aa6b3230fede0fdecfdab2945998f1bd835f374e06c755d0d92ce20b787ce",
    "status": "rejected",
    "error": "Parser Error: syntax error at or near \"AS\"",
    "elapsed_seconds": 16.272215668999706
  }
}
```

## 2026-10-15T14:54:17+03:00 — h002_generating

H002 запрос45/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 45,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:54:26+03:00 — h002_trial

H002 запрос45: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 45,
  "evaluated_distinct": 5,
  "trial": {
    "call": 45,
    "proposal": 18,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_045",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 91,
    "llm_seconds": 4.265986405,
    "program_sha256": "e72a833cdf5a8a5d3c0a9b3451f745ec781913363af41b1a9a93953351109bf6",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"price\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.rid\", \"unnamed_subquery.f_article_sales_count\", \"unnamed_subquery.raw_i_section_no\", \"unnamed_subquery.raw_i_product_code\", \"unnamed_subquery.raw_i_perceived_colour_value_id\"",
    "elapsed_seconds": 7.4119564140000875
  }
}
```

## 2026-10-15T14:54:26+03:00 — h002_generating

H002 запрос46/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 46,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:54:36+03:00 — h002_trial

H002 запрос46: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 46,
  "evaluated_distinct": 5,
  "trial": {
    "call": 46,
    "proposal": 18,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_046",
    "parent_call": 45,
    "prompt_tokens": 1388,
    "generated_tokens": 194,
    "llm_seconds": 8.503862438,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 8.567035076999673
  }
}
```

## 2026-10-15T14:54:36+03:00 — h002_generating

H002 запрос47/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 47,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:54:47+03:00 — h002_trial

H002 запрос47: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 47,
  "evaluated_distinct": 5,
  "trial": {
    "call": 47,
    "proposal": 18,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_047",
    "parent_call": 46,
    "prompt_tokens": 1434,
    "generated_tokens": 226,
    "llm_seconds": 9.560043745,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 9.621956513999976
  }
}
```

## 2026-10-15T14:54:47+03:00 — h002_generating

H002 запрос48/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 48,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:55:11+03:00 — h002_trial

H002 запрос48: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 48,
  "evaluated_distinct": 5,
  "trial": {
    "call": 48,
    "proposal": 19,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_048",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 521,
    "llm_seconds": 22.066199798,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 22.128172792999976
  }
}
```

## 2026-10-15T14:55:11+03:00 — h002_generating

H002 запрос49/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 49,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:55:36+03:00 — h002_trial

H002 запрос49: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 49,
  "evaluated_distinct": 5,
  "trial": {
    "call": 49,
    "proposal": 19,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_049",
    "parent_call": 48,
    "prompt_tokens": 1771,
    "generated_tokens": 521,
    "llm_seconds": 23.132223551,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 23.19392733099994
  }
}
```

## 2026-10-15T14:55:36+03:00 — h002_generating

H002 запрос50/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 50,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:55:59+03:00 — h002_trial

H002 запрос50: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 50,
  "evaluated_distinct": 5,
  "trial": {
    "call": 50,
    "proposal": 19,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_050",
    "parent_call": 49,
    "prompt_tokens": 1771,
    "generated_tokens": 483,
    "llm_seconds": 21.753310801,
    "status": "rejected",
    "error": "Forbidden token 'SELECT': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 21.808939900998666
  }
}
```

## 2026-10-15T14:55:59+03:00 — h002_generating

H002 запрос51/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 51,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:56:13+03:00 — h002_trial

H002 запрос51: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 51,
  "evaluated_distinct": 5,
  "trial": {
    "call": 51,
    "proposal": 20,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_051",
    "parent_call": null,
    "prompt_tokens": 1512,
    "generated_tokens": 194,
    "llm_seconds": 9.31237282,
    "program_sha256": "3a22226371300cfd52c28cabad7598b1206d3fe3802b9b47f7602c4e9fea1170",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"f_avg_days_since_product_purchase\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.f_max_days_since_product_purchase\", \"unnamed_subquery.f_avg_product_price\", \"unnamed_subquery.raw_i_perceived_colour_value_id\", \"unnamed_subquery.raw_i_perceived_colour_master_id\", \"unnamed_subquery.f_unique_customer_products\"",
    "elapsed_seconds": 12.097269783000229
  }
}
```

## 2026-10-15T14:56:13+03:00 — h002_generating

H002 запрос52/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 52,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:56:26+03:00 — h002_trial

H002 запрос52: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 52,
  "evaluated_distinct": 5,
  "trial": {
    "call": 52,
    "proposal": 20,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_052",
    "parent_call": 51,
    "prompt_tokens": 1503,
    "generated_tokens": 198,
    "llm_seconds": 9.223979001,
    "program_sha256": "eebf20b9e1204f66422991a076a27637066f6a505c994d76e8d4bf52922dfbd4",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"raw_i_price\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.raw_i_product_code\", \"unnamed_subquery.raw_i_product_type_no\", \"unnamed_subquery.raw_i_graphical_appearance_no\", \"unnamed_subquery.raw_i_section_no\", \"unnamed_subquery.raw_u_active\"",
    "elapsed_seconds": 11.778472960000727
  }
}
```

## 2026-10-15T14:56:26+03:00 — h002_generating

H002 запрос53/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 53,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:56:39+03:00 — h002_trial

H002 запрос53: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 53,
  "evaluated_distinct": 5,
  "trial": {
    "call": 53,
    "proposal": 20,
    "island": 2,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_053",
    "parent_call": 52,
    "prompt_tokens": 1499,
    "generated_tokens": 204,
    "llm_seconds": 9.001558235,
    "program_sha256": "2e3b045b97ff4ac4d65d57c3fcbf83a6eee2728e4eb175d547cad2614d4cc149",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"raw_i_price\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.raw_i_product_code\", \"unnamed_subquery.raw_i_product_type_no\", \"unnamed_subquery.raw_i_graphical_appearance_no\", \"unnamed_subquery.raw_i_section_no\", \"unnamed_subquery.raw_u_active\"",
    "elapsed_seconds": 11.505222879999565
  }
}
```

## 2026-10-15T14:56:39+03:00 — h002_generating

H002 запрос54/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 54,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:56:53+03:00 — h002_trial

H002 запрос54: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 54,
  "evaluated_distinct": 5,
  "trial": {
    "call": 54,
    "proposal": 21,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_054",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 265,
    "llm_seconds": 11.776868875,
    "program_sha256": "7ae1d02723443e1febde882d274b645efccacdeace0d37dae60ade03234325e3",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"raw_i_product_code\" not found in FROM clause!\nCandidate bindings: \"history.product_code\", \"history.perceived_colour_master_id\", \"history.colour_group_code\", \"history.perceived_colour_value_id\", \"history.product_type_no\"\nLINE 1: ...r_purchase_count,approx_count_distinct(raw_i_product_code) AS f_customer_uniqu...\n                                                  ^",
    "elapsed_seconds": 12.395580950000294
  }
}
```

## 2026-10-15T14:56:53+03:00 — h002_generating

H002 запрос55/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 55,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:57:07+03:00 — h002_trial

H002 запрос55: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 55,
  "evaluated_distinct": 5,
  "trial": {
    "call": 55,
    "proposal": 21,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_055",
    "parent_call": 54,
    "prompt_tokens": 1574,
    "generated_tokens": 269,
    "llm_seconds": 12.231707081,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 12.294947716000024
  }
}
```

## 2026-10-15T14:57:07+03:00 — h002_generating

H002 запрос56/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 56,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:57:23+03:00 — h002_trial

H002 запрос56: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 56,
  "evaluated_distinct": 5,
  "trial": {
    "call": 56,
    "proposal": 21,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_056",
    "parent_call": 55,
    "prompt_tokens": 1509,
    "generated_tokens": 269,
    "llm_seconds": 13.579258783,
    "status": "rejected",
    "error": "Only numeric SQL expressions, no statements/strings/qualified names",
    "elapsed_seconds": 13.653895290000946
  }
}
```

## 2026-10-15T14:57:23+03:00 — h002_generating

H002 запрос57/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 57,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:57:40+03:00 — h002_trial

H002 запрос57: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 57,
  "evaluated_distinct": 5,
  "trial": {
    "call": 57,
    "proposal": 22,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_057",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 317,
    "llm_seconds": 15.993506496,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 16.07310933000008
  }
}
```

## 2026-10-15T14:57:40+03:00 — h002_generating

H002 запрос58/100, оценено5/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 58,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:57:56+03:00 — h002_trial

H002 запрос58: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 58,
  "evaluated_distinct": 5,
  "trial": {
    "call": 58,
    "proposal": 22,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_058",
    "parent_call": 57,
    "prompt_tokens": 1567,
    "generated_tokens": 311,
    "llm_seconds": 13.901284297,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 13.964141484999345
  }
}
```

## 2026-10-15T14:57:56+03:00 — h002_generating

H002 запрос59/100, оценено5/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 59,
  "evaluated_distinct": 5
}
```

## 2026-10-15T14:58:11+03:00 — h002_trial

H002 запрос59: rejected; различных оценённых5/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 59,
  "evaluated_distinct": 5,
  "trial": {
    "call": 59,
    "proposal": 22,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_059",
    "parent_call": 58,
    "prompt_tokens": 1561,
    "generated_tokens": 311,
    "llm_seconds": 13.577262757,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 13.663568644000406
  }
}
```

## 2026-10-15T14:58:11+03:00 — h002_generating

H002 запрос60/100, оценено5/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 60,
  "evaluated_distinct": 5
}
```

## 2026-10-15T15:01:07+03:00 — h002_trial

H002 запрос60: valid; различных оценённых6/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 60,
  "evaluated_distinct": 6,
  "trial": {
    "call": 60,
    "proposal": 23,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_060",
    "parent_call": null,
    "prompt_tokens": 1512,
    "generated_tokens": 463,
    "llm_seconds": 20.706764215,
    "program_sha256": "6696a37051416488214c56da16dfa905a42035a541489b0695239f6b378481be",
    "status": "valid",
    "score": 0.020499733195045694,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "1c0a66276fe457a5ef1eb2730cc59fcc329f222593481efa75c3dadc4e633471",
      "program_sha256": "2b917a93c6e956a67c4fe7a5f67dca27a26409075888410926706a664d8bf2b9",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.020499733195045694
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.512057342999469,
      "elapsed_seconds": 142.91864698599966,
      "passed": true
    },
    "elapsed_seconds": 174.78177606200006
  }
}
```

## 2026-10-15T15:01:07+03:00 — h002_generating

H002 запрос61/100, оценено6/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 61,
  "evaluated_distinct": 6
}
```

## 2026-10-15T15:02:26+03:00 — h002_trial

H002 запрос61: valid; различных оценённых7/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 61,
  "evaluated_distinct": 7,
  "trial": {
    "call": 61,
    "proposal": 24,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_061",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 320,
    "llm_seconds": 13.096811912,
    "program_sha256": "e3eac4c180b1b142fdfe1fb9bd99cd42c0623b8cb9a63a62c2b786202f3d0ded",
    "status": "valid",
    "score": 0.011451005591630592,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "d001e2b24127eb323e11b0d22895b5a859d97bd6afbc74aabedf3570e2ef456c",
      "program_sha256": "601b713d933b3f8e2eb062ca9b2b8d0b4a54f63b3ac168338bd6205822847c4e",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.011451005591630592
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.590960104998885,
      "elapsed_seconds": 58.21717655900102,
      "passed": true
    },
    "elapsed_seconds": 77.84490290299982
  }
}
```

## 2026-10-15T15:02:26+03:00 — h002_generating

H002 запрос62/100, оценено7/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 62,
  "evaluated_distinct": 7
}
```

## 2026-10-15T15:02:40+03:00 — h002_trial

H002 запрос62: rejected; различных оценённых7/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 62,
  "evaluated_distinct": 7,
  "trial": {
    "call": 62,
    "proposal": 25,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_062",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 288,
    "llm_seconds": 12.15656123,
    "status": "rejected",
    "error": "Forbidden token 'OVER': IDs only in grouping keys/counts; no SQL statements, window functions, or labels",
    "elapsed_seconds": 12.203417090000585
  }
}
```

## 2026-10-15T15:02:40+03:00 — h002_generating

H002 запрос63/100, оценено7/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 63,
  "evaluated_distinct": 7
}
```

## 2026-10-15T15:05:13+03:00 — h002_trial

H002 запрос63: valid; различных оценённых8/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 63,
  "evaluated_distinct": 8,
  "trial": {
    "call": 63,
    "proposal": 25,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_063",
    "parent_call": 62,
    "prompt_tokens": 1538,
    "generated_tokens": 289,
    "llm_seconds": 12.740038794,
    "program_sha256": "28e2c886944ad4d211ca8fa9c54f2fc37e7abf17053930361aeb5c61cef234c5",
    "status": "valid",
    "score": 0.009929935515873015,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "0e48c3604667583a0979511dfcd08133d01afa17fd181b5a45486fdc775012aa",
      "program_sha256": "96e4c085a2065c9bcdaf9088c4e14ab6d46ecadaa9db304023e8dd256e046d00",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.009929935515873015
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.137843512000472,
      "elapsed_seconds": 127.07905445000142,
      "passed": true
    },
    "elapsed_seconds": 152.3509967250011
  }
}
```

## 2026-10-15T15:05:13+03:00 — h002_generating

H002 запрос64/100, оценено8/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 64,
  "evaluated_distinct": 8
}
```

## 2026-10-15T15:08:09+03:00 — h002_trial

H002 запрос64: valid; различных оценённых9/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 64,
  "evaluated_distinct": 9,
  "trial": {
    "call": 64,
    "proposal": 26,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_064",
    "parent_call": null,
    "prompt_tokens": 1717,
    "generated_tokens": 575,
    "llm_seconds": 23.627108578,
    "program_sha256": "a2f992c1fb8df01b1464effc051b1dd296d839d05078af626ba73f8cb8ca6bd8",
    "status": "valid",
    "score": 0.019582849514490137,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "071bef85681fab0da3220785bac9f83f0c2cb5872080dc2ec27efd78e7723f11",
      "program_sha256": "32e8b25a67cf14dbea01cf1d7ad1c818b5636c56d7a27fd8fd2ffe3b2ad3368f",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.019582849514490137
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.461819740999999,
      "elapsed_seconds": 140.6071476470006,
      "passed": true
    },
    "elapsed_seconds": 174.60711071399965
  }
}
```

## 2026-10-15T15:08:09+03:00 — h002_generating

H002 запрос65/100, оценено9/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 65,
  "evaluated_distinct": 9
}
```

## 2026-10-15T15:09:26+03:00 — h002_trial

H002 запрос65: valid; различных оценённых10/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 65,
  "evaluated_distinct": 10,
  "trial": {
    "call": 65,
    "proposal": 27,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_065",
    "parent_call": null,
    "prompt_tokens": 1473,
    "generated_tokens": 333,
    "llm_seconds": 13.795806915,
    "program_sha256": "bcbc54124f5309036e4592068430594c0da8ad8cb6920c68d54fc037750cbcd3",
    "status": "valid",
    "score": 0.012889591600529101,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "4a0db2e0826b9d7b18f8d8578602ed65a144d1633a9b23000f8e3df3bf95b9aa",
      "program_sha256": "55a37e113f7be6cf81541a6ec395b7903676ffe8c04efd7d880d69cc7bf275c7",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.012889591600529101
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.7845175700003892,
      "elapsed_seconds": 55.160935276999226,
      "passed": true
    },
    "elapsed_seconds": 75.37625546299932
  }
}
```

## 2026-10-15T15:09:26+03:00 — h002_generating

H002 запрос66/100, оценено10/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 66,
  "evaluated_distinct": 10
}
```

## 2026-10-15T15:12:27+03:00 — h002_trial

H002 запрос66: valid; различных оценённых11/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 66,
  "evaluated_distinct": 11,
  "trial": {
    "call": 66,
    "proposal": 28,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_066",
    "parent_call": null,
    "prompt_tokens": 1270,
    "generated_tokens": 308,
    "llm_seconds": 12.829103264,
    "program_sha256": "1c1c55948a1776217705cb439d5d486a44183fb2c90bb60831425d6770836221",
    "status": "valid",
    "score": 0.021201580537518035,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "de01460435985159abbfe55e190469f0d5caa8c96a3de3939fc4be4c634813d1",
      "program_sha256": "9abf392d5d63a9f22aca1790bdf8689083c83baef86cb2d716662fbbb474ad47",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.021201580537518035
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 5.250537501999133,
      "elapsed_seconds": 156.87035719599953,
      "passed": true
    },
    "elapsed_seconds": 180.59655597500023
  }
}
```

## 2026-10-15T15:12:27+03:00 — h002_generating

H002 запрос67/100, оценено11/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 67,
  "evaluated_distinct": 11
}
```

## 2026-10-15T15:15:12+03:00 — h002_trial

H002 запрос67: valid; различных оценённых12/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 67,
  "evaluated_distinct": 12,
  "trial": {
    "call": 67,
    "proposal": 29,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_067",
    "parent_call": null,
    "prompt_tokens": 1717,
    "generated_tokens": 629,
    "llm_seconds": 26.597388724,
    "program_sha256": "d1785bdb6e9cc87be02fd925443bcd710d27c0ae664fd27a154482945080f076",
    "status": "valid",
    "score": 0.020499733195045694,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "1c0a66276fe457a5ef1eb2730cc59fcc329f222593481efa75c3dadc4e633471",
      "program_sha256": "6c5a806084ea588c9e69b0330ddb9c1a04183299382a9c7b8c0405550640cfa4",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.020499733195045694
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 3.870906088999618,
      "elapsed_seconds": 126.82770727800016,
      "passed": true
    },
    "elapsed_seconds": 163.26281161699808
  }
}
```

## 2026-10-15T15:15:12+03:00 — h002_generating

H002 запрос68/100, оценено12/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 68,
  "evaluated_distinct": 12
}
```

## 2026-10-15T15:15:29+03:00 — h002_trial

H002 запрос68: duplicate; различных оценённых12/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 68,
  "evaluated_distinct": 12,
  "trial": {
    "call": 68,
    "proposal": 30,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_068",
    "parent_call": null,
    "prompt_tokens": 1517,
    "generated_tokens": 388,
    "llm_seconds": 15.676634704,
    "program_sha256": "bcbc54124f5309036e4592068430594c0da8ad8cb6920c68d54fc037750cbcd3",
    "status": "duplicate",
    "error": "Duplicate of an already evaluated feature set; propose distinct formulas",
    "elapsed_seconds": 15.731109706001007
  }
}
```

## 2026-10-15T15:15:29+03:00 — h002_generating

H002 запрос69/100, оценено12/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 69,
  "evaluated_distinct": 12
}
```

## 2026-10-15T15:15:50+03:00 — h002_trial

H002 запрос69: rejected; различных оценённых12/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 69,
  "evaluated_distinct": 12,
  "trial": {
    "call": 69,
    "proposal": 30,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_069",
    "parent_call": 68,
    "prompt_tokens": 1627,
    "generated_tokens": 467,
    "llm_seconds": 19.762173292,
    "program_sha256": "f880af40d07fc1b7a1c33ee5df04311b3a43e135d853e297d4e4154e0c17c3ce",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"raw_u_fashion_news_frequency\" not found in FROM clause!\nCandidate bindings: \"history.sales_channel_id\", \"history.graphical_appearance_no\", \"history.price\", \"history.index_group_no\", \"history.days_ago\"\nLINE 1: ...ND) AS f_recent_transactions_count,AVG(raw_u_fashion_news_frequency) AS f_fash...\n                                                  ^",
    "elapsed_seconds": 20.297343817001092
  }
}
```

## 2026-10-15T15:15:50+03:00 — h002_generating

H002 запрос70/100, оценено12/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 70,
  "evaluated_distinct": 12
}
```

## 2026-10-15T15:17:21+03:00 — h002_trial

H002 запрос70: valid; различных оценённых13/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 70,
  "evaluated_distinct": 13,
  "trial": {
    "call": 70,
    "proposal": 30,
    "island": 0,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_070",
    "parent_call": 69,
    "prompt_tokens": 1777,
    "generated_tokens": 429,
    "llm_seconds": 19.641339267,
    "program_sha256": "b06c331ca4fe751d9074eeb53731123c452b1fdc4a1bbbd3617bda254b38c07c",
    "status": "valid",
    "score": 0.01220216957521645,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "fcf8afafb17fa127ade06fca31462ac1aae8d4e2ed16f575253b34af27afd990",
      "program_sha256": "290550cbd56d92c6243330f1abb5222406e9c441114f243acc08856c64455fb2",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.01220216957521645
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.7265553799988993,
      "elapsed_seconds": 62.104935415998625,
      "passed": true
    },
    "elapsed_seconds": 88.972810776002
  }
}
```

## 2026-10-15T15:17:21+03:00 — h002_generating

H002 запрос71/100, оценено13/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 71,
  "evaluated_distinct": 13
}
```

## 2026-10-15T15:20:49+03:00 — h002_trial

H002 запрос71: valid; различных оценённых14/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 71,
  "evaluated_distinct": 14,
  "trial": {
    "call": 71,
    "proposal": 31,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_071",
    "parent_call": null,
    "prompt_tokens": 1562,
    "generated_tokens": 432,
    "llm_seconds": 19.074608102,
    "program_sha256": "2044182ad35da3f36b8ddb55e0d834c6590eb8a273b16aa5cd3d7c3ddc0543d4",
    "status": "valid",
    "score": 0.021201580537518035,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "de01460435985159abbfe55e190469f0d5caa8c96a3de3939fc4be4c634813d1",
      "program_sha256": "e32e27d26babeb4181cbceb4fc65aefdc7c9ffbb0913771da258910e558f4a9e",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.021201580537518035
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 6.924717279998731,
      "elapsed_seconds": 176.2416501080006,
      "passed": true
    },
    "elapsed_seconds": 206.2108263020018
  }
}
```

## 2026-10-15T15:20:49+03:00 — h002_generating

H002 запрос72/100, оценено14/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 72,
  "evaluated_distinct": 14
}
```

## 2026-10-15T15:21:07+03:00 — h002_trial

H002 запрос72: rejected; различных оценённых14/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 72,
  "evaluated_distinct": 14,
  "trial": {
    "call": 72,
    "proposal": 32,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_072",
    "parent_call": null,
    "prompt_tokens": 1717,
    "generated_tokens": 357,
    "llm_seconds": 16.062834964,
    "status": "rejected",
    "error": "Unknown feature keys",
    "elapsed_seconds": 16.13831977299924
  }
}
```

## 2026-10-15T15:21:07+03:00 — h002_generating

H002 запрос73/100, оценено14/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 73,
  "evaluated_distinct": 14
}
```

## 2026-10-15T15:21:31+03:00 — h002_trial

H002 запрос73: rejected; различных оценённых14/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 73,
  "evaluated_distinct": 14,
  "trial": {
    "call": 73,
    "proposal": 32,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_073",
    "parent_call": 72,
    "prompt_tokens": 1588,
    "generated_tokens": 404,
    "llm_seconds": 17.536535828,
    "program_sha256": "efb91e6aa4df25cc6f4bf2eeb60562fc36b4c813d7d2aa554f8fe1da07dd1043",
    "status": "rejected",
    "error": "Binder Error: Referenced column \"days_ago\" not found in FROM clause!\nCandidate bindings: \"unnamed_subquery.raw_u_age\", \"unnamed_subquery.f_product_avg_days_ago\", \"unnamed_subquery.raw_i_index_group_no\", \"unnamed_subquery.raw_i_garment_group_no\", \"unnamed_subquery.raw_u_active\"",
    "elapsed_seconds": 22.832577503999346
  }
}
```

## 2026-10-15T15:21:31+03:00 — h002_generating

H002 запрос74/100, оценено14/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 74,
  "evaluated_distinct": 14
}
```

## 2026-10-15T15:24:13+03:00 — h002_trial

H002 запрос74: valid; различных оценённых15/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 74,
  "evaluated_distinct": 15,
  "trial": {
    "call": 74,
    "proposal": 32,
    "island": 2,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_074",
    "parent_call": 73,
    "prompt_tokens": 1706,
    "generated_tokens": 407,
    "llm_seconds": 17.120685724,
    "program_sha256": "7de98ac337d1e679ee35e4121aef190f3cd55507687f270eb714e36aca232065",
    "status": "valid",
    "score": 0.020468167538480037,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "8904567f52a3dc46b9a98a982cb95a9157f9f35bfffb4bffd330b05486526381",
      "program_sha256": "e6e2df5837e6f3c316399019f3a9028183828a3a944cbc989d71443b9e8859a6",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.020468167538480037
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 3.9251409200005583,
      "elapsed_seconds": 131.78049844699854,
      "passed": true
    },
    "elapsed_seconds": 160.05521551100173
  }
}
```

## 2026-10-15T15:24:13+03:00 — h002_generating

H002 запрос75/100, оценено15/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 75,
  "evaluated_distinct": 15
}
```

## 2026-10-15T15:24:26+03:00 — h002_trial

H002 запрос75: duplicate; различных оценённых15/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 75,
  "evaluated_distinct": 15,
  "trial": {
    "call": 75,
    "proposal": 33,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_075",
    "parent_call": null,
    "prompt_tokens": 1517,
    "generated_tokens": 282,
    "llm_seconds": 11.591245535,
    "program_sha256": "bcbc54124f5309036e4592068430594c0da8ad8cb6920c68d54fc037750cbcd3",
    "status": "duplicate",
    "error": "Duplicate of an already evaluated feature set; propose distinct formulas",
    "elapsed_seconds": 11.638691018000827
  }
}
```

## 2026-10-15T15:24:26+03:00 — h002_generating

H002 запрос76/100, оценено15/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 76,
  "evaluated_distinct": 15
}
```

## 2026-10-15T15:24:53+03:00 — kaggle_notebook_prepared

Подготовлен.ipynb Llama3.1-8B дляT4, все803377 train пар, общий subset pool для трёх способов, CPU-проверки и smoke прошли. Llama/Kaggle не запускались.

Запуск: `hm_llmfe_llama31_8b_kaggle_fulltrain_v2`.

```json
{
  "status": "notebook_ready",
  "train_pairs": 803377,
  "scope": "notebook_prepared_and_CPU_checked_only",
  "local_validation_threads": 1,
  "behavioral_tests_passed": 6,
  "raw_xgboost_full_train_seconds": 71.95847935499842,
  "synthetic_quality_result": false,
  "llama_gpu_executed": false,
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "artifacts": "LLMFeatures/kaggle",
  "kaggle_t4_executed": false,
  "train_user_times": 50000,
  "raw_lightgbm_full_train_seconds": 35.21816100599972,
  "notebook": "LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb",
  "bundle": "LLMFeatures/kaggle/hm_llmfe_kaggle_fulltrain_v2.zip",
  "compare": "LLM-LightGBM/manual-LightGBM/GNN-LightGBM on exact same selected users and ID-GNN candidates; old tuning/seeds and graph pretraining differ",
  "synthetic_integration_passed": true,
  "paper_limit_deviation": "2GiB failed during full803377-pair XGBoost training; use4GiB and larger total timeout,30s per feature call",
  "original_pair_file_bit_identical": true,
  "cpu_evaluator_memory_gib": 4
}
```

## 2026-10-15T15:25:49+03:00 — h002_trial

H002 запрос76: valid; различных оценённых16/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 76,
  "evaluated_distinct": 16,
  "trial": {
    "call": 76,
    "proposal": 33,
    "island": 0,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_076",
    "parent_call": 75,
    "prompt_tokens": 1521,
    "generated_tokens": 321,
    "llm_seconds": 12.980922694,
    "program_sha256": "ae07c10f73412c66359bd55c544ef117033a954eacf5a1ad9381990c8f2b1c8c",
    "status": "valid",
    "score": 0.013090329447751323,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "e27ad1552d0d9a661c6f930860622fc496714be26d97cc235ba4037418945b40",
      "program_sha256": "3dbfc47c2527d4bf7fe4257c932cb72e3f9b750cca92e0aa4f74932b225153d4",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.013090329447751323
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 2.208388859999104,
      "elapsed_seconds": 62.05733383799816,
      "passed": true
    },
    "elapsed_seconds": 82.00331113900029
  }
}
```

## 2026-10-15T15:25:49+03:00 — h002_generating

H002 запрос77/100, оценено16/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 77,
  "evaluated_distinct": 16
}
```

## 2026-10-15T15:28:53+03:00 — h002_trial

H002 запрос77: valid; различных оценённых17/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 77,
  "evaluated_distinct": 17,
  "trial": {
    "call": 77,
    "proposal": 34,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_077",
    "parent_call": null,
    "prompt_tokens": 1562,
    "generated_tokens": 384,
    "llm_seconds": 16.513590703,
    "program_sha256": "813fc0aef1583e6eb95ccf3863546374456f24fcf143fc206798be19f971fda4",
    "status": "valid",
    "score": 0.020357495152417027,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "cb0b3e471fcf111e993d6bb71cd3a7811891831676eceaef9e2fcbab050331cb",
      "program_sha256": "1cd56f77e0647e281ba090b1b40c5a565ccbced805dc6bf4781bed3397fb0139",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.020357495152417027
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.799441893999756,
      "elapsed_seconds": 155.0480968209995,
      "passed": true
    },
    "elapsed_seconds": 182.67233746099737
  }
}
```

## 2026-10-15T15:28:53+03:00 — h002_generating

H002 запрос78/100, оценено17/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 78,
  "evaluated_distinct": 17
}
```

## 2026-10-15T15:29:16+03:00 — h002_trial

H002 запрос78: rejected; различных оценённых17/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 78,
  "evaluated_distinct": 17,
  "trial": {
    "call": 78,
    "proposal": 35,
    "island": 2,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_078",
    "parent_call": null,
    "prompt_tokens": 1717,
    "generated_tokens": 543,
    "llm_seconds": 21.564696819,
    "status": "rejected",
    "error": "Feature names must be unique f_lowercase_names",
    "elapsed_seconds": 21.62290798200047
  }
}
```

## 2026-10-15T15:29:16+03:00 — h002_generating

H002 запрос79/100, оценено17/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 79,
  "evaluated_distinct": 17
}
```

## 2026-10-15T15:31:52+03:00 — h002_trial

H002 запрос79: valid; различных оценённых18/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 79,
  "evaluated_distinct": 18,
  "trial": {
    "call": 79,
    "proposal": 35,
    "island": 2,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_079",
    "parent_call": 78,
    "prompt_tokens": 1779,
    "generated_tokens": 494,
    "llm_seconds": 19.847663031,
    "program_sha256": "7b91cb2ab5a3d5f7e2b3f9822cb1f4d86e299df162c53043772dc3fbb46878fc",
    "status": "valid",
    "score": 0.02017421236171236,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "9fe6343734c5e6ef7804596119ddee5dfb1397f043d975ca402739fbe0fb6216",
      "program_sha256": "90d69f1906f790460931f9176df1da93ab837a99c6974bed73be5618f8f21413",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.02017421236171236
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.3203956079996715,
      "elapsed_seconds": 124.25914229500268,
      "passed": true
    },
    "elapsed_seconds": 154.04495300000053
  }
}
```

## 2026-10-15T15:31:52+03:00 — h002_generating

H002 запрос80/100, оценено18/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 80,
  "evaluated_distinct": 18
}
```

## 2026-10-15T15:33:17+03:00 — h002_trial

H002 запрос80: valid; различных оценённых19/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 80,
  "evaluated_distinct": 19,
  "trial": {
    "call": 80,
    "proposal": 36,
    "island": 0,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_080",
    "parent_call": null,
    "prompt_tokens": 1575,
    "generated_tokens": 477,
    "llm_seconds": 19.907564424,
    "program_sha256": "6cfe3665ad7158647ada5b9e8d67aedfb46ab4506814ab5778ec78f7f97fb322",
    "status": "valid",
    "score": 0.013090329447751323,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "e27ad1552d0d9a661c6f930860622fc496714be26d97cc235ba4037418945b40",
      "program_sha256": "2ac354f1af97b0b29511d042334eba2838306bc011203d2e0334a1901656c1bf",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.013090329447751323
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 1.6502088950001053,
      "elapsed_seconds": 56.886731421996956,
      "passed": true
    },
    "elapsed_seconds": 83.65084179599944
  }
}
```

## 2026-10-15T15:33:17+03:00 — h002_generating

H002 запрос81/100, оценено19/20, исправление0

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 81,
  "evaluated_distinct": 19
}
```

## 2026-10-15T15:33:35+03:00 — h002_trial

H002 запрос81: duplicate; различных оценённых19/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 81,
  "evaluated_distinct": 19,
  "trial": {
    "call": 81,
    "proposal": 37,
    "island": 1,
    "repair": 0,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_081",
    "parent_call": null,
    "prompt_tokens": 1562,
    "generated_tokens": 419,
    "llm_seconds": 17.153951095,
    "program_sha256": "1c1c55948a1776217705cb439d5d486a44183fb2c90bb60831425d6770836221",
    "status": "duplicate",
    "error": "Duplicate of an already evaluated feature set; propose distinct formulas",
    "elapsed_seconds": 17.208226250000735
  }
}
```

## 2026-10-15T15:33:35+03:00 — h002_generating

H002 запрос82/100, оценено19/20, исправление1

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 82,
  "evaluated_distinct": 19
}
```

## 2026-10-15T15:33:54+03:00 — h002_trial

H002 запрос82: duplicate; различных оценённых19/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 82,
  "evaluated_distinct": 19,
  "trial": {
    "call": 82,
    "proposal": 37,
    "island": 1,
    "repair": 1,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_082",
    "parent_call": 81,
    "prompt_tokens": 1658,
    "generated_tokens": 419,
    "llm_seconds": 17.465761025,
    "program_sha256": "1c1c55948a1776217705cb439d5d486a44183fb2c90bb60831425d6770836221",
    "status": "duplicate",
    "error": "Duplicate of an already evaluated feature set; propose distinct formulas",
    "elapsed_seconds": 17.51849773199865
  }
}
```

## 2026-10-15T15:33:54+03:00 — h002_generating

H002 запрос83/100, оценено19/20, исправление2

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "generating",
  "llm_calls": 83,
  "evaluated_distinct": 19
}
```

## 2026-10-15T15:37:05+03:00 — h002_trial

H002 запрос83: valid; различных оценённых20/20

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "searching",
  "llm_calls": 83,
  "evaluated_distinct": 20,
  "trial": {
    "call": 83,
    "proposal": 37,
    "island": 1,
    "repair": 2,
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_083",
    "parent_call": 82,
    "prompt_tokens": 1658,
    "generated_tokens": 428,
    "llm_seconds": 17.886252933,
    "program_sha256": "743cc6b8cb1326a0bda2c0fe6dc908747729ac3bf3d45b5e9ba55a6350082b2a",
    "status": "valid",
    "score": 0.020224397997835496,
    "metrics": {
      "stage": "search",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "37f073d98535cb6a194bc3a910ee93c59423eb0f5dc19bd97e00554f5d8c872f",
      "program_sha256": "5218aad198aa03829930a702291be810438fed76236c7822bc731e5ef4afd855",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.020224397997835496
      },
      "val_users": 256,
      "val_pairs": 6594,
      "val_seconds": 4.804498387002241,
      "elapsed_seconds": 161.39359621300173,
      "passed": true
    },
    "elapsed_seconds": 189.36316617300326
  }
}
```

## 2026-10-15T15:37:40+03:00 — h002_selected

H002: признаки выбраны по confirmation; начата итоговая оценка на общих кандидатах

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "evaluating",
  "selection": {
    "directory": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/LLMFeatures/results/qwen25coder7b_seed42_h002_shared_v1/candidates/candidate_060",
    "score": 0.015164011568168934,
    "metrics": {
      "stage": "confirm",
      "protocol": "saved ID-GNN candidate pools",
      "smoke": false,
      "model_sha256": "1c0a66276fe457a5ef1eb2730cc59fcc329f222593481efa75c3dadc4e633471",
      "program_sha256": "2b917a93c6e956a67c4fe7a5f67dca27a26409075888410926706a664d8bf2b9",
      "prediction_threads": 8,
      "inference_from_saved_model": true,
      "val_metrics": {
        "map": 0.015164011568168934
      },
      "val_users": 1024,
      "val_pairs": 28587,
      "val_seconds": 3.9803579920007905,
      "elapsed_seconds": 5.461096573999384,
      "passed": true
    }
  }
}
```

## 2026-10-15T15:39:42+03:00 — h002_complete

H002 завершён: итоговые shared MAP, независимый полный повтор и графики сохранены

Запуск: `hm_llmfe_qwen25coder7b_seed42_h002_shared_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.017860457679790033
  },
  "test_metrics": {
    "map": 0.019753961287228266
  },
  "llm_calls": 83,
  "evaluated_distinct": 20,
  "target_met": true,
  "artifacts": "reports/llmfe_h002_shared_v1"
}
```

## 2026-10-15T15:51:47+03:00 — kaggle_model_source_config

В.ipynb добавлен MODEL_SOURCE unsloth/hf; defaultUnsloth анонимно, HF требуеттокен;7 тестов прошли. Данные и evaluator неизменны, GPUне запускался.

Запуск: `hm_llmfe_llama31_8b_kaggle_fulltrain_v2`.

```json
{
  "status": "notebook_ready",
  "model_sources": {
    "unsloth": "unsloth/Meta-Llama-3.1-8B-Instruct",
    "hf": "meta-llama/Llama-3.1-8B-Instruct"
  },
  "default_source": "unsloth",
  "tests_passed": 7,
  "weights_downloaded": false,
  "artifacts": "LLMFeatures/kaggle"
}
```

## 2026-10-15T16:14:09+03:00 — kaggle_lightgbm_search_v3

По прямому указанию весь Kaggle-поиск/confirmation переведён сXGBoost наLightGBM. Новый v3 notebook, v2 архивирован.8 тестов,803377-парный4-thread контроль и smoke прошли. Kaggle/GPUзапуск не выполнен.

Запуск: `hm_llmfe_llama31_8b_lightgbm_fulltrain_v3`.

```json
{
  "status": "notebook_ready",
  "notebook": "LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb",
  "tests_passed": 8,
  "cpu_threads": 4,
  "full_train_pairs": 803377,
  "search_backend": "lightgbm",
  "previous_xgboost_archived": "LLMFeatures/kaggle/archive/xgboost_v2",
  "archive_data_unchanged": true,
  "gpu_llama_tested": false,
  "full_train_reload_search_seconds": 22.927927161003026,
  "protocol": "hm_llmfe_llama31_8b_lightgbm_fulltrain_v3",
  "synthetic_end_to_end_passed": true
}
```

## 2026-10-15T16:46:20+03:00 — kaggle_repair_budget_v4

По указанию пользователя Kaggle v4: цель20 оценённых различных наборов, максимум300LLMобращений включая до3 исправлений.11 тестов и синтетический циклLightGBM прошли;LLama здесьне запускалась.

Запуск: `hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4`.

```json
{
  "status": "notebook_ready",
  "synthetic_distinct_sets": 2,
  "tests_passed": 11,
  "synthetic_calls": 6,
  "target_successful_distinct": 20,
  "synthetic_integration_passed": true,
  "dataset_unchanged": true,
  "max_llm_calls": 300,
  "gpu_llama_executed": false,
  "notebook": "LLMFeatures/kaggle/llmfe_llama31_hm_kaggle_t4.ipynb",
  "artifacts": "LLMFeatures/kaggle",
  "max_repairs_per_proposal": 3,
  "protocol": "hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4"
}
```

## 2026-10-15T20:00:33+03:00 — kaggle_zero_success_report

Пользователь сообщает0 успешных после83LLMвызовов Kaggle v4; error не предоставлен. Запрошены trial.error и response.tokens/truncated. Подготовлена read-only диагностика, параметры не менялись.

Запуск: `hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4`.

```json
{
  "remote_reported_calls": 83,
  "remote_reported_successes": 0,
  "cause_verified": false,
  "diagnostic": "LLMFeatures/kaggle/diagnose_failures.py"
}
```

## 2026-10-15T20:03:02+03:00 — kaggle_background_rejection_logging

Учтён Save Version: error,stage,tokens,truncated теперь печатаются в stdout;11 тестов прошли. Причина удалённых отказов пока неизвестна.

Запуск: `hm_llmfe_llama31_8b_lightgbm_repair_fulltrain_v4`.

```json
{
  "diagnostic_logging": true,
  "tests_passed": 11,
  "remote_cause_verified": false,
  "artifacts": "LLMFeatures/kaggle"
}
```

## 2026-10-15T20:28:19+03:00 — kaggle_v3_real_run_audited

ПрисланныйKaggle v3 проверен:20/20 отказов,0 LLMмоделей,выбранrawcontrol; егоMAPнельзяназыватьLLMрезультатом. Отчёт/гистограмма/неизменённыйCPUreplay сохранены.

Запуск: `hm_llmfe_llama31_8b_lightgbm_fulltrain_v3_3b338cf1f141`.

```json
{
  "status": "audited_no_llm_result",
  "artifacts": "reports/kaggle_llama_v3_audit",
  "llm_calls": 20,
  "evaluated_distinct": 0,
  "source": "user exported notebook and artifacts"
}
```

## 2026-10-15T20:28:19+03:00 — kaggle_pandas_contract_v5

Подготовленv5:короткиепрограммы,historyexamples,preflightперед803377-парнымfit,адресныеошибки,rawfallbackбезLLMподписи.13тестов+syntheticreplayпрошли;успехнастоящейLLamaнеизмерен.

Запуск: `hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5`.

```json
{
  "status": "notebook_ready",
  "artifacts": "LLMFeatures/kaggle",
  "tests_passed": 13,
  "target_successful_distinct": 20,
  "max_llm_calls": 300,
  "max_repairs_per_proposal": 3,
  "real_llama_generation_tested": false
}
```

## 2026-10-15T21:00:57+03:00 — kaggle_v5_first_candidate_received

Received tempRes partial export: call1 proposal1 island0 repair0 VALID, search MAP@12=1.0144412878787878% on256 users/6594 pairs; preflight passed,4 generated features,15 raw fields. Program SHA256 verified against trial. Generation36s, search38.66s, total79.47s. No model/predictions/raw-control metrics supplied: no independent metric replay or improvement claim. Remote current progress unknown beyond exported call1.

Запуск: `hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef`.

```json
{
  "status": "partial_export_received"
}
```

## 2026-10-15T21:15:01+03:00 — kaggle_sql_notebook_ready

Separate Llama SQL notebook ready: local Qwen-style JSON aggregates<=24 and derived<=12 after user explicitly requested derived formulas. Same803377 train pairs and256/512/1024/2048 evaluation users, LightGBM150/31 seed42,3islands,target20/max300/3repairs,hf-or-unsloth. Original pandas notebook preserved. Six interface tests passed; synthetic repair/duplicate/resume/final replay passed; SQL fixture full803377 training32.15s and independent heldout-val model replay passed. Initial test mistakenly requested unsupported replay_search; corrected to val/replay_val and passed without retraining. Artifacts: LLMFeatures/kaggle/llmfe_llama31_hm_sql_kaggle_t4.ipynb and reports/kaggle_llmfe_validation/sql_v1_derived. No real Llama generation or quality measured.

Запуск: `hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-15T21:46:46+03:00 — kaggle_sql_stopped_by_user

User stopped SQL notebook after repeated failures. Supplied calls1-3 of proposal1 were rejected at parse_and_validate: raw_u_active, then raw_u_fn, then raw_u_active incorrectly used inside history aggregates. Other visible issues: invalid sales_channel_id grouping keys, nested AVG(COUNT), missing derived references, unsupported percentile syntax, MAX used for most-recent recency. No valid sets in supplied fragment; final total call count and full-run artifacts not provided. This does not establish Llama feature quality.

Запуск: `hm_llmfe_llama31_8b_lightgbm_sql_fulltrain_v1_6eb8a9ef9ba7`.

```json
{
  "status": "stopped_by_user"
}
```

## 2026-10-15T21:47:15+03:00 — kaggle_structured_notebook_ready

Created separate llmfe_llama31_hm_structured_kaggle_t4.ipynb after user approved structured feature descriptions. Llama selects aggregate op/column/window/keys and bounded derived expression trees; host compiles SQL, no model-authored SQL/Python. Maximum24 aggregates/12 derived; prompt recommends compact sets. Validator collects multiple schema errors per repair. Ordinary JSON sampling, not grammar/token masking. Same803377 pairs,LightGBM150/31 seed42,3islands,20 measured/300calls/3repairs,unchanged256/512/1024/2048 shared candidate users,model source hf/unsloth. Seven tests passed; synthetic search/repair/duplicate/resume/final replay passed; full803377-pair test-fixture fit/search24.82s and independent val replay passed. Previous notebooks unchanged. Real Llama generation not run, no quality result. Verification reports/kaggle_llmfe_validation/structured_v1/verification.json.

Запуск: `hm_llmfe_llama31_8b_lightgbm_structured_fulltrain_v1`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-15T22:34:09+03:00 — kaggle_structured_remote_failures

User supplied structured notebook log:7 completed calls rejected at parse_and_validate,0 measured sets,call8 started. Invalid grouping keys, invalid aggregate columns, unknown derived references, duplicate/invalid names and operation arity; all visible truncated=false. Full response.json/prompt.txt/run_config absent, so exact bad key values and actual source/revision cannot be independently checked. Re-read paper appendixB.1 and official specs/specification_balance-scale.txt: authors seed evolution with real nonempty transformation (weight_difference), while our memory starts raw-only; paper uses Python on flat supervised tables, custom structured DSL is our adaptation. Seven software tests/synthetic pipeline never established real Llama compliance. No further model training or notebook change made in this diagnostic turn.

## 2026-10-15T22:48:30+03:00 — balance_scale_diagnostic_ready

Prepared standalone llmfe_llama31_balance_scale_diagnostic_t4.ipynb after user approved diagnostic on authors original task. Embedded625-row dataset, exact initial weight_difference function, domain prompt files and MIT license pinned to upstream e9a58ca3416ae74dcc7549dffdf79b9289604091. Reconstructed prompt and fixed10 train examples, not exact original-server reproduction. Same configurable hf/unsloth NF4/FP16 load; user must choose matching model/revision. Six calls:3chat/3completion,seeds42/43/44,no repairs/evolution. XGBoost3.0.5 CPU4fold CV on500 train of outerfold1,125 heldout never evaluated. Four tests plus synthetic six-response pipeline/rejections/source extraction/CV/report/resume passed. Test fixture rawCV=.870,authors-seedCV=.862,known hand-coded torque fixtureCV=1.0; these are NOT Llama results. Real GPU/Llama not run here, notebook_ready only. Verification reports/kaggle_llmfe_validation/balance_diagnostic_v1_synthetic/verification.json. H&M notebook/results unchanged.

Запуск: `balance_scale_llama31_diagnostic_v1`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-15T22:49:57+03:00 — structured_chain_config_audited

Received user structured run_config, first prompt, first response and repair. All4 runtime SHA256 match delivered modules. Confirmed model meta-llama/Llama-3.1-8B-Instruct hf revision0e9e39f249a16976918f6564b8830bc894c89659 onT4 NF4/FP16,temperature.8. No visible config mismatch; cannot infer intact weight execution or quantization effects from config alone. First response19aggregates:7 invalid keys,12 schema-valid;2 derived failures cascade from rejected aggregates. Repair retains invalid keys, removes valid revenue aggregates yet keeps references. Static age_diff/age_ratio are redundant0/1 when age nonmissing. Full-set rejection discards valid subset by design; subset salvage not implemented or evaluated. Diagnostic balance notebook defaults now match user hf/revision, unsloth choice retained;4 unit checks passed without retraining. Actual diagnostic run fingerprints include selected source/revision. No real Llama evaluation performed locally.

Запуск: `balance_scale_llama31_diagnostic_v1`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-15T23:20:46+03:00 — balance_diagnostic_remote_control_failed

User Save Version log confirms balance_scale_llama31_diagnostic_v1_09de7191636d stopped in raw control before any Llama request/model load. XGBClassifier device=cpu reached CUDA code during fit/eval and raised cudaErrorNoDevice in CUDA-hidden worker. GPU T4 was detected by parent. Package dependency/debugger warnings were not the stopping exception. Local prior checks used xgboost-cpu while notebook installed full xgboost distribution; mismatch identified. Remote data/program compliance cannot be assessed:0 LLM calls.

Запуск: `balance_scale_llama31_diagnostic_v1_09de7191636d`.

```json
{
  "status": "failed_before_llm"
}
```

## 2026-10-15T23:20:48+03:00 — balance_diagnostic_cpu_fix_ready

Prepared balance_scale_llama31_diagnostic_v2_cpu in same .ipynb; archived v1 under balance_diagnostic/archive/v1. Installer uninstalls both conflicting distributions then pins xgboost-cpu3.0.5, worker asserts USE_CUDA=false, CPU build info stored in metrics. Llama remains hf/pinned revision/NF4/FP16 on T4,6 calls and task unchanged. Failure ZIP added around control evaluation and model load. Five unit tests passed including pre-generation failure archive; new synthetic6call integration with real CPU XGBoost/CV/report/resume passed; no real Llama/T4 run. Verification reports/kaggle_llmfe_validation/balance_diagnostic_v2_cpu_synthetic/verification.json. User needs updated .ipynb and a new Save Version.

Запуск: `balance_scale_llama31_diagnostic_v2_cpu`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-15T23:52:44+03:00 — balance_diagnostic_real_run_audited

Real Kaggle diagnostic ZIP received and audited: config fingerprint6b5c7786f4b5 and2runtime hashes match. Official Llama hf revision0e9e39f249a16976918f6564b8830bc894c89659,NF4/FP16,T4. Chat3/3 valid:train-only4fold CV accuracy81.4%,91.8%,96.8%; raw87%,authorsseed86.2%. Independent bounded CPU replay of all3 matched every fold exactly. Completion0/3accepted:all2048token truncated; first complete function prefixes parse but followed by additional versions/repetitions, not evaluated separately. Seed44 independently generated left/right weight*distance features.3draws cannot prove general reliability or rule out quantization effects; H&M used chat already. No heldout/H&M evaluation, no paper reproduction. Original ZIP unchanged. Artifacts reports/balance_scale_llama31_diagnostic_v2_audit/report.md and audit.json.

Запуск: `balance_scale_llama31_diagnostic_v2_cpu_6b5c7786f4b5`.

```json
{
  "status": "diagnostic_complete"
}
```

## 2026-10-16T00:17:53+03:00 — hm_flat_notebook_ready

Prepared independent llmfe_llama31_hm_flat_kaggle_t4.ipynb after user approved flat-table Python experiment.30 base columns=15raw+15fixed human past180d aggregates, generated once per52 training snapshots; original803377 pair rows/labels/order verified unchanged. Controls Raw15/Prepared30/Seeded32(two human log transforms), real seed score/code provided to3island memory; Llama only rowwise modify_features(X), additions/removals allowed.20 AST-distinct measured/300calls/3repairs; no-success after6calls pilot gate produces failure ZIP. Same256/512/1024/2048 candidate users,LightGBM150/31/seed42/4threads. Official hf pinned0e9e39f249a16976918f6564b8830bc894c89659/NF4FP16/chat,unsloth option retained. Four unit checks and synthetic search/repair/duplicate/confirmation/final/replay/resume passed; batch-dependent feature rejected before fit. Full803377 fits and independent val model replay passed for Raw15,Prepared30,Seeded32 and test fixture; cached scoring fits~16-17s locally. Raw15 valMAP.010268722027755231 matches previous Kaggle raw control exactly. Graphs visually checked,hand-feature origins explicit. DuckDB1.4.1 pinned for clean Kaggle setup; source data ZIP unchanged. Real Llama not run, no new LLM quality result. Artifacts LLMFeatures/kaggle/flat_variant and reports/kaggle_llmfe_validation/flat_v1/verification.json.

Запуск: `hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1`.

```json
{
  "status": "notebook_ready"
}
```

## 2026-10-16T09:54:57+03:00 — hm_flat_real_run_audited

Реальный flat эксперимент проверен:20 наборов за23 обращения,3 отказа; выбран candidate003. LLM test MAP0.800949%,Prepared30 0.737375%,Seeded32 0.723351%,Raw15 0.713138%, manual126 1.862883%,GNN→LGBM1.680568%,ID-GNN2.254944% на общих2048 test пользователях. 20 candidate model/program SHA и7 runtime SHA совпали. Независимый replay4 моделей×val/test точно совпал. Парный bootstrap10k:LLM−Prepared30+.063574п.п.,95%[+.010718;+.127851]; к Raw15 интервал пересекает0. Raw15 лучше LLM на val. Качество существенно ниже manual/GNN; не полный каталог/не полный test. Выбранные4 LLM ratio поверх30base+2ручныхseedlog. flat_manifest отсутствует вZIP; исходныйbundle и код проверены, локальный кэш дал те же предсказания. Оригинальный архив не изменён.

Запуск: `hm_llmfe_llama31_8b_lightgbm_flat_fulltrain_v1_aa1ed17300ae`.

```json
{
  "status": "complete",
  "artifacts": "reports/hm_llmfe_flat_v1_audit",
  "val_metrics": {
    "map": 0.0074474111229482,
    "users": 1024,
    "scope": "shared candidate subset"
  },
  "test_metrics": {
    "map": 0.0080094885447668,
    "users": 2048,
    "scope": "shared candidate subset"
  },
  "llm_calls": 23,
  "evaluated_distinct": 20,
  "rejected": 3,
  "selected_candidate": 3,
  "independent_frozen_replay": true,
  "full_catalog": false,
  "paper_reproduction": false
}
```

## 2026-10-16T10:02:46+03:00 — hm_llama_v5_semantic_audit

Получен итог v5 из features-llama-plus-lightgbm-v3.ipynb:20 технически оценённых программ за154 calls,134 отказа. Выбран candidate151, valMAP0.977301%,test0.734573% на общих1024/2048 пользователях. Но обнаружено неверное pandas-сопоставление: groupby Series поarticle_id/customer_id присвоены вRangeIndex F безmap/reindex по ID. Перестановка/разбиение128пар меняют признаки;mean_price неверен у70/128, customer-признаки у52/128. Такой probe провалили кандидаты56,131,147,151. 20 model/program SHA и2 runtimeSHA совпали, независимый replay Raw/selected×val/test точный. Метрики воспроизводимы, но не означают правильные исторические признаки. Никакого ремонта/переобучения или нового выбора поtest не было; исходники/ZIP неизменны. Flat запуск20/23 иtest0.800949% остаётся отдельным экспериментом.

Запуск: `hm_llmfe_llama31_8b_lightgbm_preflight_fulltrain_v5_949add5c4fef`.

```json
{
  "status": "complete_with_alignment_bug",
  "artifacts": "reports/hm_llmfe_llama_v5_audit",
  "val_metrics": {
    "map": 0.0097730073474702,
    "users": 1024,
    "scope": "shared subset; feature alignment bug"
  },
  "test_metrics": {
    "map": 0.0073457346945709,
    "users": 2048,
    "scope": "shared subset; feature alignment bug"
  },
  "llm_calls": 154,
  "evaluated_distinct": 20,
  "rejected": 134,
  "selected_candidate": 151,
  "chosen_feature_semantics_valid": false,
  "independent_frozen_replay": true,
  "full_catalog": false
}
```

## 2026-10-16T10:25:47+03:00 — contextgnn_review

Прочитаны ContextGNN arXiv2411.19513 PDF и официальный репозиторий. Уже проверен на H&M user-item-purchase: val/test3.00%/2.93% против pairwise2.64%/2.81%. Подход напрямую применим: локальные scores и глобальная RHS-embedding ветвь. API1.1.0, VRAM6GB, полный каталог и отдельная гипотеза ContextGNN→дерево описаны в reports/contextgnn_assessment.md. Новых запусков и установки библиотек не было.

## 2026-10-16T10:32:37+03:00 — small_data_start

Создание отдельного малого H&M: до5000 пользователей/товаров, выбор только по прошлой истории

Запуск: `hm_small_data_v1`.

```json
{
  "status": "preparing"
}
```

## 2026-10-16T10:32:41+03:00 — small_data_complete

Малый H&M сохранён отдельно, ключи перенумерованы, покрытие будущих целей измерено после фиксации состава

Запуск: `hm_small_data_v1`.

```json
{
  "status": "complete",
  "config": {
    "source": "data/rel-hm",
    "seed": 42,
    "users": 5000,
    "items": 5000,
    "transactions": 46442,
    "history_start": "2020-03-11 00:00:00",
    "val_time": "2020-09-07 00:00:00",
    "test_time": "2020-09-14 00:00:00",
    "selection": "users active during 90 days before validation; uniform seed42; top5000 items by 180day pre-validation cohort counts; last8 train timestamps; no val/test labels used for membership",
    "protocol_caveat": "restricted catalog and removal of empty-label rows change task; MAP cannot be compared directly with full H&M/paper",
    "splits": {
      "train": {
        "source_cohort_rows": 5690,
        "retained_rows": 4804,
        "original_positive_items": 18986,
        "retained_positive_items": 12655,
        "positive_coverage": 0.6665437690930159,
        "dropped_empty_rows": 886,
        "min_timestamp": "2020-07-13 00:00:00",
        "max_timestamp": "2020-08-31 00:00:00"
      },
      "val": {
        "source_cohort_rows": 483,
        "retained_rows": 304,
        "original_positive_items": 1559,
        "retained_positive_items": 581,
        "positive_coverage": 0.372674791533034,
        "dropped_empty_rows": 179,
        "min_timestamp": "2020-09-07 00:00:00",
        "max_timestamp": "2020-09-07 00:00:00"
      },
      "test": {
        "source_cohort_rows": 440,
        "retained_rows": 250,
        "original_positive_items": 1428,
        "retained_positive_items": 481,
        "positive_coverage": 0.33683473389355745,
        "dropped_empty_rows": 190,
        "min_timestamp": "2020-09-14 00:00:00",
        "max_timestamp": "2020-09-14 00:00:00"
      }
    },
    "files": {
      "article_id_map.csv": {
        "bytes": 65546,
        "sha256": "b2b7ada5ca21be99251bbee4ec4f334e636f4f4b1d24a75c9961a5e8a4d50b39"
      },
      "customer_id_map.csv": {
        "bytes": 59909,
        "sha256": "27f04807923db3ce892f0bafe8c3d28b371db0faf235895758172a4f82b0f0c3"
      },
      "db/article.parquet": {
        "bytes": 220236,
        "sha256": "6c2c2eaa3ed13c38dc11b5055e16f63647b2f2098653c90e4a3bbb95cb67c160"
      },
      "db/customer.parquet": {
        "bytes": 200233,
        "sha256": "1a4ebd5bab73cdde4f767fefe79431180b626fca9ac77de2ff775a0f353ba6cf"
      },
      "db/transactions.parquet": {
        "bytes": 225067,
        "sha256": "c9bf89c7213f62125f75a3071f58df5fe6127f26c38a0cac9383d617eacba21e"
      },
      "manifest.yaml": {
        "bytes": 447,
        "sha256": "b1e03167a6809a00088b5f37724d78aefdb6a7a1518642d945e419510fe31f44"
      },
      "tasks/user-item-purchase/manifest.yaml": {
        "bytes": 718,
        "sha256": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281"
      },
      "tasks/user-item-purchase/test.parquet": {
        "bytes": 4836,
        "sha256": "7751de2a6eafb8d8b29d23080aee0795de35ea0c6a1229d697ee473c15eec74c"
      },
      "tasks/user-item-purchase/train.parquet": {
        "bytes": 41243,
        "sha256": "d70a8aea2123160e502ee613af11ba5d15d4596bb060089634f243a80725ac54"
      },
      "tasks/user-item-purchase/val.parquet": {
        "bytes": 5237,
        "sha256": "05e7ed94146660af3dbffd86770b21aeea53c35be447740869da1ba370d72299"
      }
    }
  },
  "artifacts": "data/rel-hm-small-v1"
}
```

## 2026-10-16T10:36:39+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_contextgnn_small_pipeline_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": 50,
    "temporal_strategy": "last",
    "evaluation": "all 5000 subset catalog items, all retained validation/test users",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-16T10:37:28+03:00 — small_epoch

Малый idgnn: эпоха 1/10, validation MAP=3.6864%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.11306636858927577,
  "val_metrics": {
    "map": 0.03686384521910837
  },
  "train_seconds": 15.666786797999976,
  "val_seconds": 0.061711678999927244,
  "steps": 38
}
```

## 2026-10-16T10:37:29+03:00 — small_epoch

Малый idgnn: эпоха 2/10, validation MAP=3.7658%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.06489922400367887,
  "val_metrics": {
    "map": 0.0376583622882965
  },
  "train_seconds": 1.0397788779996517,
  "val_seconds": 0.05456900900026085,
  "steps": 38
}
```

## 2026-10-16T10:37:32+03:00 — small_epoch

Малый idgnn: эпоха 3/10, validation MAP=3.9503%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.06318586123617072,
  "val_metrics": {
    "map": 0.03950253237259816
  },
  "train_seconds": 1.8831474290000187,
  "val_seconds": 0.09334312000009959,
  "steps": 38
}
```

## 2026-10-16T10:37:33+03:00 — small_epoch

Малый idgnn: эпоха 4/10, validation MAP=4.4107%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.06241046725527236,
  "val_metrics": {
    "map": 0.04410716065732514
  },
  "train_seconds": 1.209292000000005,
  "val_seconds": 0.05736955200018201,
  "steps": 38
}
```

## 2026-10-16T10:37:35+03:00 — small_epoch

Малый idgnn: эпоха 5/10, validation MAP=4.1524%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 0.058823605607214724,
  "val_metrics": {
    "map": 0.04152416631857422
  },
  "train_seconds": 1.417773653999575,
  "val_seconds": 0.06348668999999063,
  "steps": 38
}
```

## 2026-10-16T10:37:37+03:00 — small_epoch

Малый idgnn: эпоха 6/10, validation MAP=4.0447%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 0.05653320194074982,
  "val_metrics": {
    "map": 0.0404468201754386
  },
  "train_seconds": 1.4563508080000247,
  "val_seconds": 0.05182740400005059,
  "steps": 38
}
```

## 2026-10-16T10:37:39+03:00 — small_epoch

Малый idgnn: эпоха 7/10, validation MAP=3.8101%

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 0.05622837368987108,
  "val_metrics": {
    "map": 0.03810117148932938
  },
  "train_seconds": 1.1449612429996705,
  "val_seconds": 0.07271506400002181,
  "steps": 38
}
```

## 2026-10-16T10:37:39+03:00 — small_model_complete

idgnn обучен и оценён на малом наборе

Запуск: `hm_idgnn_small_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.04410716065732514
  },
  "test_metrics": {
    "map": 0.026534126984126986
  },
  "config": {
    "model": "idgnn",
    "seed": 42,
    "best_epoch": 4,
    "epochs_completed": 7,
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "training_and_validation_seconds": 27.500700685000083,
    "peak_cuda_bytes": 79007744,
    "config": {
      "dataset": "rel-hm-small-v1",
      "seed": 42,
      "channels": 64,
      "encoder_channels": 64,
      "encoder_layers": 2,
      "layers": 2,
      "neighbors": [
        32,
        16
      ],
      "rhs_embedding_dim": 64,
      "rhs_mode": "FUSION",
      "batch_size": 128,
      "max_epochs": 10,
      "early_stopping_patience": 3,
      "lr": 0.001,
      "steps_per_epoch_cap": 50,
      "temporal_strategy": "last",
      "evaluation": "all 5000 subset catalog items, all retained validation/test users",
      "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
      "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
    },
    "val_metrics": {
      "map": 0.04410716065732514
    },
    "val_inference_seconds": 0.07999127199991563,
    "test_metrics": {
      "map": 0.026534126984126986
    },
    "test_inference_seconds": 0.06833403100017676
  },
  "artifacts": "ContextGNN/results/hm_small_v1/idgnn"
}
```

## 2026-10-16T10:37:42+03:00 — small_epoch

Малый contextgnn: эпоха 1/10, validation MAP=0.1641%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 32.190852667156015,
  "val_metrics": {
    "map": 0.0016408208020050126
  },
  "train_seconds": 2.2800128229996517,
  "val_seconds": 0.06996210999977848,
  "steps": 38
}
```

## 2026-10-16T10:37:45+03:00 — small_epoch

Малый contextgnn: эпоха 2/10, validation MAP=0.8159%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 22.819407312493574,
  "val_metrics": {
    "map": 0.008158867530930501
  },
  "train_seconds": 1.8614081669998086,
  "val_seconds": 0.06624418700039314,
  "steps": 38
}
```

## 2026-10-16T10:37:48+03:00 — small_epoch

Малый contextgnn: эпоха 3/10, validation MAP=3.6627%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 22.170704791420384,
  "val_metrics": {
    "map": 0.03662691292625503
  },
  "train_seconds": 1.9523277379998945,
  "val_seconds": 0.06940084500001831,
  "steps": 38
}
```

## 2026-10-16T10:37:50+03:00 — small_epoch

Малый contextgnn: эпоха 4/10, validation MAP=4.6876%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 21.96258635269968,
  "val_metrics": {
    "map": 0.046876424014581905
  },
  "train_seconds": 1.9126371339998514,
  "val_seconds": 0.08757529300009992,
  "steps": 38
}
```

## 2026-10-16T10:37:53+03:00 — small_epoch

Малый contextgnn: эпоха 5/10, validation MAP=4.7619%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 21.820059625725996,
  "val_metrics": {
    "map": 0.04761926122123491
  },
  "train_seconds": 2.032198342000356,
  "val_seconds": 0.0728489289999743,
  "steps": 38
}
```

## 2026-10-16T10:37:55+03:00 — small_epoch

Малый contextgnn: эпоха 6/10, validation MAP=4.7465%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 21.80859570754202,
  "val_metrics": {
    "map": 0.04746475563909774
  },
  "train_seconds": 1.899244779000128,
  "val_seconds": 0.1065284100000099,
  "steps": 38
}
```

## 2026-10-16T10:37:58+03:00 — small_epoch

Малый contextgnn: эпоха 7/10, validation MAP=4.2884%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 21.55832496442293,
  "val_metrics": {
    "map": 0.04288425846814005
  },
  "train_seconds": 1.959009643999707,
  "val_seconds": 0.06765263799979948,
  "steps": 38
}
```

## 2026-10-16T10:38:00+03:00 — small_epoch

Малый contextgnn: эпоха 8/10, validation MAP=0.6885%

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 8,
  "train_loss": 21.763894382276032,
  "val_metrics": {
    "map": 0.006884543534762832
  },
  "train_seconds": 1.8462204829997972,
  "val_seconds": 0.06539446799979487,
  "steps": 38
}
```

## 2026-10-16T10:38:01+03:00 — small_model_complete

contextgnn обучен и оценён на малом наборе

Запуск: `hm_contextgnn_small_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.04761926122123491
  },
  "test_metrics": {
    "map": 0.030155754827183398
  },
  "config": {
    "model": "contextgnn",
    "seed": 42,
    "best_epoch": 5,
    "epochs_completed": 8,
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "training_and_validation_seconds": 20.95392044900018,
    "peak_cuda_bytes": 587496448,
    "config": {
      "dataset": "rel-hm-small-v1",
      "seed": 42,
      "channels": 64,
      "encoder_channels": 64,
      "encoder_layers": 2,
      "layers": 2,
      "neighbors": [
        32,
        16
      ],
      "rhs_embedding_dim": 64,
      "rhs_mode": "FUSION",
      "batch_size": 128,
      "max_epochs": 10,
      "early_stopping_patience": 3,
      "lr": 0.001,
      "steps_per_epoch_cap": 50,
      "temporal_strategy": "last",
      "evaluation": "all 5000 subset catalog items, all retained validation/test users",
      "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
      "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
    },
    "val_metrics": {
      "map": 0.04761926122123491
    },
    "val_inference_seconds": 0.06755045899990364,
    "test_metrics": {
      "map": 0.030155754827183398
    },
    "test_inference_seconds": 0.05535964399996374
  },
  "artifacts": "ContextGNN/results/hm_small_v1/contextgnn"
}
```

## 2026-10-16T10:40:08+03:00 — small_manual_features

Ручные признаки val готовы: 304 пользователей ×5000 товаров

Запуск: `hm_small_manual_features_v1`.

```json
{
  "status": "features",
  "split": "val",
  "pairs": 1520000
}
```

## 2026-10-16T10:40:13+03:00 — small_manual_features

Ручные признаки test готовы: 250 пользователей ×5000 товаров

Запуск: `hm_small_manual_features_v1`.

```json
{
  "status": "features",
  "split": "test",
  "pairs": 1250000
}
```

## 2026-10-16T10:40:13+03:00 — small_manual_features_complete

Общие обучающие пары двух LightGBM и ручные признаки малого набора сохранены

Запуск: `hm_small_manual_features_v1`.

```json
{
  "status": "complete",
  "train_pairs": 72813,
  "artifacts": "ContextGNN/cache/hm_small_v1/manual"
}
```

## 2026-10-16T10:41:39+03:00 — small_context_start

Малый ContextGNN: независимый инференс

Запуск: `hm_contextgnn_small_pipeline_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": 50,
    "temporal_strategy": "last",
    "evaluation": "all 5000 subset catalog items, all retained validation/test users",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-16T10:42:11+03:00 — small_model_verified

Независимая проверка idgnn на малом наборе

Запуск: `hm_idgnn_small_seed_42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 12.069197740999698
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.11253019600007974
    },
    "checkpoint_sha256": "233082a0d8b0d8de78140a3866bfff449b9e28bcda82793c98ebe5e98ff5f9b4"
  }
}
```

## 2026-10-16T10:42:11+03:00 — small_model_verified

Независимая проверка contextgnn на малом наборе

Запуск: `hm_contextgnn_small_seed_42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.2822634219996871
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.06461526600014622
    },
    "checkpoint_sha256": "ab6ac0b09d1577261a0246b7462db09af61af729bf050431b1f2f8cbb1fedd15"
  }
}
```

## 2026-10-16T10:43:05+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_contextgnn_small_pipeline_v1`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": 50,
    "temporal_strategy": "last",
    "evaluation": "all 5000 subset catalog items, all retained validation/test users",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-16T10:44:03+03:00 — small_idgnn_features

ID-GNN признаки малого train сохранены; всего72813, без вектора51335

Запуск: `hm_small_idgnn_features_v1`.

```json
{
  "status": "features",
  "counts": {
    "pairs": 72813,
    "missing_embeddings": 51335,
    "user_times": 4804
  }
}
```

## 2026-10-16T10:44:07+03:00 — small_idgnn_features

ID-GNN признаки малого val сохранены; всего1520000, без вектора1516257

Запуск: `hm_small_idgnn_features_v1`.

```json
{
  "status": "features",
  "counts": {
    "pairs": 1520000,
    "missing_embeddings": 1516257,
    "user_times": 304
  }
}
```

## 2026-10-16T10:44:10+03:00 — small_idgnn_features

ID-GNN признаки малого test сохранены; всего1250000, без вектора1247101

Запуск: `hm_small_idgnn_features_v1`.

```json
{
  "status": "features",
  "counts": {
    "pairs": 1250000,
    "missing_embeddings": 1247101,
    "user_times": 250
  }
}
```

## 2026-10-16T10:44:46+03:00 — small_tree_trial

lightgbm_manual: leaves15, valMAP0.9983%

Запуск: `hm_small_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 15,
    "validation_map": 0.009983192672337408
  }
}
```

## 2026-10-16T10:44:57+03:00 — small_tree_trial

lightgbm_manual: leaves31, valMAP0.9359%

Запуск: `hm_small_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 31,
    "validation_map": 0.00935897983595352
  }
}
```

## 2026-10-16T10:45:21+03:00 — small_tree_complete

lightgbm_manual пересчитан и проверен на общем малом каталоге

Запуск: `hm_small_lightgbm_manual_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.009983192672337408
  },
  "test_metrics": {
    "map": 0.012338802308802308
  },
  "config": {
    "model": "lightgbm_manual",
    "seed": 42,
    "train_pairs": 72813,
    "train_pair_sha256": "a583938c3a58f481ed65811b830b421a577489136c6f6f666ce5ef6915cb6d39",
    "train_user_times": 4804,
    "features": [
      "u_age",
      "u_fn_not_null",
      "u_is_active",
      "u_club_member_status",
      "u_fashion_news_frequency",
      "i_product_type_no",
      "i_graphical_appearance_no",
      "i_colour_group_code",
      "i_perceived_colour_master_id",
      "i_department_no",
      "i_section_no",
      "i_garment_group_no",
      "u_count_all",
      "u_amount_all",
      "u_price_all",
      "u_unique_all",
      "u_channel2_all",
      "u_recency_days",
      "u_mode_department_all",
      "u_mode_section_all",
      "u_mode_colour_all",
      "u_count_week1",
      "u_amount_week1",
      "u_price_week1",
      "u_unique_week1",
      "u_channel2_week1",
      "u_mode_department_week1",
      "u_mode_section_week1",
      "u_mode_colour_week1",
      "u_count_week2",
      "u_amount_week2",
      "u_price_week2",
      "u_unique_week2",
      "u_channel2_week2",
      "u_mode_department_week2",
      "u_mode_section_week2",
      "u_mode_colour_week2",
      "u_count_week3",
      "u_amount_week3",
      "u_price_week3",
      "u_unique_week3",
      "u_channel2_week3",
      "u_mode_department_week3",
      "u_mode_section_week3",
      "u_mode_colour_week3",
      "u_count_week4",
      "u_amount_week4",
      "u_price_week4",
      "u_unique_week4",
      "u_channel2_week4",
      "u_mode_department_week4",
      "u_mode_section_week4",
      "u_mode_colour_week4",
      "u_count_week5",
      "u_amount_week5",
      "u_price_week5",
      "u_unique_week5",
      "u_channel2_week5",
      "u_mode_department_week5",
      "u_mode_section_week5",
      "u_mode_colour_week5",
      "u_count_28d",
      "i_count_all",
      "i_amount_all",
      "i_price_all",
      "i_recency_days",
      "i_count_week1",
      "i_amount_week1",
      "i_price_week1",
      "i_unique_buyers_week1",
      "i_buyer_age_week1",
      "i_count_week2",
      "i_amount_week2",
      "i_price_week2",
      "i_unique_buyers_week2",
      "i_buyer_age_week2",
      "i_count_week3",
      "i_amount_week3",
      "i_price_week3",
      "i_unique_buyers_week3",
      "i_buyer_age_week3",
      "i_count_week4",
      "i_amount_week4",
      "i_price_week4",
      "i_unique_buyers_week4",
      "i_buyer_age_week4",
      "i_count_week5",
      "i_amount_week5",
      "i_price_week5",
      "i_unique_buyers_week5",
      "i_buyer_age_week5",
      "p_count_all",
      "p_price_all",
      "p_count_7d",
      "p_count_28d",
      "p_recency_days",
      "a_dept_count_28d",
      "a_dept_share_28d",
      "a_section_count_28d",
      "a_section_share_28d",
      "a_colour_count_28d",
      "a_colour_share_28d",
      "a_type_count_28d",
      "a_type_share_28d",
      "match_department_all",
      "match_department_week1",
      "match_department_week2",
      "match_department_week3",
      "match_department_week4",
      "match_department_week5",
      "match_section_all",
      "match_section_week1",
      "match_section_week2",
      "match_section_week3",
      "match_section_week4",
      "match_section_week5",
      "match_colour_all",
      "match_colour_week1",
      "match_colour_week2",
      "match_colour_week3",
      "match_colour_week4",
      "match_colour_week5",
      "price_gap",
      "price_ratio",
      "week_of_year",
      "month_of_year"
    ],
    "categorical_features": [
      "u_club_member_status",
      "u_fashion_news_frequency",
      "i_product_type_no",
      "i_graphical_appearance_no",
      "i_colour_group_code",
      "i_perceived_colour_master_id",
      "i_department_no",
      "i_section_no",
      "i_garment_group_no",
      "u_mode_department_all",
      "u_mode_section_all",
      "u_mode_colour_all",
      "u_mode_department_week1",
      "u_mode_section_week1",
      "u_mode_colour_week1",
      "u_mode_department_week2",
      "u_mode_section_week2",
      "u_mode_colour_week2",
      "u_mode_department_week3",
      "u_mode_section_week3",
      "u_mode_colour_week3",
      "u_mode_department_week4",
      "u_mode_section_week4",
      "u_mode_colour_week4",
      "u_mode_department_week5",
      "u_mode_section_week5",
      "u_mode_colour_week5"
    ],
    "trials": [
      {
        "num_leaves": 15,
        "validation_map": 0.009983192672337408
      },
      {
        "num_leaves": 31,
        "validation_map": 0.00935897983595352
      }
    ],
    "selected_num_leaves": 15,
    "rounds": 150,
    "training_and_tuning_seconds": 20.122374947000026,
    "inference_from_saved_model": true,
    "evaluation_catalog": 5000,
    "subset": "rel-hm-small-v1",
    "candidate_audit": {
      "val": {
        "full_catalog": true,
        "users": 304,
        "pairs": 1520000
      },
      "test": {
        "full_catalog": true,
        "users": 250,
        "pairs": 1250000
      }
    },
    "val_metrics": {
      "map": 0.009983192672337408
    },
    "val_inference_seconds": 6.522759204999602,
    "test_metrics": {
      "map": 0.012338802308802308
    },
    "test_inference_seconds": 5.045370581000043
  },
  "artifacts": "ContextGNN/results/hm_small_v1/lightgbm_manual"
}
```

## 2026-10-16T10:45:24+03:00 — small_tree_trial

lightgbm_idgnn: leaves15, valMAP0.6853%

Запуск: `hm_small_lightgbm_idgnn_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 15,
    "validation_map": 0.006853070175438595
  }
}
```

## 2026-10-16T10:45:27+03:00 — small_tree_trial

lightgbm_idgnn: leaves31, valMAP0.6853%

Запуск: `hm_small_lightgbm_idgnn_seed_42_v1`.

```json
{
  "status": "tuning",
  "trial": {
    "num_leaves": 31,
    "validation_map": 0.006853070175438595
  }
}
```

## 2026-10-16T10:45:35+03:00 — small_tree_complete

lightgbm_idgnn пересчитан и проверен на общем малом каталоге

Запуск: `hm_small_lightgbm_idgnn_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.006853070175438595
  },
  "test_metrics": {
    "map": 0.009666666666666665
  },
  "config": {
    "model": "lightgbm_idgnn",
    "seed": 42,
    "train_pairs": 72813,
    "train_pair_sha256": "a583938c3a58f481ed65811b830b421a577489136c6f6f666ce5ef6915cb6d39",
    "train_user_times": 4804,
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
      "gnn_available"
    ],
    "categorical_features": [],
    "trials": [
      {
        "num_leaves": 15,
        "validation_map": 0.006853070175438595
      },
      {
        "num_leaves": 31,
        "validation_map": 0.006853070175438595
      }
    ],
    "selected_num_leaves": 15,
    "rounds": 150,
    "training_and_tuning_seconds": 5.406174842000382,
    "inference_from_saved_model": true,
    "evaluation_catalog": 5000,
    "subset": "rel-hm-small-v1",
    "candidate_audit": {
      "val": {
        "full_catalog": true,
        "users": 304,
        "pairs": 1520000
      },
      "test": {
        "full_catalog": true,
        "users": 250,
        "pairs": 1250000
      }
    },
    "embedding_coverage": {
      "train": {
        "pairs": 72813,
        "missing_embeddings": 51335,
        "user_times": 4804
      },
      "val": {
        "pairs": 1520000,
        "missing_embeddings": 1516257,
        "user_times": 304
      },
      "test": {
        "pairs": 1250000,
        "missing_embeddings": 1247101,
        "user_times": 250
      }
    },
    "missing_policy": "zero local vector plus availability flag; in-sample frozen ID-GNN train representations",
    "val_metrics": {
      "map": 0.006853070175438595
    },
    "val_inference_seconds": 1.9870614540000133,
    "test_metrics": {
      "map": 0.009666666666666665
    },
    "test_inference_seconds": 1.7468301660001089
  },
  "artifacts": "ContextGNN/results/hm_small_v1/lightgbm_idgnn"
}
```

## 2026-10-16T10:46:48+03:00 — small_pilot_complete

Малый пилот завершён: ContextGNN, ID-GNN и оба LightGBM оценены по всем5000товарам; модели проверены, MAP пересчитан из сохранённых предсказаний, общие пары/кандидаты сверены. Отчёт и графики сохранены отдельно от полного H&M.

Запуск: `hm_contextgnn_small_pipeline_v1`.

```json
{
  "status": "complete",
  "comparison": [
    {
      "method": "Popularity",
      "training_seconds": 0.0,
      "val_inference_seconds": 0.0,
      "test_inference_seconds": 0.0,
      "validation_map_percent": 0.26256116481680386,
      "test_map_percent": 0.7264502164502166
    },
    {
      "method": "ID-GNN",
      "validation_map_percent": 4.4107160657325135,
      "test_map_percent": 2.6534126984126987,
      "training_seconds": 27.500700685000083,
      "val_inference_seconds": 0.07999127199991563,
      "test_inference_seconds": 0.06833403100017676
    },
    {
      "method": "ContextGNN",
      "validation_map_percent": 4.761926122123491,
      "test_map_percent": 3.0155754827183396,
      "training_seconds": 20.95392044900018,
      "val_inference_seconds": 0.06755045899990364,
      "test_inference_seconds": 0.05535964399996374
    },
    {
      "method": "LightGBM + manual",
      "validation_map_percent": 0.9983192672337408,
      "test_map_percent": 1.2338802308802308,
      "training_seconds": 20.122374947000026,
      "val_inference_seconds": 6.522759204999602,
      "test_inference_seconds": 5.045370581000043
    },
    {
      "method": "LightGBM + ID-GNN features",
      "validation_map_percent": 0.6853070175438595,
      "test_map_percent": 0.9666666666666666,
      "training_seconds": 5.406174842000382,
      "val_inference_seconds": 1.9870614540000133,
      "test_inference_seconds": 1.7468301660001089
    }
  ],
  "artifacts": "reports/contextgnn_small_v1"
}
```

## 2026-10-16T10:49:22+03:00 — small_pilot_final_audit

Малый набор создан до обучения и сохранён в data/rel-hm-small-v1:5000users/5000items/46442transactions,train4804/val304/test250. Пользователь добавил оба LightGBM: пересчитаны на одинаковых72813парах, SHA совпал, eval общийuser×5000catalog сверён. TestMAP%:ContextGNN3.01558,IDGNN2.65341,manualLightGBM1.23388,IDGNN-LightGBM0.96667. Независимые replay/пересчётMAP и проверки CE value/gradient, FK/time и SHA набора прошли. CI разницы Context−ID включает0; малый каталог ограничивает покрытие, нельзя сравнивать с полнымH&M. Графики просмотрены, контекст обновлён, все этапы завершены.

## 2026-10-16T11:02:00+03:00 — small_twotower_start

Двухбашенная Model из прежнего проекта подключена к малому H&M

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "preparing",
  "artifacts": "ContextGNN/results/hm_small_v1/two_tower"
}
```

## 2026-10-16T11:02:27+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха1/10, valMAP0.7587%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.6376428192570096,
  "val_metrics": {
    "map": 0.0075867936887673735
  },
  "train_seconds": 11.400553931999639,
  "val_seconds": 0.4669161290003103,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:30+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха2/10, valMAP0.4322%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.5883399553242183,
  "val_metrics": {
    "map": 0.004322438039543303
  },
  "train_seconds": 2.3331163060001927,
  "val_seconds": 0.5348695419997966,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:34+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха3/10, valMAP0.6272%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.528716191649437,
  "val_metrics": {
    "map": 0.006272131559960507
  },
  "train_seconds": 2.403867938000076,
  "val_seconds": 0.5431426969998938,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:37+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха4/10, valMAP0.9963%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.4541755808251245,
  "val_metrics": {
    "map": 0.009963315802131592
  },
  "train_seconds": 2.3304691280000043,
  "val_seconds": 0.4844005130007645,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:40+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха5/10, valMAP1.5520%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 0.3525588774077949,
  "val_metrics": {
    "map": 0.015520058036505404
  },
  "train_seconds": 2.4002117059999364,
  "val_seconds": 0.5931487339994419,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:44+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха6/10, valMAP1.5526%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 0.24079838205528045,
  "val_metrics": {
    "map": 0.015525635426951217
  },
  "train_seconds": 2.4055162899994684,
  "val_seconds": 0.4947864910000135,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:47+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха7/10, valMAP1.3556%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 0.1988964854972437,
  "val_metrics": {
    "map": 0.013555817811574392
  },
  "train_seconds": 2.241698926999561,
  "val_seconds": 0.48320974800026306,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:50+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха8/10, valMAP1.0174%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 8,
  "train_loss": 0.18179444459799146,
  "val_metrics": {
    "map": 0.010174366629958737
  },
  "train_seconds": 2.36081483199996,
  "val_seconds": 0.4766806269999506,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:53+03:00 — small_twotower_epoch

Малая двухбашенная GNN: эпоха9/10, valMAP1.0591%

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "training",
  "epoch": 9,
  "train_loss": 0.14469169405111598,
  "val_metrics": {
    "map": 0.010591385344674818
  },
  "train_seconds": 2.2572714490006547,
  "val_seconds": 0.5086964009997246,
  "train_rows": 4804
}
```

## 2026-10-16T11:02:54+03:00 — small_twotower_complete

Двухбашенная модель заново обучена и оценена на том же малом наборе

Запуск: `hm_twotower_small_seed_42_v1`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.015525635426951217
  },
  "test_metrics": {
    "map": 0.006836767676767676
  },
  "config": {
    "model": "Two-tower GraphSAGE",
    "seed": 42,
    "best_epoch": 6,
    "epochs_completed": 9,
    "config": {
      "subset": "rel-hm-small-v1",
      "seed": 42,
      "channels": 64,
      "layers": 2,
      "encoder_channels": 64,
      "encoder_layers": 2,
      "neighbors": [
        32,
        16
      ],
      "batch_size": 128,
      "max_epochs": 10,
      "patience": 3,
      "lr": 0.001,
      "temporal_strategy": "last",
      "shared_model": true,
      "shallow_item_embedding": true,
      "loss": "BPR with same-time in-batch negatives",
      "training_rows": 4804,
      "steps_per_epoch": 42,
      "partial_batch_policy": "keep remainders of every timestamp group, no training rows dropped",
      "source": "RelBenchGNN/upstream/examples/model.py, same Model as run_two_tower.py",
      "source_commit": "919fb8a61a4b4cb787283860597f45701895578d",
      "trainable_parameters": 920768,
      "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096"
    },
    "training_and_validation_seconds": 38.09164969699941,
    "peak_cuda_bytes": 121253376,
    "val_metrics": {
      "map": 0.015525635426951217
    },
    "val_inference_seconds": 0.5815334320004695,
    "test_metrics": {
      "map": 0.006836767676767676
    },
    "test_inference_seconds": 0.6985469760002161
  },
  "artifacts": "ContextGNN/results/hm_small_v1/two_tower"
}
```

## 2026-10-16T11:03:55+03:00 — small_twotower_start

Двухбашенная Model из прежнего проекта подключена к малому H&M

Запуск: `hm_twotower_small_seed_42_v1_inference`.

```json
{
  "status": "preparing",
  "artifacts": "ContextGNN/results/hm_small_v1/two_tower"
}
```

## 2026-10-16T11:04:17+03:00 — small_twotower_verified

Двухбашенный независимый инференс малого набора проверен

Запуск: `hm_twotower_small_seed_42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 10.199683484999696
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.6276555509994068
    }
  }
}
```

## 2026-10-16T11:04:30+03:00 — small_pilot_complete

Малый пилот завершён: ContextGNN, ID-GNN и оба LightGBM оценены по всем5000товарам; модели проверены, MAP пересчитан из сохранённых предсказаний, общие пары/кандидаты сверены. Отчёт и графики сохранены отдельно от полного H&M.

Запуск: `hm_contextgnn_small_pipeline_v1`.

```json
{
  "status": "complete",
  "comparison": [
    {
      "method": "Popularity",
      "training_seconds": 0.0,
      "val_inference_seconds": 0.0,
      "test_inference_seconds": 0.0,
      "validation_map_percent": 0.26256116481680386,
      "test_map_percent": 0.7264502164502166
    },
    {
      "method": "ID-GNN",
      "validation_map_percent": 4.4107160657325135,
      "test_map_percent": 2.6534126984126987,
      "training_seconds": 27.500700685000083,
      "val_inference_seconds": 0.07999127199991563,
      "test_inference_seconds": 0.06833403100017676
    },
    {
      "method": "ContextGNN",
      "validation_map_percent": 4.761926122123491,
      "test_map_percent": 3.0155754827183396,
      "training_seconds": 20.95392044900018,
      "val_inference_seconds": 0.06755045899990364,
      "test_inference_seconds": 0.05535964399996374
    },
    {
      "method": "Two-tower GraphSAGE",
      "validation_map_percent": 1.5525635426951216,
      "test_map_percent": 0.6836767676767677,
      "training_seconds": 38.09164969699941,
      "val_inference_seconds": 0.5815334320004695,
      "test_inference_seconds": 0.6985469760002161
    },
    {
      "method": "LightGBM + manual",
      "validation_map_percent": 0.9983192672337408,
      "test_map_percent": 1.2338802308802308,
      "training_seconds": 20.122374947000026,
      "val_inference_seconds": 6.522759204999602,
      "test_inference_seconds": 5.045370581000043
    },
    {
      "method": "LightGBM + ID-GNN features",
      "validation_map_percent": 0.6853070175438595,
      "test_map_percent": 0.9666666666666666,
      "training_seconds": 5.406174842000382,
      "val_inference_seconds": 1.9870614540000133,
      "test_inference_seconds": 1.7468301660001089
    }
  ],
  "artifacts": "reports/contextgnn_small_v1"
}
```

## 2026-10-16T11:06:50+03:00 — audit

Small pilot complete: five trained models plus Popularity; two-tower checkpoint replay passed with identical predictions and zero MAP difference; comparison and learning-curve figures visually checked. Previous four models unchanged; previous report archived in before_two_tower.

Запуск: `hm_small_comparison_v1`.

```json
{
  "status": "complete"
}
```

## 2026-10-16T11:23:53+03:00 — analysis

Checked paper LightGBM H-and-M val/test 0.44/0.38 percent versus local manual126 0.998/1.234 percent; features and datasets differ. Documented sampled binary training and limited tuning as untested explanations, not established causes. See reports/contextgnn_small_v1/manual_baseline_interpretation.md. No retraining.

## 2026-10-16T13:13:10+03:00 — llama_qwen_common_subset_comparison

Пересчитан замороженный Qwen H002 candidate060 на тех же1024val/2048test пользователях и ID-GNN пулах, что Llama flat. Строки/цели/customerIDs/принадлежностьtop12 проверены. Без нового обучения или выбора поtest. Qwen subset testMAP=1.429810%;Llama flat0.800949%. Это сравнение разных конвейеров, не чистой силыLLM.

```json
{
  "artifacts": "reports/llama_vs_qwen_shared_subset",
  "qwen_subset_test_map": 0.014298102749030482,
  "test_users": 2048
}
```

## 2026-10-16T13:22:40+03:00 — project_review

Reviewed project history, protocols and main data/model entry points before a new user-defined experiment. No training launched or environment changed. WSL process inspection found no project training/evaluation process; RTX 3060 Laptop GPU reported 0 MiB and 0 percent utilization. Historical evaluating/paused statuses are not proof of live jobs. Awaiting next experiment specification; scope and compute budget remain to be defined.

## 2026-10-16T13:29:27+03:00 — recformer_assessment

Recorded user goals: research report, H&M recommendations, existing small-v1 subset preferred, RTX3060 or KaggleT4, desired experiment duration at most one hour. Reviewed Recformer paper and linked replication code. Author repo currently README only. Proposed cutoff-safe multi-positive weekly adaptation and full5000 MAP12 evaluation. Checkpoint bytes, compatibility and runtime not yet verified; no training launched. See reports/recformer_assessment.md.

## 2026-10-16T13:47:10+03:00 — recformer_error

Recformer small error: PytorchStreamReader failed reading zip archive: failed finding central directory

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "failed"
}
```

## 2026-10-16T13:48:56+03:00 — recformer_preparation

Pinned replication 26b00a58e7affe0c54a89c143ea7bce37f2e8e08 and implemented separate small-HM adapter without changing packages. First checkpoint download was truncated (277495808 versus749479199 bytes), rejected by PyTorch before training; downloader now resumes HTTP ranges and checks size and ZIP. Full experiment not started; smoke timing pending.

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "preparing"
}
```

## 2026-10-16T13:53:09+03:00 — recformer_smoke

Full pretrained checkpoint loaded; only unused MLM head keys ignored. Smoke passed on RTX3060:148110336parameters, peak2798040064bytes, catalog encode26.75s, warm batch4 steps0.16-0.22s. Four full epochs estimated924s before evaluation/checkpoint overhead. Fixing2+2epochs,256tokens,batch4/accum4; no test metrics inspected.

Запуск: `hm_recformer_small_smoke_v1`.

```json
{
  "status": "smoke_complete"
}
```

## 2026-10-16T13:54:06+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 5e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "f4c57d8a77b73ef2bece649b53dd506697b419f8d80a64dbb127537bf77be62f",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-16T13:56:13+03:00 — recformer_data_audit

All10small-v1 files match original sizes and SHA256; cutoff and multi-positive-loss behavior checks passed. Exactly4846unique tokenized item descriptions among5000catalog items at3attributes/32tokens per attribute; content collisions are an explicit text-only limitation. Full first epoch running; no new test results inspected.

## 2026-10-16T13:59:22+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 0.76477%

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 8.4865389140222,
    "val_metrics": {
      "map": 0.0076477296460849085
    },
    "epoch_seconds": 266.2759240669984,
    "val_seconds": 5.390641175999917,
    "rows": 4804
  }
}
```

## 2026-10-16T14:04:39+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 0.70129%

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.444978222461863,
    "val_metrics": {
      "map": 0.007012915812257919
    },
    "epoch_seconds": 316.8079238829996,
    "val_seconds": 4.8983171279996895,
    "rows": 4804
  }
}
```

## 2026-10-16T14:09:59+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 1.28200%

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.389285053440574,
    "val_metrics": {
      "map": 0.012820035410495936
    },
    "epoch_seconds": 308.07688992600015,
    "val_seconds": 6.406644815999243,
    "rows": 4804
  }
}
```

## 2026-10-16T14:15:02+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 2.47022%

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.32651477769253,
    "val_metrics": {
      "map": 0.02470220295055821
    },
    "epoch_seconds": 296.2743831259995,
    "val_seconds": 6.732142905999353,
    "rows": 4804
  }
}
```

## 2026-10-16T14:15:22+03:00 — recformer_measured

Recformer zero_shot: metrics measured, independent replay pending

Запуск: `hm_recformer_small_seed42_v1_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_seed42_v1/zero_shot"
}
```

## 2026-10-16T14:15:41+03:00 — recformer_measured

Recformer finetuned: metrics measured, independent replay pending

Запуск: `hm_recformer_small_seed42_v1_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.02470220295055821
  },
  "test_metrics": {
    "map": 0.012355555555555555
  },
  "artifacts": "Recformer/results/hm_small_seed42_v1/finetuned"
}
```

## 2026-10-16T14:17:47+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_recformer_small_seed42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.026699561403508775,
        "seconds": 16.32431028499923
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03300543530543531,
        "seconds": 4.040454604999468
      },
      "checkpoint_sha256": "b8fdcc6d1904a74fe590c29b3aa61c8faaed4bbd2554cf2b6f1d5096cc1f7601"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.02470220295055821,
        "seconds": 4.714585158000773
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.012355555555555555,
        "seconds": 3.726713430000018
      },
      "checkpoint_sha256": "0152a42e16472dd3561c804256a193e534e2f6daaff6aacb802eac4d4ed1c118"
    }
  }
}
```

## 2026-10-16T14:18:03+03:00 — recformer_complete

Recformer zero_shot: complete and independently verified

Запуск: `hm_recformer_small_seed42_v1_zero_shot`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_seed42_v1/zero_shot"
}
```

## 2026-10-16T14:18:03+03:00 — recformer_complete

Recformer finetuned: complete and independently verified

Запуск: `hm_recformer_small_seed42_v1_finetuned`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.02470220295055821
  },
  "test_metrics": {
    "map": 0.012355555555555555
  },
  "artifacts": "Recformer/results/hm_small_seed42_v1/finetuned"
}
```

## 2026-10-16T14:18:05+03:00 — recformer_report

Recformer small report generated after full independent replay; old reports unchanged

Запуск: `hm_recformer_small_seed42_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/recformer_small_v1",
  "comparison": [
    {
      "method": "Popularity",
      "validation_map_percent": 0.2625611648168038,
      "test_map_percent": 0.7264502164502166,
      "training_seconds": 0.0,
      "val_inference_seconds": 0.0,
      "test_inference_seconds": 0.0
    },
    {
      "method": "ID-GNN",
      "validation_map_percent": 4.4107160657325135,
      "test_map_percent": 2.6534126984126987,
      "training_seconds": 27.500700685000083,
      "val_inference_seconds": 0.0799912719999156,
      "test_inference_seconds": 0.0683340310001767
    },
    {
      "method": "ContextGNN",
      "validation_map_percent": 4.761926122123491,
      "test_map_percent": 3.01557548271834,
      "training_seconds": 20.95392044900018,
      "val_inference_seconds": 0.0675504589999036,
      "test_inference_seconds": 0.0553596439999637
    },
    {
      "method": "Two-tower GraphSAGE",
      "validation_map_percent": 1.5525635426951216,
      "test_map_percent": 0.6836767676767677,
      "training_seconds": 38.09164969699941,
      "val_inference_seconds": 0.5815334320004695,
      "test_inference_seconds": 0.6985469760002161
    },
    {
      "method": "LightGBM + manual",
      "validation_map_percent": 0.9983192672337408,
      "test_map_percent": 1.2338802308802308,
      "training_seconds": 20.122374947000026,
      "val_inference_seconds": 6.522759204999602,
      "test_inference_seconds": 5.045370581000043
    },
    {
      "method": "LightGBM + ID-GNN features",
      "validation_map_percent": 0.6853070175438595,
      "test_map_percent": 0.9666666666666666,
      "training_seconds": 5.406174842000382,
      "val_inference_seconds": 1.987061454000013,
      "test_inference_seconds": 1.7468301660001089
    },
    {
      "method": "Recformer zero_shot",
      "training_seconds": 0.0,
      "validation_map_percent": 2.6699561403508776,
      "val_inference_seconds": 6.151355272000728,
      "test_map_percent": 3.3005435305435307,
      "test_inference_seconds": 6.137794426000255
    },
    {
      "method": "Recformer finetuned",
      "training_seconds": 1255.72406289,
      "validation_map_percent": 2.470220295055821,
      "val_inference_seconds": 5.816426020001018,
      "test_map_percent": 1.2355555555555555,
      "test_inference_seconds": 4.916274175999206
    }
  ],
  "bootstrap": {
    "zero_shot": {
      "delta_percentage_points": -2.0649879749879747,
      "paired_user_bootstrap_95ci_pp": [
        -4.16532251082251,
        -0.00999735449735592
      ]
    },
    "contextgnn": {
      "delta_percentage_points": -1.7800199271627843,
      "paired_user_bootstrap_95ci_pp": [
        -3.910321677660963,
        0.27627463409606273
      ]
    },
    "idgnn": {
      "delta_percentage_points": -1.417857142857143,
      "paired_user_bootstrap_95ci_pp": [
        -3.388894841269841,
        0.48982539682539367
      ]
    },
    "lightgbm_manual": {
      "delta_percentage_points": 0.0016753246753246742,
      "paired_user_bootstrap_95ci_pp": [
        -1.3446391414141412,
        1.3529040043290042
      ]
    },
    "lightgbm_idgnn": {
      "delta_percentage_points": 0.26888888888888884,
      "paired_user_bootstrap_95ci_pp": [
        -1.3756666666666666,
        1.8756111111111105
      ]
    },
    "two_tower": {
      "delta_percentage_points": 0.5518787878787879,
      "paired_user_bootstrap_95ci_pp": [
        -0.8486979797979796,
        2.0440277777777776
      ]
    }
  },
  "zero_shot_bootstrap": {
    "contextgnn": {
      "delta_percentage_points": 0.28496804782519064,
      "paired_user_bootstrap_95ci_pp": [
        -1.2331769652305367,
        1.7975353878925304
      ]
    },
    "idgnn": {
      "delta_percentage_points": 0.647130832130832,
      "paired_user_bootstrap_95ci_pp": [
        -0.8770432900432901,
        2.168402296777297
      ]
    },
    "lightgbm_manual": {
      "delta_percentage_points": 2.0666632996633,
      "paired_user_bootstrap_95ci_pp": [
        0.11209843674843685,
        4.140414285714286
      ]
    },
    "lightgbm_idgnn": {
      "delta_percentage_points": 2.333876863876864,
      "paired_user_bootstrap_95ci_pp": [
        0.9034411976911976,
        3.9707766955266934
      ]
    },
    "two_tower": {
      "delta_percentage_points": 2.6168667628667626,
      "paired_user_bootstrap_95ci_pp": [
        0.7060319384319386,
        4.696972366522365
      ]
    }
  }
}
```

## 2026-10-16T14:23:54+03:00 — recformer_final_audit

Recformer small experiment completed: pipeline exit0; all4zero-shot/fine-tuned val/test replays have identical full scores and top12. Comparison and learning-curve PNGs visually verified. Frozen subset/source hashes passed. Zero-shot val/test2.669956/3.300544percent; fine-tuned2.470220/1.235556percent; train+val20.93min. Zero-shot minus ContextGNN test+0.284968pp, paired95CI[-1.23318,1.79754], no established robust superiority. Old artifacts unchanged; context and report updated.

## 2026-10-16T14:27:31+03:00 — recformer_finetuning_diagnosis

Posthoc saved-prediction audit, no retraining: fine-tuned recommendations concentrate. Validation unique top12 items1989->722, max single-item user share6.58->50.66percent; test1735->600 and5.6->54.8percent. More popular items recommended on average. Four-epoch val curve recovers in stage2, so excessive epochs/classic overfitting is not established. Hypotheses: full148M adaptation on4804rows, constantlr withoutwarmup, weekly objective mismatch and item-cache drift. See reports/recformer_small_v1/finetuning_diagnosis.md.

## 2026-10-16T14:39:01+03:00 — kaggle_notebook_ready

Отдельный KaggleT4 notebook Qwen2.5-Coder7B vs Llama3.1-8B на неизменном ContextGNN small-v1 готов. Прежний SQL/JSON интерфейс Qwen; обе NF4/FP16, одинаковые72813trainпар,128search/88confirm/88heldoutval, val304/test250 и весь5000каталог.20успешных/300calls/3repairs/3islands на каждую. Семь сохранённых baseline+Popularity, графики/гистограммы, независимый replay и ZIP. CPU integration с фиктивными ответами проверен; реального нового LLM результата нет. Категории компактно закодированы согласованно в raw/history: тестовый model.txt уменьшен174MB→1.3MB. Проверка ID-сопоставления применяется к обеим моделям; старая обнаруженная ошибка была в Python Llama v5, а не установленной ошибкой Qwen.

Запуск: `hm_small_qwen_llama_sql_v1`.

```json
{
  "status": "notebook_ready",
  "artifacts": "LLMFeatures/kaggle/small_compare",
  "delivery": {
    "protocol": "hm_small_qwen_llama_sql_v1",
    "notebook": "hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb",
    "notebook_sha256": "173b5a4558a4a7a009b296aaa7f81240407140705fa6b3436c94f098804851f1",
    "modules": {
      "features.py": "d4625f7cfe65395925a54984835a5b9536dbde586be7916deaaacbe50069efe1",
      "original_prompt.py": "0b79bb4885bf6383a6a4afb4d18828265780d691aa314e9ea917a1969951d82c",
      "worker.py": "3844f32b7a86a387725f6a5c1cc0121c8f7921aee2893e17847bd6c0c47c92a4",
      "runtime.py": "33fead39d4b655ca862921261e33345df2a22f00f483bec864b530a6f8ad10f0"
    },
    "bundle_manifest_sha256": "3cb473dfafa1d60c4922fe85e63ae5b19efe0cf76f72cfd04164030132db01a3",
    "dataset": "hm_small_sql_compare_v1.zip",
    "dataset_sha256": "99197d63ad853b6dfa3b88ed10afddec076bb2c3038612622ae9ad4cfaaa8406",
    "llm_inference_executed_locally": false
  },
  "verification": "reports/kaggle_llmfe_validation/small_compare_v1/verification.json"
}
```

## 2026-10-16T16:50:36+03:00 — recformer_ablation_plan

User approved two separate sequential ablations: peakLR1e-5 with100-updatewarmup and linear decay, then independently frozen embeddings+lower6/12layers with originalconstantLR5e-5. Same pretrained/small-v1/seed/order/2+2epochs. Both train and select onval before either test is evaluated. Epoch0 eligible in selection.json, best-trained still reported separately. Longer stage2 discussed as useful future separate experiment, not launched.

Запуск: `hm_recformer_ablations_v1`.

```json
{
  "status": "preparing"
}
```

## 2026-10-16T16:51:54+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 1e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "low_lr_warmup",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 148110336,
      "frozen": 0
    },
    "freeze_policy": "none",
    "scheduler": "100 successful optimizer updates warmup, then linear decay over1204 updates",
    "warmup_updates": 100,
    "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "b77815d134c79aa2b96770dc12cbc2e55bf63df6b237d05f36a2624a922f10a1",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-16T16:57:15+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 3.00099%

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 8.518387130654721,
    "val_metrics": {
      "map": 0.030009920634920636
    },
    "epoch_seconds": 268.1660285029975,
    "val_seconds": 5.846062697000889,
    "rows": 4804,
    "lr_first": 1.0000000000000001e-07,
    "lr_last": 8.206521739130436e-06,
    "optimizer_updates": 299,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T17:02:24+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 3.48238%

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.38142562011795,
    "val_metrics": {
      "map": 0.03482383159603555
    },
    "epoch_seconds": 303.4192040630005,
    "val_seconds": 5.146646225999575,
    "rows": 4804,
    "lr_first": 8.197463768115942e-06,
    "lr_last": 5.489130434782609e-06,
    "optimizer_updates": 599,
    "amp_skipped_updates": 3
  }
}
```

## 2026-10-16T17:06:19+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 3.14165%

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.297746987068882,
    "val_metrics": {
      "map": 0.031416491038201565
    },
    "epoch_seconds": 230.31866308199824,
    "val_seconds": 4.964393074998952,
    "rows": 4804,
    "lr_first": 5.480072463768117e-06,
    "lr_last": 2.7626811594202903e-06,
    "optimizer_updates": 900,
    "amp_skipped_updates": 3
  }
}
```

## 2026-10-16T17:10:07+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 3.55434%

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.258166165474949,
    "val_metrics": {
      "map": 0.0355434039644566
    },
    "epoch_seconds": 222.95218447099978,
    "val_seconds": 4.869326451000234,
    "rows": 4804,
    "lr_first": 2.7536231884057974e-06,
    "lr_last": 3.623188405797102e-08,
    "optimizer_updates": 1201,
    "amp_skipped_updates": 3
  }
}
```

## 2026-10-16T17:10:07+03:00 — recformer_ablation_trained

Recformer low_lr_warmup:4epochs trained; test not evaluated yet

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 4,
  "training_seconds": 1093.3031492580012,
  "best_trained_val_map": 0.0355434039644566
}
```

## 2026-10-16T17:11:22+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 5e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "freeze_lower6",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 53157888,
      "frozen": 94952448
    },
    "freeze_policy": "embeddings plus encoder layers0..5; dropout mode unchanged",
    "scheduler": "constant; same as original",
    "warmup_updates": 0,
    "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "b77815d134c79aa2b96770dc12cbc2e55bf63df6b237d05f36a2624a922f10a1",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-16T17:15:12+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 0.88345%

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 8.463869755909306,
    "val_metrics": {
      "map": 0.008834527132224499
    },
    "epoch_seconds": 185.62178008900082,
    "val_seconds": 5.022617935002927,
    "rows": 4804,
    "lr_first": 5e-05,
    "lr_last": 5e-05,
    "optimizer_updates": 301,
    "amp_skipped_updates": 0
  }
}
```

## 2026-10-16T17:18:26+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 1.46034%

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.409302522101866,
    "val_metrics": {
      "map": 0.014603388205361889
    },
    "epoch_seconds": 187.08664828399924,
    "val_seconds": 4.930730774998665,
    "rows": 4804,
    "lr_first": 5e-05,
    "lr_last": 5e-05,
    "optimizer_updates": 602,
    "amp_skipped_updates": 0
  }
}
```

## 2026-10-16T17:21:26+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 1.61828%

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.343921458095833,
    "val_metrics": {
      "map": 0.016182818156502365
    },
    "epoch_seconds": 172.7997656330008,
    "val_seconds": 4.68897793600263,
    "rows": 4804,
    "lr_first": 5e-05,
    "lr_last": 5e-05,
    "optimizer_updates": 903,
    "amp_skipped_updates": 0
  }
}
```

## 2026-10-16T17:24:24+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 1.98481%

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.301402692691571,
    "val_metrics": {
      "map": 0.019848101155666945
    },
    "epoch_seconds": 175.51058113700128,
    "val_seconds": 4.720026636998227,
    "rows": 4804,
    "lr_first": 5e-05,
    "lr_last": 5e-05,
    "optimizer_updates": 1204,
    "amp_skipped_updates": 0
  }
}
```

## 2026-10-16T17:24:25+03:00 — recformer_ablation_trained

Recformer freeze_lower6:4epochs trained; test not evaluated yet

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 4,
  "training_seconds": 782.3379594479993,
  "best_trained_val_map": 0.019848101155666945
}
```

## 2026-10-16T17:26:02+03:00 — recformer_ablation_measured

Recformer low_lr_warmup zero_shot: measured; replay pending

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_low_lr_warmup_seed42_v1/zero_shot"
}
```

## 2026-10-16T17:26:14+03:00 — recformer_ablation_measured

Recformer low_lr_warmup finetuned: measured; replay pending

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.0355434039644566
  },
  "test_metrics": {
    "map": 0.038575132275132276
  },
  "artifacts": "Recformer/results/hm_small_low_lr_warmup_seed42_v1/finetuned"
}
```

## 2026-10-16T17:27:58+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.026699561403508775,
        "seconds": 14.727275842000381
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03300543530543531,
        "seconds": 3.586490170997422
      },
      "checkpoint_sha256": "b8fdcc6d1904a74fe590c29b3aa61c8faaed4bbd2554cf2b6f1d5096cc1f7601"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.0355434039644566,
        "seconds": 4.598420926999097
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.038575132275132276,
        "seconds": 3.5338989489973756
      },
      "checkpoint_sha256": "1210322e9218eedbc34ce98ea770576dab59f7a8225627854c64a83aa147c6c5"
    }
  }
}
```

## 2026-10-16T17:29:27+03:00 — recformer_ablation_measured

Recformer freeze_lower6 zero_shot: measured; replay pending

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_freeze_lower6_seed42_v1/zero_shot"
}
```

## 2026-10-16T17:29:39+03:00 — recformer_ablation_measured

Recformer freeze_lower6 finetuned: measured; replay pending

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.019848101155666945
  },
  "test_metrics": {
    "map": 0.017615584415584414
  },
  "artifacts": "Recformer/results/hm_small_freeze_lower6_seed42_v1/finetuned"
}
```

## 2026-10-16T17:31:21+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.026699561403508775,
        "seconds": 14.580587559001287
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03300543530543531,
        "seconds": 3.556468978000339
      },
      "checkpoint_sha256": "b8fdcc6d1904a74fe590c29b3aa61c8faaed4bbd2554cf2b6f1d5096cc1f7601"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.019848101155666945,
        "seconds": 4.545756769999571
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.017615584415584414,
        "seconds": 3.7226175619980495
      },
      "checkpoint_sha256": "d43b705c11212141651df4901c08721680fb83b817b7ba0a4e64d6f5f3c59ed0"
    }
  }
}
```

## 2026-10-16T17:31:35+03:00 — recformer_ablation_complete

Recformer low_lr_warmup independently verified; selection byval including epoch0

Запуск: `hm_recformer_small_low_lr_warmup_seed42_v1`.

```json
{
  "status": "complete",
  "epoch": 4,
  "val_metrics": {
    "map": 0.0355434039644566
  },
  "test_metrics": {
    "map": 0.038575132275132276
  },
  "selection": {
    "selected_kind": "finetuned",
    "criterion": "validation MAP@12; zero-shot epoch0 eligible",
    "val_metrics": {
      "map": 0.0355434039644566
    },
    "test_metrics": {
      "map": 0.038575132275132276
    }
  },
  "training_seconds": 1093.3031492580012,
  "artifacts": "Recformer/results/hm_small_low_lr_warmup_seed42_v1"
}
```

## 2026-10-16T17:31:35+03:00 — recformer_ablation_complete

Recformer freeze_lower6 independently verified; selection byval including epoch0

Запуск: `hm_recformer_small_freeze_lower6_seed42_v1`.

```json
{
  "status": "complete",
  "epoch": 4,
  "val_metrics": {
    "map": 0.019848101155666945
  },
  "test_metrics": {
    "map": 0.017615584415584414
  },
  "selection": {
    "selected_kind": "zero_shot",
    "criterion": "validation MAP@12; zero-shot epoch0 eligible",
    "val_metrics": {
      "map": 0.026699561403508775
    },
    "test_metrics": {
      "map": 0.03300543530543531
    }
  },
  "training_seconds": 782.3379594479993,
  "artifacts": "Recformer/results/hm_small_freeze_lower6_seed42_v1"
}
```

## 2026-10-16T17:31:38+03:00 — recformer_ablations_report

Both Recformer ablations complete with independent replay; new comparison report generated

Запуск: `hm_recformer_ablations_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/recformer_ablations_v1",
  "comparison": [
    {
      "method": "Popularity",
      "validation_map_percent": 0.2625611648168038,
      "test_map_percent": 0.7264502164502166,
      "training_seconds": 0.0,
      "val_inference_seconds": 0.0,
      "test_inference_seconds": 0.0
    },
    {
      "method": "ID-GNN",
      "validation_map_percent": 4.4107160657325135,
      "test_map_percent": 2.6534126984126987,
      "training_seconds": 27.500700685000083,
      "val_inference_seconds": 0.0799912719999156,
      "test_inference_seconds": 0.0683340310001767
    },
    {
      "method": "ContextGNN",
      "validation_map_percent": 4.761926122123491,
      "test_map_percent": 3.01557548271834,
      "training_seconds": 20.95392044900018,
      "val_inference_seconds": 0.0675504589999036,
      "test_inference_seconds": 0.0553596439999637
    },
    {
      "method": "Two-tower GraphSAGE",
      "validation_map_percent": 1.5525635426951216,
      "test_map_percent": 0.6836767676767677,
      "training_seconds": 38.09164969699941,
      "val_inference_seconds": 0.5815334320004695,
      "test_inference_seconds": 0.6985469760002161
    },
    {
      "method": "LightGBM + manual",
      "validation_map_percent": 0.9983192672337408,
      "test_map_percent": 1.2338802308802308,
      "training_seconds": 20.122374947000026,
      "val_inference_seconds": 6.522759204999602,
      "test_inference_seconds": 5.045370581000043
    },
    {
      "method": "LightGBM + ID-GNN features",
      "validation_map_percent": 0.6853070175438595,
      "test_map_percent": 0.9666666666666666,
      "training_seconds": 5.406174842000382,
      "val_inference_seconds": 1.987061454000013,
      "test_inference_seconds": 1.7468301660001089
    },
    {
      "method": "Recformer zero_shot",
      "validation_map_percent": 2.6699561403508776,
      "test_map_percent": 3.3005435305435307,
      "training_seconds": 0.0,
      "val_inference_seconds": 6.151355272000728,
      "test_inference_seconds": 6.137794426000255
    },
    {
      "method": "Recformer finetuned",
      "validation_map_percent": 2.470220295055821,
      "test_map_percent": 1.2355555555555555,
      "training_seconds": 1255.72406289,
      "val_inference_seconds": 5.816426020001018,
      "test_inference_seconds": 4.916274175999206
    },
    {
      "method": "Recformer LR1e-5 + warmup/decay",
      "training_seconds": 1093.3031492580012,
      "validation_map_percent": 3.55434039644566,
      "val_inference_seconds": 4.69383036599902,
      "test_map_percent": 3.857513227513228,
      "test_inference_seconds": 3.959533139997802
    },
    {
      "method": "Recformer frozen embeddings + lower6",
      "training_seconds": 782.3379594479993,
      "validation_map_percent": 1.9848101155666944,
      "val_inference_seconds": 4.731954194998252,
      "test_map_percent": 1.7615584415584413,
      "test_inference_seconds": 3.9454427540003962
    }
  ],
  "results": {
    "low_lr_warmup": {
      "model": "Recformer low_lr_warmup finetuned",
      "config": {
        "seed": 42,
        "max_tokens": 256,
        "max_items": 50,
        "attributes": 3,
        "max_attr_length": 32,
        "batch": 4,
        "gradient_accumulation": 4,
        "epochs_per_stage": 2,
        "stages": 2,
        "lr": 1e-05,
        "weight_decay": 0.0,
        "precision": "FP16 autocast; FP32 normalized cosine matmul",
        "variant": "low_lr_warmup",
        "parameter_counts": {
          "total": 148110336,
          "trainable": 148110336,
          "frozen": 0
        },
        "freeze_policy": "none",
        "scheduler": "100 successful optimizer updates warmup, then linear decay over1204 updates",
        "warmup_updates": 100,
        "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
        "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
        "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
        "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
        "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
        "runner_sha256": "b77815d134c79aa2b96770dc12cbc2e55bf63df6b237d05f36a2624a922f10a1",
        "asset_manifest": {
          "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
          "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
          "backbone_repo": "allenai/longformer-base-4096",
          "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
          "files": {
            "config.json": {
              "bytes": 694,
              "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
            },
            "merges.txt": {
              "bytes": 456318,
              "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
            },
            "recformer_seqrec.bin": {
              "bytes": 749479199,
              "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
            },
            "vocab.json": {
              "bytes": 898823,
              "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
            }
          }
        },
        "runtime": {
          "torch": "2.2.2+cu118",
          "transformers": "4.46.3",
          "numpy": "1.26.4",
          "pandas": "2.2.3"
        },
        "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
      },
      "selected_stage": 2,
      "selected_epoch": 2,
      "training_and_validation_seconds": 1093.3031492580012,
      "peak_cuda_bytes_training": 3424326656,
      "val_metrics": {
        "map": 0.0355434039644566
      },
      "val_inference_seconds": 4.69383036599902,
      "test_metrics": {
        "map": 0.038575132275132276
      },
      "test_inference_seconds": 3.959533139997802,
      "selection": {
        "selected_kind": "finetuned",
        "criterion": "validation MAP@12; zero-shot epoch0 eligible",
        "val_metrics": {
          "map": 0.0355434039644566
        },
        "test_metrics": {
          "map": 0.038575132275132276
        }
      }
    },
    "freeze_lower6": {
      "model": "Recformer freeze_lower6 finetuned",
      "config": {
        "seed": 42,
        "max_tokens": 256,
        "max_items": 50,
        "attributes": 3,
        "max_attr_length": 32,
        "batch": 4,
        "gradient_accumulation": 4,
        "epochs_per_stage": 2,
        "stages": 2,
        "lr": 5e-05,
        "weight_decay": 0.0,
        "precision": "FP16 autocast; FP32 normalized cosine matmul",
        "variant": "freeze_lower6",
        "parameter_counts": {
          "total": 148110336,
          "trainable": 53157888,
          "frozen": 94952448
        },
        "freeze_policy": "embeddings plus encoder layers0..5; dropout mode unchanged",
        "scheduler": "constant; same as original",
        "warmup_updates": 0,
        "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
        "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
        "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
        "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
        "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
        "runner_sha256": "b77815d134c79aa2b96770dc12cbc2e55bf63df6b237d05f36a2624a922f10a1",
        "asset_manifest": {
          "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
          "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
          "backbone_repo": "allenai/longformer-base-4096",
          "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
          "files": {
            "config.json": {
              "bytes": 694,
              "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
            },
            "merges.txt": {
              "bytes": 456318,
              "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
            },
            "recformer_seqrec.bin": {
              "bytes": 749479199,
              "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
            },
            "vocab.json": {
              "bytes": 898823,
              "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
            }
          }
        },
        "runtime": {
          "torch": "2.2.2+cu118",
          "transformers": "4.46.3",
          "numpy": "1.26.4",
          "pandas": "2.2.3"
        },
        "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
      },
      "selected_stage": 2,
      "selected_epoch": 2,
      "training_and_validation_seconds": 782.3379594479993,
      "peak_cuda_bytes_training": 2289264640,
      "val_metrics": {
        "map": 0.019848101155666945
      },
      "val_inference_seconds": 4.731954194998252,
      "test_metrics": {
        "map": 0.017615584415584414
      },
      "test_inference_seconds": 3.9454427540003962,
      "selection": {
        "selected_kind": "zero_shot",
        "criterion": "validation MAP@12; zero-shot epoch0 eligible",
        "val_metrics": {
          "map": 0.026699561403508775
        },
        "test_metrics": {
          "map": 0.03300543530543531
        }
      }
    }
  }
}
```

## 2026-10-16T17:32:49+03:00 — recformer_ablations_final_audit

Both requested separate2+2epoch ablations complete; pipelineexit0. LR1e-5+100updatewarmup+decay val/test3.554340/3.857513percent,18.22min; frozen embeddings+lower6 atconstant5e-5 val/test1.984810/1.761558percent,13.04min. All8replays have exact full scores/top12; zero-shot matches original; frozen94.95Mweights unchanged. Epoch0/trained selection recorded pretest:lowLRtrained,freezezero-shot. Three PNGs visually checked. LowerLR+schedule beats originalfine by2.62196pp,paired95CI[0.59927,4.81070]; advantages overzero-shot/ContextGNN not established. Old artifacts and environment unchanged. Longer epochs left for separate future experiment. See reports/recformer_ablations_v1.

## 2026-10-16T17:41:06+03:00 — recformer_long_plan

User approved longer-epoch experiment. Fixed protocol: pretrained/small-v1/seed42,2stage1+up-to6stage2epochs,patience3,min4total; warmup100 to1e-5,decay tofloor1e-6 byupdate1204 thenconstant. Matched4epochcontrol copied from identical-prefix trajectory, not olddecay-to-zero run. Freeze both selections beforetest;6independentfullreplays;45mintrainingguard leaves evaluationreserve. Schedule/data/historical-runner integrity checks passed; packages unchanged.

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "preparing"
}
```

## 2026-10-16T17:42:10+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "stage1_epochs": 2,
    "stage2_max_epochs": 6,
    "stages": 2,
    "lr": 1e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "long_floor",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 148110336,
      "frozen": 0
    },
    "freeze_policy": "none",
    "scheduler": "100 successful-update warmup to1e-5; decay to1e-6 byupdate1204; constant1e-6 thereafter",
    "warmup_updates": 100,
    "lr_floor": 1e-06,
    "decay_boundary_updates": 1204,
    "stage2_patience": 3,
    "training_budget_seconds": 2700,
    "comparison_policy": "matched short best-of-first4 versus long best-of-up-to8 checkpoints on ONE identical-prefix trajectory; same schedule through first4; zero-shot also eligible separately",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog5000",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "77e56b0ecfb28be148598452efc2a47b89d9fcff99664be4ee56f39bf592fa5f",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "stage1=2,stage2<=6; stage2patience3; do not start another epoch if estimated totaltrain exceeds45min; test only after both selections fixed"
  }
}
```

## 2026-10-16T17:46:46+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 2.90758%

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 8.518538457170116,
    "val_metrics": {
      "map": 0.029075846181109342
    },
    "epoch_seconds": 231.05957080699955,
    "val_seconds": 4.46227146000092,
    "rows": 4804,
    "lr_first": 1.0000000000000001e-07,
    "lr_last": 8.385869565217392e-06,
    "optimizer_updates": 299,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T17:50:46+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 3.57807%

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.379021974130039,
    "val_metrics": {
      "map": 0.03578065072719678
    },
    "epoch_seconds": 237.0678688750013,
    "val_seconds": 4.581761284996901,
    "rows": 4804,
    "lr_first": 8.377717391304349e-06,
    "lr_last": 5.932065217391305e-06,
    "optimizer_updates": 600,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T17:54:35+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 2.86999%

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.292696339800196,
    "val_metrics": {
      "map": 0.02869994588744589
    },
    "epoch_seconds": 226.46998699200049,
    "val_seconds": 4.893202745002782,
    "rows": 4804,
    "lr_first": 5.923913043478262e-06,
    "lr_last": 3.4782608695652175e-06,
    "optimizer_updates": 901,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T17:58:45+03:00 — recformer_long_short_frozen

Matched four-epoch control checkpoint frozen; no test evaluation

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "short_best_val_map": 0.03578065072719678,
  "short_checkpoint_sha256": "ba88a315d56816dabb226ca5e46ed416dcbeba803cc103db9cdf0af529046ef1"
}
```

## 2026-10-16T17:58:45+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 3.28048%

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.253060303957238,
    "val_metrics": {
      "map": 0.03280478658768132
    },
    "epoch_seconds": 230.38570586700007,
    "val_seconds": 5.061506418998761,
    "rows": 4804,
    "lr_first": 3.4701086956521746e-06,
    "lr_last": 1.0244565217391305e-06,
    "optimizer_updates": 1202,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T18:02:37+03:00 — recformer_epoch

Recformer stage 2 epoch 3: val MAP 3.24733%

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "progress": {
    "stage": 2,
    "epoch": 3,
    "train_loss": 8.22836678589909,
    "val_metrics": {
      "map": 0.03247334719374193
    },
    "epoch_seconds": 232.30560869400142,
    "val_seconds": 5.030010975999176,
    "rows": 4804,
    "lr_first": 1.0163043478260872e-06,
    "lr_last": 1.0000000000000002e-06,
    "optimizer_updates": 1503,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-16T18:02:38+03:00 — recformer_long_trained

Recformer long:5epochs trained; selections frozen before test

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 5,
  "training_seconds": 1227.2146030080003,
  "best_trained_val_map": 0.03578065072719678
}
```

## 2026-10-16T18:04:39+03:00 — recformer_ablation_measured

Recformer long_floor zero_shot: measured; replay pending

Запуск: `hm_recformer_small_long_floor_seed42_v1_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/zero_shot"
}
```

## 2026-10-16T18:04:52+03:00 — recformer_ablation_measured

Recformer long_floor short_2plus2: measured; replay pending

Запуск: `hm_recformer_small_long_floor_seed42_v1_short_2plus2`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.03578065072719678
  },
  "test_metrics": {
    "map": 0.034388888888888886
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/short_2plus2"
}
```

## 2026-10-16T18:05:04+03:00 — recformer_ablation_measured

Recformer long_floor finetuned: measured; replay pending

Запуск: `hm_recformer_small_long_floor_seed42_v1_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.03578065072719678
  },
  "test_metrics": {
    "map": 0.034388888888888886
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/finetuned"
}
```

## 2026-10-16T18:07:21+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_recformer_small_long_floor_seed42_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.026699561403508775,
        "seconds": 17.262818507999327
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03300543530543531,
        "seconds": 4.439797627001099
      },
      "checkpoint_sha256": "b8fdcc6d1904a74fe590c29b3aa61c8faaed4bbd2554cf2b6f1d5096cc1f7601"
    },
    "short_2plus2": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03578065072719678,
        "seconds": 4.913132130001031
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.034388888888888886,
        "seconds": 3.809182041000895
      },
      "checkpoint_sha256": "ba88a315d56816dabb226ca5e46ed416dcbeba803cc103db9cdf0af529046ef1"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.03578065072719678,
        "seconds": 5.160258024003269
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.034388888888888886,
        "seconds": 4.725203219000832
      },
      "checkpoint_sha256": "ba88a315d56816dabb226ca5e46ed416dcbeba803cc103db9cdf0af529046ef1"
    }
  }
}
```

## 2026-10-16T18:07:40+03:00 — recformer_long_model_verified

Long experiment zero_shot: measured and independently verified

Запуск: `hm_recformer_small_long_floor_seed42_v1_zero_shot`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.026699561403508775
  },
  "test_metrics": {
    "map": 0.03300543530543531
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/zero_shot"
}
```

## 2026-10-16T18:07:40+03:00 — recformer_long_model_verified

Long experiment short_2plus2: measured and independently verified

Запуск: `hm_recformer_small_long_floor_seed42_v1_short_2plus2`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.03578065072719678
  },
  "test_metrics": {
    "map": 0.034388888888888886
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/short_2plus2"
}
```

## 2026-10-16T18:07:40+03:00 — recformer_long_model_verified

Long experiment finetuned: measured and independently verified

Запуск: `hm_recformer_small_long_floor_seed42_v1_finetuned`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.03578065072719678
  },
  "test_metrics": {
    "map": 0.034388888888888886
  },
  "artifacts": "Recformer/results/hm_small_long_floor_seed42_v1/finetuned"
}
```

## 2026-10-16T18:07:40+03:00 — recformer_long_report

Long Recformer experiment complete; matched short/long comparison verified

Запуск: `hm_recformer_small_long_floor_seed42_v1`.

```json
{
  "status": "complete",
  "epoch": 5,
  "val_metrics": {
    "map": 0.03578065072719678
  },
  "test_metrics": {
    "map": 0.034388888888888886
  },
  "training_summary": {
    "training_and_validation_seconds": 1227.2146030080003,
    "peak_cuda_bytes": 3424326656,
    "optimizer_updates": 1503,
    "amp_skipped_updates": 2,
    "best_trained_val_map": 0.03578065072719678,
    "short_best_trained_val_map": 0.03578065072719678,
    "short_training_and_validation_seconds": 986.7455223329998,
    "epochs": 5,
    "stop_reason": "stage2_patience3"
  },
  "bootstrap": {
    "matched_short": {
      "difference_pp": 0.0,
      "paired_user_bootstrap95_pp": [
        0.0,
        0.0
      ]
    },
    "zero_shot": {
      "difference_pp": 0.13834535834535833,
      "paired_user_bootstrap95_pp": [
        -1.083902958152958,
        1.3814873737373734
      ]
    },
    "previous_LR_warmup": {
      "difference_pp": -0.41862433862433873,
      "paired_user_bootstrap95_pp": [
        -1.299031746031746,
        0.5017460317460316
      ]
    },
    "contextgnn": {
      "difference_pp": 0.42331340617054886,
      "paired_user_bootstrap95_pp": [
        -1.1326176389747815,
        2.119103758675187
      ]
    }
  },
  "artifacts": "reports/recformer_long_v1"
}
```

## 2026-10-16T18:09:46+03:00 — external_run_reported

Пользователь сообщил: исходный hm_small_qwen_vs_llama_sql_kaggle_t4.ipynb сейчас выполняется на Kaggle. Итоговый ZIP ещё не получен; фактических новых метрик нет. Не повторять Qwen7B/Llama.

Запуск: `hm_small_qwen_llama_sql_v1`.

```json
{
  "status": "running_on_kaggle_user_reported"
}
```

## 2026-10-16T18:09:46+03:00 — kaggle_notebook_ready

Создан отдельный hm_small_qwen14b_sql_kaggle_t4.ipynb для параллельного запуска пользователем на KaggleT4. Только публичная Qwen2.5-Coder-14B-Instruct,NF4/FP16,безHF_TOKEN. Те жеInput,72813trainпар, search128/confirm88/heldout88,val304/test250/full5000,LightGBM150/31/4threads,20success/300calls/3repairs/3islands. Все4основныхмодуля побайтово совпали с работающим7B/Llama notebook; исходный notebook/архив не изменены. По уточнению пользователя импорт результатов другихLLM вKaggle убран: отчёты трёх моделей сравнить позже локально. Схема/сопоставимость/начальныйprompt/одномодельныйотчёт/графики/ZIP проверены на frozenCPUfixtures; реального14Bинференса и измеренияVRAM пока нет.

Запуск: `hm_small_qwen14b_sql_v1`.

```json
{
  "status": "notebook_ready",
  "artifacts": "LLMFeatures/kaggle/qwen14_small",
  "delivery": {
    "protocol": "hm_small_qwen14b_sql_v1",
    "notebook": "hm_small_qwen14b_sql_kaggle_t4.ipynb",
    "notebook_sha256": "50640f72158b4061f42576c286a8bcb10eb8939d9a7f5a8933ae3de225fab808",
    "parent_notebook_sha256": "173b5a4558a4a7a009b296aaa7f81240407140705fa6b3436c94f098804851f1",
    "parent_protocol": "hm_small_qwen_llama_sql_v1",
    "shared_modules_identical": {
      "features.py": "d4625f7cfe65395925a54984835a5b9536dbde586be7916deaaacbe50069efe1",
      "original_prompt.py": "0b79bb4885bf6383a6a4afb4d18828265780d691aa314e9ea917a1969951d82c",
      "worker.py": "3844f32b7a86a387725f6a5c1cc0121c8f7921aee2893e17847bd6c0c47c92a4",
      "runtime.py": "33fead39d4b655ca862921261e33345df2a22f00f483bec864b530a6f8ad10f0"
    },
    "modules": {
      "features.py": "d4625f7cfe65395925a54984835a5b9536dbde586be7916deaaacbe50069efe1",
      "original_prompt.py": "0b79bb4885bf6383a6a4afb4d18828265780d691aa314e9ea917a1969951d82c",
      "worker.py": "3844f32b7a86a387725f6a5c1cc0121c8f7921aee2893e17847bd6c0c47c92a4",
      "runtime.py": "33fead39d4b655ca862921261e33345df2a22f00f483bec864b530a6f8ad10f0",
      "runtime14.py": "a9b4dd41df4091e544f3a10e16f473c785cd47768e357499dd4e6a9da5bf331c"
    },
    "dataset": "hm_small_sql_compare_v1.zip",
    "dataset_sha256": "99197d63ad853b6dfa3b88ed10afddec076bb2c3038612622ae9ad4cfaaa8406",
    "bundle_manifest_sha256": "3cb473dfafa1d60c4922fe85e63ae5b19efe0cf76f72cfd04164030132db01a3",
    "previous_llms_required_as_input": false,
    "llm_inference_executed_locally": false
  },
  "verification": "reports/kaggle_llmfe_validation/qwen14_small_v1/verification.json"
}
```

## 2026-10-16T18:10:22+03:00 — recformer_long_final_audit

Completed: exact scores and top12 in all six independent replays; identical short/long checkpoint selected at epoch2; stopped at epoch5 by patience3; val/test MAP 3.578065/3.438889 percent; training plus validation 20.45min; pipeline exit0; all three report PNGs visually checked; CONTEXT and report updated. Previous runs preserved. Final read-only audit passed using PowerShell after a WSL command quoting error; no training rerun.

## 2026-10-16T19:20:56+03:00 — project_review

Reviewed project history, protocols, runners and latest artifacts before the next user experiment. No training started. WSL has no project training or evaluation processes; GPU idle. Long Recformer pipeline exitcode=0; verification passed. Kaggle Qwen7B/Llama remains user-reported external execution without final results; Qwen14B notebook ready. Historical evaluating/training statuses are not evidence of active processes. Existing results and environments preserved.

## 2026-10-16T19:30:27+03:00 — research_assessment

Studied TDM arXiv1801.02294v5 and JTM1902.07565v2 plus both supplied Alibaba repositories. Actual TDM implementations confirmed in XDL and TorchEasyRec; ready JTM not confirmed in checked modules. Saved pinned source snapshots and hashes, report reports/tdm_assessment/report.md, and CONTEXT entry. Main H&M adaptations: weekly multi-positive targets and negative exclusion, past-only histories, tree/node mappings, MAP@12, frozen tree plus checkpoint and replay. No training, imports of upstream code, package installs or environment changes. Next experiment not yet authorized.

## 2026-10-16T19:55:43+03:00 — tdm_smoke

TDM behavioral checks and isolated CUDA smoke passed

Запуск: `hm_tdm_small_smoke_v1`.

```json
{
  "status": "smoke_complete",
  "checks": {
    "passed": true,
    "scope": "behavioral checks and separate one-update CUDA smoke; no experiment metrics",
    "torch": "2.2.2+cu118",
    "cuda": true,
    "smoke8user_update_seconds": 0.29186208300234284,
    "peak_cuda_bytes": 98534912,
    "checks": [
      "all10dataSHA",
      "tree_reachability_nonpower2",
      "future_invariance",
      "item0_padding",
      "multi_positive_negative_exclusion",
      "equal_user_mass",
      "upstream_pooling_parity",
      "eval_batch_invariance",
      "exhaustive_beam_matches_full",
      "article_id_ties",
      "cuda_backward"
    ]
  }
}
```

## 2026-10-16T19:56:44+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 900,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "fixed",
    "run_id": "hm_tdm_small_fixed_seed42_v1",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "data_hashes": {
      "article_id_map.csv": "b2b7ada5ca21be99251bbee4ec4f334e636f4f4b1d24a75c9961a5e8a4d50b39",
      "customer_id_map.csv": "27f04807923db3ce892f0bafe8c3d28b371db0faf235895758172a4f82b0f0c3",
      "db/article.parquet": "6c2c2eaa3ed13c38dc11b5055e16f63647b2f2098653c90e4a3bbb95cb67c160",
      "db/customer.parquet": "1a4ebd5bab73cdde4f767fefe79431180b626fca9ac77de2ff775a0f353ba6cf",
      "db/transactions.parquet": "c9bf89c7213f62125f75a3071f58df5fe6127f26c38a0cac9383d617eacba21e",
      "manifest.yaml": "b1e03167a6809a00088b5f37724d78aefdb6a7a1518642d945e419510fe31f44",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "7751de2a6eafb8d8b29d23080aee0795de35ea0c6a1229d697ee473c15eec74c",
      "tasks/user-item-purchase/train.parquet": "d70a8aea2123160e502ee613af11ba5d15d4596bb060089634f243a80725ac54",
      "tasks/user-item-purchase/val.parquet": "05e7ed94146660af3dbffd86770b21aeea53c35be447740869da1ba370d72299"
    },
    "tree_sha256": "1a3886a63618901bb5f8957b46c0d197e07cebb277ddac100e6010aeb0851280",
    "prerequisite": {
      "initial_tree_seconds": 0.029822702999808826
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 440079
  }
}
```

## 2026-10-16T19:57:20+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "val_metrics": {
    "map": 0.006222587719298245
  },
  "best_epoch": 1,
  "train_loss": 0.6818496416536913
}
```

## 2026-10-16T19:57:46+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "val_metrics": {
    "map": 0.006222587719298245
  },
  "best_epoch": 1,
  "train_loss": 0.666370215964737
}
```

## 2026-10-16T19:58:14+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "best_epoch": 3,
  "train_loss": 0.6413529355026205
}
```

## 2026-10-16T19:58:36+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "best_epoch": 3,
  "train_loss": 0.5952152306373719
}
```

## 2026-10-16T19:59:00+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "best_epoch": 3,
  "train_loss": 0.5439312030374384
}
```

## 2026-10-16T19:59:28+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "best_epoch": 3,
  "train_loss": 0.4957144376391438
}
```

## 2026-10-16T19:59:53+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 7,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "best_epoch": 3,
  "train_loss": 0.45338098841566565
}
```

## 2026-10-16T19:59:53+03:00 — tdm_training_complete

TDM training complete; test not evaluated

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "trained_pending_test",
  "epoch": 7,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "artifacts": "TDM/results/hm_small_v1/fixed",
  "summary": {
    "best_epoch": 3,
    "epochs": 7,
    "best_validation_map": 0.010160103409829287,
    "training_and_validation_seconds": 188.6061899560009,
    "peak_cuda_bytes": 102302720,
    "stop_reason": "patience4",
    "checkpoint_sha256": "fec5341ae294b62220e1989c1ea10a8213985d57528f3df4a2e5f36b04c30766",
    "tree_sha256": "1a3886a63618901bb5f8957b46c0d197e07cebb277ddac100e6010aeb0851280"
  }
}
```

## 2026-10-16T20:00:06+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 900,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "cluster",
    "run_id": "hm_tdm_small_cluster_seed42_v1",
    "subset_sha256": "28c31d09b91ea8ed03e93e093182d5ad6403ceb95d07f115f86da8b8f234c096",
    "data_hashes": {
      "article_id_map.csv": "b2b7ada5ca21be99251bbee4ec4f334e636f4f4b1d24a75c9961a5e8a4d50b39",
      "customer_id_map.csv": "27f04807923db3ce892f0bafe8c3d28b371db0faf235895758172a4f82b0f0c3",
      "db/article.parquet": "6c2c2eaa3ed13c38dc11b5055e16f63647b2f2098653c90e4a3bbb95cb67c160",
      "db/customer.parquet": "1a4ebd5bab73cdde4f767fefe79431180b626fca9ac77de2ff775a0f353ba6cf",
      "db/transactions.parquet": "c9bf89c7213f62125f75a3071f58df5fe6127f26c38a0cac9383d617eacba21e",
      "manifest.yaml": "b1e03167a6809a00088b5f37724d78aefdb6a7a1518642d945e419510fe31f44",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "7751de2a6eafb8d8b29d23080aee0795de35ea0c6a1229d697ee473c15eec74c",
      "tasks/user-item-purchase/train.parquet": "d70a8aea2123160e502ee613af11ba5d15d4596bb060089634f243a80725ac54",
      "tasks/user-item-purchase/val.parquet": "05e7ed94146660af3dbffd86770b21aeea53c35be447740869da1ba370d72299"
    },
    "tree_sha256": "9697f967f52edf9e211578f80f14788671447da109aee417e32e5fe48606e75d",
    "prerequisite": {
      "source_checkpoint_sha256": "fec5341ae294b62220e1989c1ea10a8213985d57528f3df4a2e5f36b04c30766",
      "clustering_seconds": 13.290499057999114,
      "method": "recursive balanced KMeans2 distance difference; no JTM",
      "initialization": "fresh seed42; no weight warm start",
      "fixed_training_seconds": 188.6061899560009
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 440079
  }
}
```

## 2026-10-16T20:00:29+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 1,
  "val_metrics": {
    "map": 0.007104982310574416
  },
  "best_epoch": 1,
  "train_loss": 0.6062426978053772
}
```

## 2026-10-16T20:00:51+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 2,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "best_epoch": 2,
  "train_loss": 0.578748894425002
}
```

## 2026-10-16T20:01:14+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 3,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "best_epoch": 2,
  "train_loss": 0.5667671860485717
}
```

## 2026-10-16T20:01:36+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 4,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "best_epoch": 2,
  "train_loss": 0.5383922245084377
}
```

## 2026-10-16T20:01:56+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 5,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "best_epoch": 2,
  "train_loss": 0.5059755942390706
}
```

## 2026-10-16T20:02:19+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "training",
  "epoch": 6,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "best_epoch": 2,
  "train_loss": 0.46484031214184524
}
```

## 2026-10-16T20:02:19+03:00 — tdm_training_complete

TDM training complete; test not evaluated

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "trained_pending_test",
  "epoch": 6,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "artifacts": "TDM/results/hm_small_v1/cluster",
  "summary": {
    "best_epoch": 2,
    "epochs": 6,
    "best_validation_map": 0.00745875104427736,
    "training_and_validation_seconds": 132.8533849969972,
    "peak_cuda_bytes": 102302720,
    "stop_reason": "patience4",
    "checkpoint_sha256": "15692cd1b9bf8eeaedc98f1bb96ef2626d6f5bf310e1be135855667435e0b0f3",
    "tree_sha256": "9697f967f52edf9e211578f80f14788671447da109aee417e32e5fe48606e75d"
  }
}
```

## 2026-10-16T20:02:19+03:00 — tdm_pretest_frozen

Both TDM models and trees fixed before test scoring

Запуск: `hm_tdm_small_pipeline_v1`.

```json
{
  "status": "selected",
  "selection": {
    "fixed": {
      "checkpoint_sha256": "fec5341ae294b62220e1989c1ea10a8213985d57528f3df4a2e5f36b04c30766",
      "tree_sha256": "1a3886a63618901bb5f8957b46c0d197e07cebb277ddac100e6010aeb0851280",
      "summary": {
        "best_epoch": 3,
        "epochs": 7,
        "best_validation_map": 0.010160103409829287,
        "training_and_validation_seconds": 188.6061899560009,
        "peak_cuda_bytes": 102302720,
        "stop_reason": "patience4",
        "checkpoint_sha256": "fec5341ae294b62220e1989c1ea10a8213985d57528f3df4a2e5f36b04c30766",
        "tree_sha256": "1a3886a63618901bb5f8957b46c0d197e07cebb277ddac100e6010aeb0851280"
      }
    },
    "cluster": {
      "checkpoint_sha256": "15692cd1b9bf8eeaedc98f1bb96ef2626d6f5bf310e1be135855667435e0b0f3",
      "tree_sha256": "9697f967f52edf9e211578f80f14788671447da109aee417e32e5fe48606e75d",
      "summary": {
        "best_epoch": 2,
        "epochs": 6,
        "best_validation_map": 0.00745875104427736,
        "training_and_validation_seconds": 132.8533849969972,
        "peak_cuda_bytes": 102302720,
        "stop_reason": "patience4",
        "checkpoint_sha256": "15692cd1b9bf8eeaedc98f1bb96ef2626d6f5bf310e1be135855667435e0b0f3",
        "tree_sha256": "9697f967f52edf9e211578f80f14788671447da109aee417e32e5fe48606e75d"
      }
    }
  }
}
```

## 2026-10-16T20:03:40+03:00 — tdm_scored

TDM weekly MAP measured; independent replay still required

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "test_metrics": {
    "map": 0.01395194805194805
  }
}
```

## 2026-10-16T20:04:09+03:00 — tdm_scored

TDM weekly MAP measured; independent replay still required

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "test_metrics": {
    "map": 0.005512626262626263
  }
}
```

## 2026-10-16T20:06:05+03:00 — tdm_verified

All eight TDM beam/full val/test replays matched exactly

Запуск: `hm_tdm_small_pipeline_v1_inference`.

```json
{
  "status": "verified",
  "checks": {
    "fixed": {
      "beam_val": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "trace_nodes": true,
          "trace_scores": true,
          "trace_offsets": true,
          "metric_identical": true
        },
        "replay_seconds": 20.530800439002633
      },
      "beam_test": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "trace_nodes": true,
          "trace_scores": true,
          "trace_offsets": true,
          "metric_identical": true
        },
        "replay_seconds": 8.25342785900284
      },
      "full_val": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "metric_identical": true
        },
        "replay_seconds": 6.513463911003782
      },
      "full_test": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "metric_identical": true
        },
        "replay_seconds": 5.648639831000764
      }
    },
    "cluster": {
      "beam_val": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "trace_nodes": true,
          "trace_scores": true,
          "trace_offsets": true,
          "metric_identical": true
        },
        "replay_seconds": 8.829294859002403
      },
      "beam_test": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "trace_nodes": true,
          "trace_scores": true,
          "trace_offsets": true,
          "metric_identical": true
        },
        "replay_seconds": 7.020735035002872
      },
      "full_val": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "metric_identical": true
        },
        "replay_seconds": 6.217787682995549
      },
      "full_test": {
        "passed": true,
        "checks": {
          "predictions": true,
          "scores": true,
          "ap_per_user": true,
          "user_ids": true,
          "timestamps": true,
          "metric_identical": true
        },
        "replay_seconds": 5.430215631000465
      }
    }
  }
}
```

## 2026-10-16T20:06:32+03:00 — tdm_report_ready

TDM measured and replay-verified; report prepared for visual review

Запуск: `hm_tdm_small_pipeline_v1`.

```json
{
  "status": "verified_pending_visual_review",
  "artifacts": "reports/tdm_small_v1",
  "comparisons": {
    "TDM cluster beam minus TDM fixed beam": {
      "difference_pp": -0.8439321789321788,
      "paired_user_bootstrap95_pp": [
        -2.142747113997114,
        0.21910840548340527
      ]
    },
    "TDM fixed beam minus TDM fixed full": {
      "difference_pp": 0.3922756132756133,
      "paired_user_bootstrap95_pp": [
        -0.217825974025974,
        1.1273543650793647
      ]
    },
    "TDM cluster beam minus TDM cluster full": {
      "difference_pp": 0.08487373737373738,
      "paired_user_bootstrap95_pp": [
        0.007500000000000001,
        0.16881502525252523
      ]
    },
    "TDM fixed beam minus ContextGNN": {
      "difference_pp": -1.6203806775235345,
      "paired_user_bootstrap95_pp": [
        -3.843799920978492,
        0.4537329073043358
      ]
    },
    "TDM cluster beam minus ContextGNN": {
      "difference_pp": -2.4643128564557135,
      "paired_user_bootstrap95_pp": [
        -4.3847107125678555,
        -0.7609954476740202
      ]
    },
    "TDM fixed beam minus Recformer LR/warmup": {
      "difference_pp": -2.4623184223184222,
      "paired_user_bootstrap95_pp": [
        -4.864092352092351,
        -0.19301960076960162
      ]
    },
    "TDM cluster beam minus Recformer LR/warmup": {
      "difference_pp": -3.3062506012506017,
      "paired_user_bootstrap95_pp": [
        -5.436087662337663,
        -1.394525853775854
      ]
    }
  }
}
```

## 2026-10-16T20:07:52+03:00 — tdm_complete

TDM weekly run complete; independent replay and visual report checks passed

Запуск: `hm_tdm_small_fixed_seed42_v1`.

```json
{
  "status": "complete",
  "epoch": 7,
  "val_metrics": {
    "map": 0.010160103409829287
  },
  "test_metrics": {
    "map": 0.01395194805194805
  },
  "artifacts": "TDM/results/hm_small_v1/fixed",
  "summary": {
    "best_epoch": 3,
    "epochs": 7,
    "best_validation_map": 0.010160103409829287,
    "training_and_validation_seconds": 188.6061899560009,
    "peak_cuda_bytes": 102302720,
    "stop_reason": "patience4",
    "checkpoint_sha256": "fec5341ae294b62220e1989c1ea10a8213985d57528f3df4a2e5f36b04c30766",
    "tree_sha256": "1a3886a63618901bb5f8957b46c0d197e07cebb277ddac100e6010aeb0851280"
  }
}
```

## 2026-10-16T20:07:52+03:00 — tdm_complete

TDM weekly run complete; independent replay and visual report checks passed

Запуск: `hm_tdm_small_cluster_seed42_v1`.

```json
{
  "status": "complete",
  "epoch": 6,
  "val_metrics": {
    "map": 0.00745875104427736
  },
  "test_metrics": {
    "map": 0.005512626262626263
  },
  "artifacts": "TDM/results/hm_small_v1/cluster",
  "summary": {
    "best_epoch": 2,
    "epochs": 6,
    "best_validation_map": 0.00745875104427736,
    "training_and_validation_seconds": 132.8533849969972,
    "peak_cuda_bytes": 102302720,
    "stop_reason": "patience4",
    "checkpoint_sha256": "15692cd1b9bf8eeaedc98f1bb96ef2626d6f5bf310e1be135855667435e0b0f3",
    "tree_sha256": "9697f967f52edf9e211578f80f14788671447da109aee417e32e5fe48606e75d"
  }
}
```

## 2026-10-16T20:07:52+03:00 — tdm_pipeline_complete

Completed both authorized TDM small-v1 experiments. Fixed tree:7epochs,best3, beam val/test1.016010/1.395195 percent; exhaustive same checkpoint0.934150/1.002919 percent. Cluster tree:6epochs,best2,beam0.745875/0.551263 percent; exhaustive0.672455/0.466389 percent. Train+validation188.61s and132.85s; clustering13.29s; peak allocated CUDA102302720bytes each. Both selections fixed before test. All8 independent replays exact, final artifact audit passed, all3 PNGs visually checked, pipeline exit0. Local adaptation,one seed250testusers; cluster-minus-fixed beam bootstrap95 percent interval[-2.14275,+0.21911]pp, so robust general harm/benefit not established. Single-pass beam test7.86/7.18s versus full5.49/5.26s despite986/988 versus5000 scored nodes per user. No package/environment changes; earlier results preserved. Source snapshot retained.

Запуск: `hm_tdm_small_pipeline_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/tdm_small_v1",
  "verification": "TDM/results/hm_small_v1/verification.json",
  "final_audit": "reports/tdm_small_v1/final_audit.json"
}
```

## 2026-10-16T20:52:30+03:00 — kaggle_small_llm_audited

Qwen7B_LightGBM: реальный Kaggle запуск проверен;20успешных/67вызовов,candidate5; val/testMAP=0.777180/1.107143%. Совпали72813trainпар/source/model/programSHA/выборпоconfirmation. НезависимыйCPUreplay точно совпал top12/AP/MAP. Безобучения/новойгенерации/выборапоtest.

Запуск: `hm_small_qwen_llama_sql_v1_2ecc60d61fd4_qwen`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.007771796916533759
  },
  "test_metrics": {
    "map": 0.01107142857142857
  },
  "artifacts": "reports/hm_small_llms_v1",
  "selected_call": 5,
  "llm_calls": 67,
  "evaluated_distinct": 20
}
```

## 2026-10-16T20:52:30+03:00 — kaggle_small_llm_audited

Llama8B_LightGBM: реальный Kaggle запуск проверен;20успешных/201вызовов,candidate144; val/testMAP=0.843960/0.780337%. Совпали72813trainпар/source/model/programSHA/выборпоconfirmation. НезависимыйCPUreplay точно совпал top12/AP/MAP. Безобучения/новойгенерации/выборапоtest.

Запуск: `hm_small_qwen_llama_sql_v1_2ecc60d61fd4_llama`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.008439600421508316
  },
  "test_metrics": {
    "map": 0.007803367003367003
  },
  "artifacts": "reports/hm_small_llms_v1",
  "selected_call": 144,
  "llm_calls": 201,
  "evaluated_distinct": 20
}
```

## 2026-10-16T20:52:30+03:00 — kaggle_small_llm_audited

Qwen14B_LightGBM: реальный Kaggle запуск проверен;20успешных/45вызовов,candidate14; val/testMAP=1.211209/0.743306%. Совпали72813trainпар/source/model/programSHA/выборпоconfirmation. НезависимыйCPUreplay точно совпал top12/AP/MAP. Безобучения/новойгенерации/выборапоtest.

Запуск: `hm_small_qwen14b_sql_v1_f373011050bf`.

```json
{
  "status": "complete",
  "val_metrics": {
    "map": 0.01211209447229184
  },
  "test_metrics": {
    "map": 0.00743305785123967
  },
  "artifacts": "reports/hm_small_llms_v1",
  "selected_call": 14,
  "llm_calls": 45,
  "evaluated_distinct": 20
}
```

## 2026-10-16T20:52:31+03:00 — kaggle_small_llms_comparison

Оба ZIP проверены,все60программ. Qwen7Btest1.107143%,Llama8B0.780337%,Qwen14B0.743306%; Raw0.959630%,manual1.233880%,ContextGNN3.015575%. У14B45calls против67/201,но генерация71.61мин против46.42/262.10мин. Выбранные14B/Llama historyагрегатытолькоcustomer_id;Qwen7B включаетcategory/customer×department;причинностьне установлена. Report/таблицы/5PNG/bootstrap10kготовы. Одинseed250test,точечныйпорядокне доказываетустойчивоепревосходство. ИзначальныйWSLстекотклонилnullableboolLlama;точныеCPUверсииKaggleустановленыизолированновaudit_deps,старыеenvне менялись. 4модели×val/testreplayточносовпали. Никакогообучения/измененияисходныхZIP.

Запуск: `hm_small_llms_comparison_v1`.

```json
{
  "status": "complete",
  "artifacts": "reports/hm_small_llms_v1",
  "audit": "reports/hm_small_llms_v1/audit.json",
  "report": "reports/hm_small_llms_v1/report.md",
  "bootstrap": "reports/hm_small_llms_v1/paired_test_bootstrap.csv"
}
```

## 2026-10-16T20:52:31+03:00 — external_run_audited

Kaggle запуск завершён и проверен; фактические результаты отдельно: hm_small_qwen_llama_sql_v1_2ecc60d61fd4

Запуск: `hm_small_qwen_llama_sql_v1`.

```json
{
  "status": "completed_on_kaggle_audited",
  "actual_run_id": "hm_small_qwen_llama_sql_v1_2ecc60d61fd4",
  "artifacts": "reports/hm_small_llms_v1"
}
```

## 2026-10-16T20:52:31+03:00 — external_run_audited

Kaggle запуск завершён и проверен; фактические результаты отдельно: hm_small_qwen14b_sql_v1_f373011050bf

Запуск: `hm_small_qwen14b_sql_v1`.

```json
{
  "status": "completed_on_kaggle_audited",
  "actual_run_id": "hm_small_qwen14b_sql_v1_f373011050bf",
  "artifacts": "reports/hm_small_llms_v1"
}
```

## 2026-10-16T21:14:45+03:00 — qwen7_generation_error_analysis

Пользователь выбрал Qwen2.5-Coder-7B-Instruct. Разобраны67реальныхответовsmall-v1: 20валидных/30отказов/17дубликатов;JSON67/67,обрезаний0. Первыеошибки9строковыхрезультатов,8OVER,6keys, 4history-в-derived,2SQLsyntax,1ID-в-derived. У18ответов несколько проблемныхfeatures;13/40repair возвращаютнеизменённуюпрограмму(7отказов,6дубликатов).9/17дубликатов=candidate001. Сохраненывсеошибкипоfeatures/цепочки/примеры/promptaddendum/repairtemplate;SQLпримерыEXPLAIN-проверены DuckDB1.4.1насинтетическойсхеме. Нетгенерации/обучения/переоценкиMAP/измененийрабочихноутбуков. H003A/B/CвHYPOTHESES.md предложены,не запущены. Устойчивое превосходство7Bне доказано;testуже просмотрен.

```json
{
  "artifacts": "reports/qwen7b_generation_errors_v1",
  "analysis": "reports/qwen7b_generation_errors_v1/analysis.json",
  "chosen_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
  "proposed_hypothesis": "H003",
  "experiment_started": false
}
```

## 2026-10-16T21:29:47+03:00 — gitignore_updated

По просьбе пользователя исключены из Git зависимости аудита, установщик pip, распакованные результаты Kaggle, архивы результатов и временные SQL/scratch файлы. Сам .gitignore остаётся игнорируемым. Код, ноутбуки, отчёты и история сохранены; файлы не удалялись, индекс Git не менялся.

## 2026-10-16T21:40:32+03:00 — h003_kaggle_notebook_prepared

Подготовлен отдельный Kaggle T4 ноутбук H003 для Qwen2.5-Coder-7B-Instruct: A/AB/ABC, те же72813пары иSQLинтерфейс; CPU smoke/67историческихответов проверены. Реальная LLM-генерация H003 не выполнялась; старые эксперименты сохранены.

```json
{
  "notebook": "LLMFeatures/kaggle/hm_small_qwen7b_h003_kaggle_t4.ipynb",
  "verification": "reports/kaggle_llmfe_validation/h003_small_v1/verification.json",
  "protocol": "hm_small_qwen7b_h003_v1",
  "actual_llm_experiment_started": false
}
```

## 2026-10-16T22:49:09+03:00 — h003_context_checked

Точный токенизатор закреплённой Qwen7B: реконструированы201 H003-промпт по67историческимобращениям. Максимумы входа A2693/B3184/C3297 при6144; примеры491токен. Включены system/chat template/repair. Будущие ответы не гарантируются; runtime проверяет длину без обрезки. Веса не загружались, генерации не было. Артефакт reports/kaggle_llmfe_validation/h003_small_v1/context_budget.json.

## 2026-10-17T09:27:39+03:00 — h003_kaggle_arm_audited

h003a:20измеренных/65вызовов;отказов36,дубликатов9; val/testMAP=0.642195/0.751212%. Верифицированы данные/исходники/selection/frozen CPU replay. Без обучения/новой генерации.

Запуск: `hm_small_qwen7b_h003_v1_6852748fc0e4_h003a`.

```json
{
  "status": "complete",
  "artifacts": "reports/h003_small_v1",
  "val_metrics": {
    "map": 0.006421949760765549
  },
  "test_metrics": {
    "map": 0.007512121212121212
  },
  "llm_calls": 65,
  "evaluated_distinct": 20,
  "selected_call": 58
}
```

## 2026-10-17T09:27:39+03:00 — h003_kaggle_arm_audited

h003b:20измеренных/78вызовов;отказов21,дубликатов37; val/testMAP=0.712666/0.873593%. Верифицированы данные/исходники/selection/frozen CPU replay. Без обучения/новой генерации.

Запуск: `hm_small_qwen7b_h003_v1_6852748fc0e4_h003b`.

```json
{
  "status": "complete",
  "artifacts": "reports/h003_small_v1",
  "val_metrics": {
    "map": 0.007126658976987924
  },
  "test_metrics": {
    "map": 0.008735930735930736
  },
  "llm_calls": 78,
  "evaluated_distinct": 20,
  "selected_call": 31
}
```

## 2026-10-17T09:27:39+03:00 — h003_kaggle_arm_audited

h003c:20измеренных/51вызовов;отказов15,дубликатов16; val/testMAP=0.841421/0.888745%. Верифицированы данные/исходники/selection/frozen CPU replay. Без обучения/новой генерации.

Запуск: `hm_small_qwen7b_h003_v1_6852748fc0e4_h003c`.

```json
{
  "status": "complete",
  "artifacts": "reports/h003_small_v1",
  "val_metrics": {
    "map": 0.0084142054947976
  },
  "test_metrics": {
    "map": 0.008887445887445888
  },
  "llm_calls": 51,
  "evaluated_distinct": 20,
  "selected_call": 8
}
```

## 2026-10-17T09:27:39+03:00 — h003_kaggle_results_audited

H003 полностью проверен: A65/36/9,B78/21/37,C51/15/16 (calls/reject/duplicate), каждый20успехов. Cпротивконтроля67calls:на23.9%меньшеобращений,44.88против46.42мингенерации. TestMAP A0.751212/B0.873593/C0.888745% противстарогоQwen7B1.107143% иraw0.959630%; качество не улучшилось. Все4модели×val/test frozenreplayсовпали. A21–23derivedагрегациипропущеныдиагностикой,остановленыpreflight. 9WITHINGROUPвыраженийоказалисьневалиднымquantile_contдиалектом,ложныхотказовсрединихнет. Одинseed250test,повторнаяоценка;всеbootstrapинтервалыразницывключают0.

Запуск: `hm_small_qwen7b_h003_v1_6852748fc0e4`.

```json
{
  "status": "complete",
  "artifacts": "reports/h003_small_v1",
  "report": "reports/h003_small_v1/report.md",
  "test_previously_inspected": true
}
```

## 2026-10-17T10:44:11+03:00 — full_sql_kaggle_notebook_prepared

По поручению пользователя подготовлен отдельный Kaggle T4 ноутбук Qwen7B full SQL: обычные SELECT/WITH без JSON,host проверяет и присоединяет числовые таблицы признаков. Те же72813пары/LightGBM150/31/4threads/3популяции/20успехов/300calls/3repair. CPU smoke с заданными SQL ответами прошёл,rawконтроль byte-identical, CTE/quantile/window/pandas/future exclusion/ключи/routing/resume/replay/ZIP проверены. Реальной LLM-генерации нет; GPU запустит пользователь.

```json
{
  "notebook": "LLMFeatures/kaggle/hm_small_qwen7b_full_sql_kaggle_t4.ipynb",
  "protocol": "hm_small_qwen7b_full_sql_v1",
  "hypothesis": "H004",
  "verification": "reports/kaggle_llmfe_validation/full_sql_small_v1/verification.json",
  "context_counts": {
    "initial": 1340,
    "example_repair": 2040,
    "large_six_query_repair": 5866,
    "large_duplicate_repair": 5443
  },
  "actual_llm_experiment_started": false
}
```

## 2026-10-17T10:56:22+03:00 — provider_feature_search_started

Запущен реальный GPT-6.1-Sol через tookен.club: small-v1/fullSQL,20успехов/300calls,данныеиLightGBMпрежние. Токен только в памяти.

Запуск: `hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0",
  "model": "gpt-6.1-sol"
}
```

## 2026-10-17T11:03:16+03:00 — provider_feature_search_progress

GPT-6.1-Sol API fullSQL: сейчас11/20оценённых,14/300обращений. Тотжеsmall-v1/72813пары/LightGBM150/31/4CPU;поискнеиспользуетtest,промежуточныйsearchMAPнеитоговыйрезультат.

Запуск: `hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0",
  "evaluated_distinct": 11,
  "llm_calls": 14
}
```

## 2026-10-17T11:07:09+03:00 — provider_validator_bug_identified

Дофинальногоselection/test обнаруженложныйотказ APIcall14:SQLGlot считаетAND exp.Func,allowlistнеучёллогическиеоператоры. План:сохранитьисходныйv1,изолированноисправитьвалидатор,переоценитьтотжепотокответовбезновыхAPIвызовов,взятьпервые20валидныхпоисправленнойпроверке,выбратьтолькопоvalidation. Неизменятьстарыеисходники/метрики. Этоисправленныйreplay,ненезависимыйLLMпрогон.

## 2026-10-17T11:11:45+03:00 — provider_feature_search_finished

API поиск завершён,выборзафиксировандоtest,отчётсохранён. Требуетсялокальныйаудитпередитоговымвыводом.

Запуск: `hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0`.

```json
{
  "status": "completed_pending_audit",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0"
}
```

## 2026-10-17T11:13:38+03:00 — provider_corrected_evaluation_selected

Исправленныйsaved-streamreplay:первые20валидных,selectionпоvalidationзафиксирован. ДополнительныхAPIвызовов0;этоНЕнезависимыйLLMпрогон.

Запуск: `hm_small_gpt61sol_full_sql_corrected_eval_v2_ffbd51c51899`.

```json
{
  "status": "evaluating",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_sql_corrected_eval_v2_ffbd51c51899",
  "source_run": "hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0"
}
```

## 2026-10-17T11:19:53+03:00 — provider_feature_experiment_audited

Поиск GPT-6.1 Sol завершён и независимо проверен. 20 оценённых наборов; test MAP@12 0.979030%, raw 0.959630%, прежний Qwen7B 1.107143%. Преимущество по качеству не подтверждено. Исходный поток: 26 API обращений, 5 дубликатов и один ложный отказ AND.

Запуск: `hm_small_gpt61sol_full_sql_seed42_v1_f33bb22767c0`.

```json
{
  "status": "complete",
  "artifacts": "reports/gpt61sol_small_v1",
  "evaluated_distinct": 20,
  "api_requests": 26,
  "source_api_requests": 26,
  "val_metrics": {
    "map": 0.007914435710488343
  },
  "test_metrics": {
    "map": 0.009790303030303031
  },
  "independent_audit": "passed",
  "independent_llm_run": true
}
```

## 2026-10-17T11:19:53+03:00 — provider_feature_experiment_audited

Поиск GPT-6.1 Sol завершён и независимо проверен. 20 оценённых наборов; test MAP@12 0.979030%, raw 0.959630%, прежний Qwen7B 1.107143%. Преимущество по качеству не подтверждено. Исправленная оценка сохранённого потока: первые 20 валидных за 24 ответа, 4 дубликата, без отказов; дополнительных API обращений 0. Это не независимый LLM запуск. Выбран тот же candidate_004.

Запуск: `hm_small_gpt61sol_full_sql_corrected_eval_v2_ffbd51c51899`.

```json
{
  "status": "complete",
  "artifacts": "reports/gpt61sol_small_v2",
  "evaluated_distinct": 20,
  "api_requests": 0,
  "source_api_requests": 26,
  "val_metrics": {
    "map": 0.007914435710488343
  },
  "test_metrics": {
    "map": 0.009790303030303031
  },
  "independent_audit": "passed",
  "independent_llm_run": false
}
```

## 2026-10-17T11:19:53+03:00 — provider_feature_experiment_summary

H005 завершена: 20 наборов, 26 API запросов, независимый аудит пройден. Полный SQL исполняется успешно, но преимущество по MAP не подтверждено. Исправление ложного AND отказа не изменило выбранный набор и итоговые метрики.

```json
{
  "artifacts": "reports/gpt61sol_small_v2",
  "seed": 42,
  "test_users": 250
}
```

## 2026-10-17T11:29:04+03:00 — provider_python_protocol_registered

H006: отдельный Python эксперимент с прежними данными и LightGBM. 300 обращений максимум / 20 оценённых наборов. Валидатор проверяется до генерации, все реальные отказы будут разобраны отдельно.

Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "prepared",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:29:25+03:00 — provider_python_search_started

H006: реальный GPT-6.1 Sol пишет полную Python функцию. Те же 72813 пар / LightGBM150/31 / seed42 / 20 наборов / 300 API вызовов. Предварительная проверка валидатора пройдена. Test не используется при отборе.

Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:31:09+03:00 — provider_python_search_interrupted

API HTTP502: <html>
<head><title>502 Bad Gateway</title></head>
<body>
<center><h1>502 Bad Gateway</h1></center>
<hr><center>nginx/1.24.0 (Ubuntu)</center>
</body>
</html>


Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "interrupted",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:32:13+03:00 — provider_python_api_outage

После 3 валидных программ провайдер ответил HTTP502 на API attempt4. Ошибка сохранена отдельно и не считается ошибкой Python/валидатора. Возобновляем тот же поток; неудачный POST входит в лимит300.

Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "resuming"
}
```

## 2026-10-17T11:32:29+03:00 — provider_python_search_started

H006: реальный GPT-6.1 Sol пишет полную Python функцию. Те же 72813 пар / LightGBM150/31 / seed42 / 20 наборов / 300 API вызовов. Предварительная проверка валидатора пройдена. Test не используется при отборе.

Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:35:58+03:00 — provider_python_search_interrupted



Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "interrupted",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:38:42+03:00 — provider_python_validator_v1_preserved

Исходный Pythonv1 сохранён. Дополнительная проверка нашла другой порядок одинаковых столбцов на пустой историиcall5; v2 выравнивает столбцы поименам и добавляет empty/absent preflight. 7 оценённых наборов,8 сохранённых ответов,9 POST включая502. Перенос без сбросаAPIбюджета, до итогового отбора/test.

Запуск: `hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1`.

```json
{
  "status": "superseded_validator_v2"
}
```

## 2026-10-17T11:39:25+03:00 — provider_python_validator_migration

До итогового отбора найдена нестабильность порядка столбцов на пустой истории в call5. v2 выравнивает столбцы по именам и добавляет empty/absent preflight. Исходный поток сохранён; модели переиспользованы только после совпадения матриц. API запросов для миграции0, общий лимит300 не обнуляется.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "prepared",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449",
  "source_run": "hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T11:39:25+03:00 — provider_python_search_started

H006: реальный GPT-6.1 Sol пишет полную Python функцию. Те же 72813 пар / LightGBM150/31 / seed42 / 20 наборов / 300 API вызовов. Предварительная проверка валидатора пройдена; v2 выравнивает столбцы и проверяет пустую историю. Test не используется при отборе.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449"
}
```

## 2026-10-17T11:41:17+03:00 — provider_python_progress

H006 Pythonv2: 10/20 полностью оценённых наборов, 11/300 фактических API запросов. Бюджет включает исходные9POST v1. v1 сохранён; v2 выравнивает столбцы по именам и проверяет пустую историю. 29 регрессий пройдено, два реальных набора (11+17 признаков) совпали с независимым SQL по8срезам. Неограниченный exec был отклонён автоматической проверкой безопасности и не выполнялся; проверки модельного кода идут через ограниченный wrapper.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "searching",
  "api_requests": 11,
  "evaluated_distinct": 10,
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449"
}
```

## 2026-10-17T11:43:31+03:00 — provider_python_hypothesis_clarified

Пользователь справедливо указал: текущие агрегаты выразимы иSQL иPython. Нет оснований ожидать превосходства Python как языка. H006 сравнивает результат поиска через разные интерфейсы/промпты; одинаковые матрицы с теми же настройкамиLightGBM дают одинаковое обучение. Активный протокол не изменён.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "searching"
}
```

## 2026-10-17T11:47:00+03:00 — tdm_next_experiments_proposed

User asked which TDM experiments could establish potential. Proposed validation-only routing/history diagnostics, a matched leaf-only DNN versus new TDM control, separate weekly-loss and negative-allocation ablations, then conditional tree/features/JTM and scale checks. Plan saved in reports/tdm_assessment/next_experiments.md. Proposals only: no training launched, no active LLM protocol or environment changed. Previously viewed test must not be used for tuning; confirm promising results across seeds and additional temporal holdout.

## 2026-10-17T11:54:29+03:00 — provider_python_search_finished

Python эксперимент завершён; требуется независимый аудит. Отбор заморожен до test.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "completed_pending_audit",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449"
}
```

## 2026-10-17T11:56:22+03:00 — provider_python_prompt_log_reconciled

Независимый аудит нашёл неточность лога приresume call8: prompt.txt был заменён реконструированнымv2 текстом, хотя ответ повторно не запрашивался. Фактически отправленныйprompt восстановлен из неизменного APIrequest (совпадаетсv1); неотправленный текст сохранён отдельно. Данные, код модели, отбор и метрики не менялись.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "completed_pending_audit",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_python_seed42_v2_db3ced2f4449"
}
```

## 2026-10-17T11:59:40+03:00 — provider_python_experiment_audited

H006 завершена и независимо проверена: Python test MAP@12 1.357362%, validation 1.079708%; SQL 0.979030%, прежний Qwen7B 1.107143%, raw 0.959630%. 20 оценённых программ, 22 фактическихAPIPOST в одном потоке; отказовкода 1, дубликатов 0, ошибокAPI 1. v1 сохранён, исправлениеv2 выполнено до итогового выбора/test без повторной генерации первых8ответов. 29 регрессий, дополнительный разбор всех ответов и независимые SQL эталоны пройдены. Численно различных train-матриц 18 из20; confirmation-кандидаты численно различаются. Все12признаков победителя выраженыSQL и дают точно те жеfloat32 значения на всех72813train-парах. Одинseed/250ранее просмотренныхtest пользователей; это диагностическое сравнение, не воспроизведение статьи.

Запуск: `hm_small_gpt61sol_python_seed42_v2_db3ced2f4449`.

```json
{
  "status": "complete",
  "artifacts": "reports/gpt61sol_python_v1",
  "api_requests": 22,
  "evaluated_distinct": 20,
  "val_metrics": {
    "map": 0.010797076339839498
  },
  "test_metrics": {
    "map": 0.013573617123617125
  },
  "independent_audit": "passed",
  "validator_audit": "passed",
  "source_run": "hm_small_gpt61sol_python_seed42_v1_8b3ac9a151c1"
}
```

## 2026-10-17T12:10:04+03:00 — authored20_protocol_registered

H007: пользователь поручил текущей сессии Codex самостоятельно написать и оценить ровно20 наборов. Адаптивный поиск по3популяциям, выбор родителей поsearch. Те же72813пары/LightGBM150/31/4CPU/seed42. Точная модель сессии не аттестована; сравнение не доказывает подмену провайдером. Текущая сессия знает историю, ограничение2048токенов к ней не применяется. Черновики не обучались; только20зафиксированных перед оценкой предложений будут оценены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "prepared",
  "artifacts": "LLMFeatures/results/hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9",
  "planned_sets": 20,
  "api_requests": 0
}
```

## 2026-10-17T12:11:52+03:00 — authored20_candidate_committed

Зафиксирован набор1/20, популяция0, родительNone. 12 новых признаков. Решение записано до получения егоMAP. Начальная популяция0: компактная временная основа и повторные покупки. Контроль — raw15; новые метрики ещё не известны.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 1,
  "evaluated_sets": 0,
  "api_requests": 0
}
```

## 2026-10-17T12:12:13+03:00 — authored20_candidate_evaluated

Набор1/20 оценён: searchMAP@12 1.526199%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 1,
  "committed_sets": 1,
  "api_requests": 0
}
```

## 2026-10-17T12:13:17+03:00 — authored20_candidate_committed

Зафиксирован набор2/20, популяция1, родительNone. 21 новых признаков. Решение записано до получения егоMAP. Начальная популяция1 независимо от популяции0. Проверяю близость кандидата к личной истории продуктовых семей и типов, с поправкой на глобальную популярность.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 2,
  "evaluated_sets": 1,
  "api_requests": 0
}
```

## 2026-10-17T12:13:31+03:00 — authored20_candidate_evaluated

Набор2/20 оценён: searchMAP@12 0.931328%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 2,
  "committed_sets": 2,
  "api_requests": 0
}
```

## 2026-10-17T12:13:31+03:00 — authored20_candidate_committed

Зафиксирован набор3/20, популяция2, родительNone. 23 новых признаков. Решение записано до получения егоMAP. Начальная популяция2: считаю сходство разных категорий по общим покупателям на прошлой90-дневной истории, убирая диагональ. Этот коллективный сигнал дополняет личные частоты; валидационных результатов ещё нет.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 3,
  "evaluated_sets": 2,
  "api_requests": 0
}
```

## 2026-10-17T12:14:03+03:00 — authored20_candidate_evaluated

Набор3/20 оценён: searchMAP@12 1.197607%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 3,
  "committed_sets": 3,
  "api_requests": 0
}
```

## 2026-10-17T12:14:58+03:00 — authored20_candidate_committed

Зафиксирован набор4/20, популяция0, родитель1. 20 новых признаков. Решение записано до получения егоMAP. Родитель1 дал search1.526199%. Сохраняю все12признаков, добавляю относительные короткие/длинные тренды товара и пользователя и тренды типов/секций. Это проверка, помогает ли свежесть популярности сверх абсолютных счётчиков.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 4,
  "evaluated_sets": 3,
  "api_requests": 0
}
```

## 2026-10-17T12:15:12+03:00 — authored20_candidate_evaluated

Набор4/20 оценён: searchMAP@12 1.203046%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 4,
  "committed_sets": 4,
  "api_requests": 0
}
```

## 2026-10-17T12:15:12+03:00 — authored20_candidate_committed

Зафиксирован набор5/20, популяция1, родитель2. 25 новых признаков. Решение записано до получения егоMAP. Родитель2 дал search0.931328%. Узкая продуктовая семья может иметь мало повторений; убираю её отдельные счётчики, сохраняю тип и добавляю более общие секцию/цвет, их давность и30-дневные доли. Ценовой разрыв и разнообразие дополняют сигналы пользователя.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 5,
  "evaluated_sets": 4,
  "api_requests": 0
}
```

## 2026-10-17T12:15:25+03:00 — authored20_candidate_evaluated

Набор5/20 оценён: searchMAP@12 1.765715%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 5,
  "committed_sets": 5,
  "api_requests": 0
}
```

## 2026-10-17T12:15:25+03:00 — authored20_candidate_committed

Зафиксирован набор6/20, популяция2, родитель3. 26 новых признаков. Решение записано до получения егоMAP. Родитель3 дал search1.197607%. Делаю коллективный сигнал менее разреженным: оставляю типы/секции, добавляю365-дневный горизонт вместо графов цвета/группы одежды. Дополняю недавними личными предпочтениями и относительным ценовым отклонением.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 6,
  "evaluated_sets": 5,
  "api_requests": 0
}
```

## 2026-10-17T12:16:03+03:00 — authored20_candidate_evaluated

Набор6/20 оценён: searchMAP@12 1.791295%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 6,
  "committed_sets": 6,
  "api_requests": 0
}
```

## 2026-10-17T12:16:51+03:00 — authored20_candidate_committed

Зафиксирован набор7/20, популяция0, родитель1. 19 новых признаков. Решение записано до получения егоMAP. Расширение4 дало1.203046% против1.526199% у1; возвращаюсь к лучшему родителю1. Вместо множества отношений окон добавляю экспоненциальное затухание14/30дней и долю/относительную давность повторных покупок.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 7,
  "evaluated_sets": 6,
  "api_requests": 0
}
```

## 2026-10-17T12:17:06+03:00 — authored20_candidate_evaluated

Набор7/20 оценён: searchMAP@12 1.473214%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 7,
  "committed_sets": 7,
  "api_requests": 0
}
```

## 2026-10-17T12:17:06+03:00 — authored20_candidate_committed

Зафиксирован набор8/20, популяция1, родитель5. 31 новых признаков. Решение записано до получения егоMAP. Набор5 улучшил собственную ветку с0.931328% до1.765715%. Сохраняю его25признаков и добавляю затухающие предпочтения типа/секции/цвета, вес повторной покупки и масштабированное ценовое отклонение. Проверяю непрерывную давность сверх фиксированного30-дневного окна.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 8,
  "evaluated_sets": 7,
  "api_requests": 0
}
```

## 2026-10-17T12:17:20+03:00 — authored20_candidate_evaluated

Набор8/20 оценён: searchMAP@12 2.148015%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 8,
  "committed_sets": 8,
  "api_requests": 0
}
```

## 2026-10-17T12:17:21+03:00 — authored20_candidate_committed

Зафиксирован набор9/20, популяция2, родитель6. 26 новых признаков. Решение записано до получения егоMAP. Набор6 поднял search ветки с1.197607% до1.791295%, но изменял несколько компонентов сразу. Проверяю более простой вариант с365-дневными графами типов/секций;90-дневные убираю, добавляю разнообразие пользователя и число уникальных покупателей товара. Остальные признаки6 сохраняю.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 9,
  "evaluated_sets": 8,
  "api_requests": 0
}
```

## 2026-10-17T12:17:47+03:00 — authored20_candidate_evaluated

Набор9/20 оценён: searchMAP@12 1.806486%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 9,
  "committed_sets": 9,
  "api_requests": 0
}
```

## 2026-10-17T12:18:47+03:00 — authored20_candidate_committed

Зафиксирован набор10/20, популяция0, родитель1. 19 новых признаков. Решение записано до получения егоMAP. В этой популяции и тренды4(1.203046%), и затухание7(1.473214%) не обошли1(1.526199%). Снова беру1, проверяю другое направление: историческую цену кандидата относительно среднего/разброса бюджета пользователя и цены типа.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 10,
  "evaluated_sets": 9,
  "api_requests": 0
}
```

## 2026-10-17T12:19:01+03:00 — authored20_candidate_evaluated

Набор10/20 оценён: searchMAP@12 1.049624%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 10,
  "committed_sets": 10,
  "api_requests": 0
}
```

## 2026-10-17T12:19:01+03:00 — authored20_candidate_committed

Зафиксирован набор11/20, популяция1, родитель8. 36 новых признаков. Решение записано до получения егоMAP. Набор8 улучшил5 с1.765715% до2.148015%, поэтому сохраняю все31признак8. Добавляю разницу между давностью категории и последней покупкой пользователя, ценовой межквартильный размах и совместимость исторического канала. Получается36признаков — прежний предел.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 11,
  "evaluated_sets": 10,
  "api_requests": 0
}
```

## 2026-10-17T12:19:15+03:00 — authored20_candidate_evaluated

Набор11/20 оценён: searchMAP@12 1.614076%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 11,
  "committed_sets": 11,
  "api_requests": 0
}
```

## 2026-10-17T12:19:15+03:00 — authored20_candidate_committed

Зафиксирован набор12/20, популяция2, родитель9. 30 новых признаков. Решение записано до получения егоMAP. Набор9 дал1.806486% против1.791295% у6 — небольшое улучшение, но по установленному правилу родитель9. Сохраняю его26признаков и дополняю плавно затухающими личными предпочтениями типа/секции/цвета и весом повторной покупки, чтобы совместить долгую коллективную историю с текущими интересами.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 12,
  "evaluated_sets": 11,
  "api_requests": 0
}
```

## 2026-10-17T12:19:42+03:00 — authored20_candidate_evaluated

Набор12/20 оценён: searchMAP@12 1.119637%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 12,
  "committed_sets": 12,
  "api_requests": 0
}
```

## 2026-10-17T12:21:24+03:00 — authored20_candidate_committed

Зафиксирован набор13/20, популяция0, родитель1. 11 новых признаков. Решение записано до получения егоMAP. Родитель1 остаётся лучшим1.526199%; добавление цен10 ухудшило до1.049624%. Теперь сокращаю общие пользовательские/длинные счётчики и акцентирую давность/частоту конкретного товара и его продуктовой семьи. Это структурное упрощение, а не смена параметровLightGBM.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 13,
  "evaluated_sets": 12,
  "api_requests": 0
}
```

## 2026-10-17T12:21:37+03:00 — authored20_candidate_evaluated

Набор13/20 оценён: searchMAP@12 1.260293%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 13,
  "committed_sets": 13,
  "api_requests": 0
}
```

## 2026-10-17T12:21:37+03:00 — authored20_candidate_committed

Зафиксирован набор14/20, популяция1, родитель8. 28 новых признаков. Решение записано до получения егоMAP. У8 search2.148015%, расширение11 до36признаков дало лишь1.614076%. Возвращаюськ8; убираю часть абсолютных счётчиков категорий, уже представленных долями и давностью, и оставляю стандартизированный ценовой разрыв вместо двух его версий. Добавляю30-дневную и затухающую долю отдела как более общий уровень интереса.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 14,
  "evaluated_sets": 13,
  "api_requests": 0
}
```

## 2026-10-17T12:21:50+03:00 — authored20_candidate_evaluated

Набор14/20 оценён: searchMAP@12 1.677489%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 14,
  "committed_sets": 14,
  "api_requests": 0
}
```

## 2026-10-17T12:21:51+03:00 — authored20_candidate_committed

Зафиксирован набор15/20, популяция2, родитель9. 24 новых признаков. Решение записано до получения егоMAP. У9 search1.806486%, добавлениезатухания12 снизило до1.119637%. Проверяю, нужны ли сами графы: удаляю только graph_t365/graph_s365 из9, сохраняя все остальные24признака. Такое сравнение поможет выбрать направление последних шагов этой популяции.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 15,
  "evaluated_sets": 14,
  "api_requests": 0
}
```

## 2026-10-17T12:22:04+03:00 — authored20_candidate_evaluated

Набор15/20 оценён: searchMAP@12 1.768663%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 15,
  "committed_sets": 15,
  "api_requests": 0
}
```

## 2026-10-17T12:23:16+03:00 — authored20_candidate_committed

Зафиксирован набор16/20, популяция0, родитель1. 18 новых признаков. Решение записано до получения егоMAP. После четырёхнеудачных расширений лучшимвветкеостаётся1(1.526199%); упрощение13 дало1.260293%. Сохраняю12признаков1 и проверяю новый для этой ветки сигнал: прямые личные счётчики и давность секции, продуктовой семьи и цвета, вместо дополнительных глобальных трендов/цен.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 16,
  "evaluated_sets": 15,
  "api_requests": 0
}
```

## 2026-10-17T12:23:29+03:00 — authored20_candidate_evaluated

Набор16/20 оценён: searchMAP@12 1.441310%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 16,
  "committed_sets": 16,
  "api_requests": 0
}
```

## 2026-10-17T12:23:29+03:00 — authored20_candidate_committed

Зафиксирован набор17/20, популяция1, родитель8. 30 новых признаков. Решение записано до получения егоMAP. Родитель8 остаётся лучшим2.148015%; добавление11 и многокомпонентное сокращение14 хуже(1.614076%,1.677489%). Теперь меняю ровноодинпризнак: убираю абсолютныйprice_gap, оставляя масштабированныйprice_z. Проверяю более контролируемое сокращение коррелирующей информации.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 17,
  "evaluated_sets": 16,
  "api_requests": 0
}
```

## 2026-10-17T12:23:42+03:00 — authored20_candidate_evaluated

Набор17/20 оценён: searchMAP@12 1.181176%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 17,
  "committed_sets": 17,
  "api_requests": 0
}
```

## 2026-10-17T12:23:42+03:00 — authored20_candidate_committed

Зафиксирован набор18/20, популяция2, родитель9. 28 новых признаков. Решение записано до получения егоMAP. Удалениеграфов15 дало1.768663% против1.806486% у9 — небольшой спад, потому сохраняю9какродителя. Последний шаг этой популяции расширяет365-дневный коллективный сигнал двумя уровнями:цветом и группой одежды. Не возвращаю затухание, которое в12 ухудшило результат.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 18,
  "evaluated_sets": 17,
  "api_requests": 0
}
```

## 2026-10-17T12:24:19+03:00 — authored20_candidate_evaluated

Набор18/20 оценён: searchMAP@12 1.203215%, популяция2. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 18,
  "committed_sets": 18,
  "api_requests": 0
}
```

## 2026-10-17T12:26:14+03:00 — authored20_candidate_committed

Зафиксирован набор19/20, популяция0, родитель1. 16 новых признаков. Решение записано до получения егоMAP. Лучший0по-прежнему1(1.526199%); личные категории16 дали1.441310%, а предыдущие временные/ценовые варианты не улучшили1. Последний шаг ветки проверяет отдельный источник информации: возраст исторических покупателей товара/типа и его отклонение от возраста пользователя. Добавляю четыре признака к неизменённому1.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 19,
  "evaluated_sets": 18,
  "api_requests": 0
}
```

## 2026-10-17T12:26:26+03:00 — authored20_candidate_evaluated

Набор19/20 оценён: searchMAP@12 1.005704%, популяция0. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 19,
  "committed_sets": 19,
  "api_requests": 0
}
```

## 2026-10-17T12:26:26+03:00 — authored20_candidate_committed

Зафиксирован набор20/20, популяция1, родитель8. 35 новых признаков. Решение записано до получения егоMAP. Родитель8 остаётся2.148015%; удаление толькоprice_gap в17 снизило до1.181176%, поэтому сохраняю все31признак8. В последнем разрешённом наборе добавляю явные счётчики типа за7дней, секции/цвета за30дней и покупок пользователя за7дней. Часть информации связана с долями, но такие координаты могут быть удобнее деревьям. Это ровно20-й набор, дальше поиск не продолжается.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "committed_sets": 20,
  "evaluated_sets": 19,
  "api_requests": 0
}
```

## 2026-10-17T12:26:40+03:00 — authored20_candidate_evaluated

Набор20/20 оценён: searchMAP@12 1.205808%, популяция1. Матрица численно отличается от предыдущих; код и адаптивное решение сохранены.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "searching",
  "evaluated_sets": 20,
  "committed_sets": 20,
  "api_requests": 0
}
```

## 2026-10-17T13:13:37+03:00 — fresh_chat_prompt_prepared

Сохранён самостоятельный промпт без прежних решений: три популяции, 20 адаптивных наборов, только сгенерированные признаки в LightGBM. Созданы search_results.md/csv для 20 уже оценённых наборов H007; поиск H007 не является слепым, confirmation/test ещё не выполнены. Новый промпт не означает запуска API generated-only.

## 2026-10-17T13:17:12+03:00 — authored20_search_plots

Построены search_dashboard и 6 графиков PNG/SVG для 20 наборов H007: ход поиска, лидеры популяций, оценки наборов, гистограмма MAP, гистограмма AP пользователей и train loss. Средние сохранённых AP всех 20 наборов сверены с search MAP. Новых обучений/API нет; confirmation/test не выполнялись. Артефакты: reports/authored20_v1/plots.

## 2026-10-17T13:20:02+03:00 — authored20_selection_frozen

Все20 наборов оценены. Победитель выбран поconfirmation88 до итоговой оценкиval/test.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "evaluating",
  "selected_call": 9,
  "authored_sets": 20,
  "api_requests": 0
}
```

## 2026-10-17T13:22:17+03:00 — authored20_scoring_complete

All 20 sets retained; confirmation selected set 9. Final scores and six frozen replays completed. Legacy API-efficiency report failed on a missing non-API config key; verified output-only recovery, frozen sources/config unchanged. Independent audit next.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "completed_pending_audit",
  "authored_sets": 20,
  "api_requests": 0,
  "artifacts": "reports/authored20_v1"
}
```

## 2026-10-17T13:25:18+03:00 — authored20_comparison_delivered

Аудит H007 пройден:20 различных наборов, цепочка решений и независимые replay проверены. Выбран9: validation1.260603%,test2.231032%. Создан общий график reports/authored20_v1/comparison_all_methods.png. Исправлена ошибка в промпте нового чата: SHA256 байтов train_pairs.parquet=b30309d657a3d5aa7772a9affe81fb558c8a5289a8c9d39992ca12735821e719; a583938... — логический отпечаток записей, не хеш файла.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "complete"
}
```

## 2026-10-17T13:29:27+03:00 — authored20_verified_metrics_registered

H007 complete: 20 adaptive sets, 3 populations; confirmation selected set 9. Validation MAP@12 1.260603%, test 2.231032%. Audit passed. Generated features plus raw15; prior experiment history known, not a blind search.

Запуск: `hm_small_codex_authored20_adaptive_seed42_v1_cbebf62371c9`.

```json
{
  "status": "complete",
  "selected_call": 9,
  "authored_sets": 20,
  "api_requests": 0,
  "audit_status": "passed",
  "prior_experiment_history_known": true,
  "automatic_raw_features": 15,
  "artifacts": "reports/authored20_v1",
  "search_metrics": {
    "map": 0.018064856150793653
  },
  "confirm_metrics": {
    "map": 0.010532475731339369
  },
  "heldout_val_metrics": {
    "map": 0.006739472648563558
  },
  "val_metrics": {
    "map": 0.012606029752411332
  },
  "test_metrics": {
    "map": 0.02231031746031746
  }
}
```

## 2026-10-17T13:39:25+03:00 — provider_generated_only_prepared

H008: new GPT-6.1 Sol API stream, only generated f_* features enter LightGBM. Same data/LightGBM/seed/best-only memory as H006; constant-only control,20 valid programs/300 POST/3 repairs/3 islands.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "prepared",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde"
}
```

## 2026-10-17T13:40:37+03:00 — provider_generated_only_started

Validator verified; starting constant control and fresh API search.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde"
}
```

## 2026-10-17T13:41:46+03:00 — provider_generated_only_progress

H008: 1/20 programs evaluated; 1 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1,
  "api_requests": 1
}
```

## 2026-10-17T13:42:28+03:00 — provider_generated_only_progress

H008: 2/20 programs evaluated; 2 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2,
  "api_requests": 2
}
```

## 2026-10-17T13:42:55+03:00 — experiment_completed

Independent H&M adaptive feature search completed in .venv-wsl: 20 numerically distinct sets, populations 7/7/6. Winner s17 selected by confirm; final test MAP@12=0.024371224146224148. Original train_pairs checksum differed; user explicitly authorized actual file in a new protocol. Old solutions/history were not read.

Запуск: `isolated_hm_20261017_venvwsl_v1`.

```json
{
  "status": "completed",
  "winner": "s17",
  "metrics": {
    "s17": {
      "heldout_val": {
        "split": "heldout_val",
        "n_users": 88,
        "map12": 0.030298520923520922,
        "max_feature_batch_seconds": 0.22584884500065527,
        "full_catalog_size": 5000,
        "batch_users": 16
      },
      "validation": {
        "split": "validation",
        "n_users": 304,
        "map12": 0.02280822400065821,
        "max_feature_batch_seconds": 0.20266831800108775,
        "full_catalog_size": 5000,
        "batch_users": 16
      },
      "test": {
        "split": "test",
        "n_users": 250,
        "map12": 0.024371224146224148,
        "max_feature_batch_seconds": 0.34216597600061505,
        "full_catalog_size": 5000,
        "batch_users": 16
      }
    },
    "control": {
      "heldout_val": {
        "split": "heldout_val",
        "n_users": 88,
        "map12": 0.0009469696969696969,
        "max_feature_batch_seconds": 0.007121442000425304,
        "full_catalog_size": 5000,
        "batch_users": 16
      },
      "validation": {
        "split": "validation",
        "n_users": 304,
        "map12": 0.00027412280701754384,
        "max_feature_batch_seconds": 0.00837782700000389,
        "full_catalog_size": 5000,
        "batch_users": 16
      },
      "test": {
        "split": "test",
        "n_users": 250,
        "map12": 0.0016666666666666666,
        "max_feature_batch_seconds": 0.008947611000621691,
        "full_catalog_size": 5000,
        "batch_users": 16
      }
    }
  },
  "counts": {
    "successful_feature_sets": 20,
    "population_sizes": [
      7,
      7,
      6
    ],
    "substantive_proposal_versions": 20,
    "control_proposals": 1,
    "total_submitted_versions_including_control": 21,
    "repairs": 0,
    "rejections": 0,
    "numerical_duplicates": 0,
    "trainings_current_run": 21,
    "superseded_control_trainings": 1,
    "trainings_total_chat": 22,
    "post_selection_trainings": 0
  },
  "report": "/mnt/c/Users/Мишаня/ml/projs/tbank/Features/isolated_hm_20261017_venvwsl_v1/REPORT.md",
  "history_read": false,
  "train_pairs_sha256": "b30309d657a3d5aa7772a9affe81fb558c8a5289a8c9d39992ca12735821e719"
}
```

## 2026-10-17T13:43:11+03:00 — provider_generated_only_progress

H008: 3/20 programs evaluated; 3 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3,
  "api_requests": 3
}
```

## 2026-10-17T13:43:59+03:00 — provider_generated_only_progress

H008: 4/20 programs evaluated; 4 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4,
  "api_requests": 4
}
```

## 2026-10-17T13:44:46+03:00 — provider_generated_only_progress

H008: 4/20 programs evaluated; 5 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 5,
  "api_requests": 5
}
```

## 2026-10-17T13:45:12+03:00 — provider_generated_only_progress

H008: 5/20 programs evaluated; 6 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 6,
  "api_requests": 6
}
```

## 2026-10-17T13:46:03+03:00 — provider_generated_only_progress

H008: 6/20 programs evaluated; 7 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 7,
  "api_requests": 7
}
```

## 2026-10-17T13:46:28+03:00 — provider_generated_only_progress

H008: 7/20 programs evaluated; 8 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 8,
  "api_requests": 8
}
```

## 2026-10-17T13:46:55+03:00 — provider_generated_only_progress

H008: 8/20 programs evaluated; 9 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 9,
  "api_requests": 9
}
```

## 2026-10-17T13:47:23+03:00 — provider_generated_only_progress

H008: 9/20 programs evaluated; 10 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 10,
  "api_requests": 10
}
```

## 2026-10-17T13:47:51+03:00 — provider_generated_only_progress

H008: 10/20 programs evaluated; 11 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 11,
  "api_requests": 11
}
```

## 2026-10-17T13:48:18+03:00 — provider_generated_only_progress

H008: 11/20 programs evaluated; 12 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 12,
  "api_requests": 12
}
```

## 2026-10-17T13:48:41+03:00 — provider_generated_only_progress

H008: 12/20 programs evaluated; 13 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 13,
  "api_requests": 13
}
```

## 2026-10-17T13:48:57+03:00 — provider_generated_only_progress

H008: 12/20 programs evaluated; 14 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 14,
  "api_requests": 14
}
```

## 2026-10-17T13:49:25+03:00 — provider_generated_only_progress

H008: 13/20 programs evaluated; 15 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 15,
  "api_requests": 15
}
```

## 2026-10-17T13:49:53+03:00 — provider_generated_only_progress

H008: 14/20 programs evaluated; 16 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 16,
  "api_requests": 16
}
```

## 2026-10-17T13:50:15+03:00 — provider_generated_only_progress

H008: 15/20 programs evaluated; 17 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 17,
  "api_requests": 17
}
```

## 2026-10-17T13:50:42+03:00 — provider_generated_only_progress

H008: 16/20 programs evaluated; 18 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 18,
  "api_requests": 18
}
```

## 2026-10-17T13:51:14+03:00 — provider_generated_only_progress

H008: 17/20 programs evaluated; 19 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 19,
  "api_requests": 19
}
```

## 2026-10-17T13:51:38+03:00 — provider_generated_only_progress

H008: 18/20 programs evaluated; 20 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 20,
  "api_requests": 20
}
```

## 2026-10-17T13:51:56+03:00 — provider_generated_only_progress

H008: 18/20 programs evaluated; 21 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 21,
  "api_requests": 21
}
```

## 2026-10-17T13:52:26+03:00 — provider_generated_only_progress

H008: 19/20 programs evaluated; 22 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 22,
  "api_requests": 22
}
```

## 2026-10-17T13:52:59+03:00 — provider_generated_only_progress

H008: 20/20 programs evaluated; 23 responses processed.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 23,
  "api_requests": 23
}
```

## 2026-10-17T13:53:31+03:00 — provider_generated_only_selection_frozen

Selection frozen on confirmation before final evaluation.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "evaluating",
  "selected_call": 12,
  "measured": 20
}
```

## 2026-10-17T13:55:12+03:00 — provider_generated_only_finished

Search and final evaluation completed; independent audit required.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "completed_pending_audit",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde"
}
```

## 2026-10-17T13:56:09+03:00 — provider_generated_only_audited

H008 complete: generated-only inputs verified; final metrics and plots audited.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "complete",
  "automatic_raw_features": 0,
  "audit_status": "passed",
  "api_requests": 23,
  "measured": 20,
  "numeric_distinct_sets": 19,
  "selected_call": 12,
  "val_metrics": {
    "map": 0.014785629108545773
  },
  "test_metrics": {
    "map": 0.014267604617604618
  },
  "artifacts": "reports/provider_generated_only_v1"
}
```

## 2026-10-17T13:57:19+03:00 — provider_generated_only_summary

H008 verified:23 API POST,20 valid programs,3 genuine preflight rejections,0 HTTP failures;19 unordered numeric feature sets (calls9/16 coincide by values but differ in column order). Selected12:25 explicitly returned inputs including7 static copies, automatic raw15=0. Validation1.478563%,test1.426760%; prior H006test1.357362%, difference+0.069399pp, paired-user95%CI[-1.034078,1.273127] includes0. Report/plots/archive delivered in reports/provider_generated_only_v1 and the unique run folder.

Запуск: `hm_small_gpt61sol_generated_only_seed42_v1_1257cedd9dde`.

```json
{
  "status": "complete"
}
```

## 2026-10-17T14:02:29+03:00 — provider_history_prepared

H009: fresh GPT API stream, full separate history of each island, including failures and search feedback. Same generated-only features/data/downstream/20 valid/300POST/3repairs as H008. No history truncation; input-token budget differs.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "prepared",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0"
}
```

## 2026-10-17T14:03:56+03:00 — provider_history_progress

H009: 1/20 valid; 1 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1,
  "api_requests": 1
}
```

## 2026-10-17T14:04:44+03:00 — provider_history_progress

H009: 2/20 valid; 2 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2,
  "api_requests": 2
}
```

## 2026-10-17T14:05:35+03:00 — provider_history_progress

H009: 3/20 valid; 3 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3,
  "api_requests": 3
}
```

## 2026-10-17T14:06:15+03:00 — provider_history_progress

H009: 4/20 valid; 4 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4,
  "api_requests": 4
}
```

## 2026-10-17T14:06:54+03:00 — provider_history_progress

H009: 5/20 valid; 5 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5,
  "api_requests": 5
}
```

## 2026-10-17T14:07:43+03:00 — provider_history_progress

H009: 6/20 valid; 6 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6,
  "api_requests": 6
}
```

## 2026-10-17T14:08:27+03:00 — provider_history_progress

H009: 7/20 valid; 7 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7,
  "api_requests": 7
}
```

## 2026-10-17T14:09:03+03:00 — provider_history_progress

H009: 8/20 valid; 8 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8,
  "api_requests": 8
}
```

## 2026-10-17T14:09:33+03:00 — provider_history_progress

H009: 9/20 valid; 9 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9,
  "api_requests": 9
}
```

## 2026-10-17T14:09:58+03:00 — provider_history_progress

H009: 10/20 valid; 10 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10,
  "api_requests": 10
}
```

## 2026-10-17T14:10:28+03:00 — provider_history_progress

H009: 10/20 valid; 11 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 11,
  "api_requests": 11
}
```

## 2026-10-17T14:11:02+03:00 — provider_history_progress

H009: 11/20 valid; 12 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 12,
  "api_requests": 12
}
```

## 2026-10-17T14:11:32+03:00 — provider_history_progress

H009: 12/20 valid; 13 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 13,
  "api_requests": 13
}
```

## 2026-10-17T14:11:56+03:00 — provider_history_progress

H009: 12/20 valid; 14 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 14,
  "api_requests": 14
}
```

## 2026-10-17T14:12:21+03:00 — provider_history_progress

H009: 12/20 valid; 15 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 15,
  "api_requests": 15
}
```

## 2026-10-17T14:12:52+03:00 — provider_history_progress

H009: 13/20 valid; 16 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 16,
  "api_requests": 16
}
```

## 2026-10-17T14:13:19+03:00 — provider_history_progress

H009: 13/20 valid; 17 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 17,
  "api_requests": 17
}
```

## 2026-10-17T14:13:54+03:00 — provider_history_progress

H009: 14/20 valid; 18 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 18,
  "api_requests": 18
}
```

## 2026-10-17T14:14:41+03:00 — provider_history_progress

H009: 15/20 valid; 19 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 19,
  "api_requests": 19
}
```

## 2026-10-17T14:15:23+03:00 — provider_history_progress

H009: 16/20 valid; 20 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 20,
  "api_requests": 20
}
```

## 2026-10-17T14:15:51+03:00 — provider_history_progress

H009: 17/20 valid; 21 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 21,
  "api_requests": 21
}
```

## 2026-10-17T14:16:08+03:00 — provider_history_host_limit

H009: call15 rejected because restricted host omits hasattr, not because ordinary Python is invalid. Separate diagnostic allowing only hasattr preserves AST/I/O restrictions, passes preflight and exactly matches accepted call16 on all72813 train pairs. Live sources/config unchanged;0 extra fits/0 API. This limitation must be disclosed and fixed or documented before a future protocol.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

## 2026-10-17T14:16:37+03:00 — provider_history_progress

H009: 18/20 valid; 22 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 22,
  "api_requests": 22
}
```

## 2026-10-17T14:17:25+03:00 — provider_history_progress

H009: 19/20 valid; 23 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 23,
  "api_requests": 23
}
```

## 2026-10-17T14:17:53+03:00 — provider_history_progress

H009: 20/20 valid; 24 responses.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 24,
  "api_requests": 24
}
```

## 2026-10-17T14:18:32+03:00 — provider_history_selection_frozen

Full-history selection frozen before final targets.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "evaluating",
  "selected_call": 6
}
```

## 2026-10-17T14:20:25+03:00 — provider_history_finished

H009 final scoring completed; independent audit next.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "completed_pending_audit",
  "artifacts": "LLMFeatures/results/hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0"
}
```

## 2026-10-17T14:22:46+03:00 — provider_history_audited

H009 complete: full own-island message histories verified; final metrics and plots audited.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "complete",
  "automatic_raw_features": 0,
  "audit_status": "passed",
  "api_requests": 24,
  "measured": 20,
  "numeric_distinct_sets": 18,
  "selected_call": 6,
  "val_metrics": {
    "map": 0.022869891743247005
  },
  "test_metrics": {
    "map": 0.007215958284140102
  },
  "artifacts": "reports/provider_history_v1"
}
```

## 2026-10-17T14:24:27+03:00 — provider_history_verified_summary

H009 complete:24 API POST,20 accepted programs,18 unordered numeric sets. Selected6:validation2.286989%,test0.721596% versus best-only H008test1.426760%. All own-island histories/search feedback verified, max18 messages/38143 input tokens, 385823 total input tokens versus55261. Four rejections include one HOST hasattr limitation; diagnostic proves rejected15 equals accepted16 when only hasattr is enabled. Live runtime unchanged. One run does not establish a universal memory effect.

Запуск: `hm_small_gpt61sol_full_history_seed42_v1_93021ef262b0`.

```json
{
  "status": "complete",
  "audit_status": "passed",
  "api_requests": 24,
  "measured": 20,
  "numeric_distinct_sets": 18,
  "selected_call": 6,
  "full_own_island_history_verified": true,
  "input_tokens": 385823,
  "max_input_tokens_observed": 38143,
  "automatic_raw_features": 0,
  "host_builtin_limitations": 1,
  "artifacts": "reports/provider_history_v1",
  "search_metrics": {
    "map": 0.029162016369047625
  },
  "confirm_metrics": {
    "map": 0.016740319865319864
  },
  "heldout_val_metrics": {
    "map": 0.019847282347282346
  },
  "val_metrics": {
    "map": 0.022869891743247005
  },
  "test_metrics": {
    "map": 0.007215958284140102
  }
}
```

## 2026-10-17T17:38:54+03:00 — gitignore_cleanup

Updated ignore rules for raw GPT/authored runs, smoke/replay outputs, provider probes, local pointers and editor settings. Preserved configs/manifests, source, notebooks, summary reports and plots. Exported six selected feature programs with SHA256 manifests to report folders. Untracked files reduced from2453 to339. Files and Git index were not deleted or modified; .gitignore self-ignore preserved.

## 2026-10-17T17:52:26+03:00 — medium_cv_prepare

Preparing larger fixed past-only cohort and temporal CV; no model fitting yet.

Запуск: `hm_medium_temporal_cv_v1`.

```json
{
  "status": "preparing",
  "artifacts": "CVBenchmark/PROTOCOL.md"
}
```

## 2026-10-17T17:52:34+03:00 — medium_cv_dataset_ready

Larger fixed cohort and three temporal folds saved; originals unchanged.

Запуск: `hm_medium_temporal_cv_v1`.

```json
{
  "status": "data_ready",
  "users": 20000,
  "items": 10000,
  "fold_rows": [
    {
      "train": 10923,
      "val": 1410,
      "test": 1276
    },
    {
      "train": 9583,
      "val": 1301,
      "test": 1191
    },
    {
      "train": 8548,
      "val": 1069,
      "test": 873
    }
  ],
  "artifacts": "reports/medium_cv_v1"
}
```

## 2026-10-17T17:55:05+03:00 — medium_cv_deferred

User deferred work until later. Dataset prepared:20000 users,10000 items,3 temporal folds,3340 outer-test user-times. No model training or API searches started. Draft protocol and preparation source retained. Before fitting review low fixed-catalog future-positive coverage46.47/35.16/28.52 percent and dropped empty-target rows. Neural native environment must avoid NumPy2 audit overlay.

Запуск: `hm_medium_temporal_cv_v1`.

```json
{
  "status": "deferred_by_user"
}
```

## 2026-10-17T20:26:23+03:00 — medium_cv_v2_data

Retained all outer users and all original positive labels in metric denominators; no future targets used for catalog selection.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "data_ready",
  "test_user_times": [
    1839,
    1982,
    1698
  ],
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T20:35:10+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T20:37:10+03:00 — medium_cv_resumed

Starting nine-method temporal CV; three reset folds; no Qwen/Llama. Outer scoring gated until all selections frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T20:38:24+03:00 — medium_cv_metadata_fix

Before any API config/request or fitting: corrected inherited API version metadata to capture actual native dependency versions; source manifest updated, previous manifest retained. Experimental parameters/validator/runtime unchanged.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying"
}
```

## 2026-10-17T20:38:24+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T20:38:47+03:00 — small_context_error

Ошибка малого ContextGNN эксперимента

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "failed",
  "error": "<StatType.MEAN: 'MEAN'>"
}
```

## 2026-10-17T20:38:50+03:00 — medium_cv_error

gpu_gnn_smoke failed; inspect /mnt/c/Users/Мишаня/ml/projs/tbank/Features/reports/medium_cv_v2/stages/gpu_gnn_smoke.log

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "interrupted",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T20:40:04+03:00 — medium_cv_preflight_cache_fix

Repeated GPU smoke found unseeded get_stype_proposal random sampling mismatching cached column statistics (missing MEAN). No model fitting/API requests yet. Fixed seed42 before schema inference; infer schema from first-train-cutoff history; separate new cache path. Failed preflight/old manifests retained. Rechecking fresh and cached paths before training.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying"
}
```

## 2026-10-17T20:40:16+03:00 — medium_cv_resumed

Starting nine-method temporal CV; three reset folds; no Qwen/Llama. Outer scoring gated until all selections frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T20:40:45+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T20:43:15+03:00 — medium_cv_running

Validator and GPU smoke checks passed. CPU/API and GPU lanes begin; no outer-test scores available.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T20:43:32+03:00 — medium_cv_tree_trained

Fold0 manual: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold0_manual`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T20:43:43+03:00 — medium_cv_tree_trained

Fold0 raw15: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold0_raw15`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T20:43:56+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T20:44:35+03:00 — medium_cv_api_progress

Fold0 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T20:44:36+03:00 — small_epoch

Малый idgnn: эпоха 1/10, validation MAP=0.0760%

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.0749088759469085,
  "val_metrics": {
    "map": 0.000759548611111111
  },
  "train_seconds": 15.409163905000241,
  "val_seconds": 0.02872178200050257,
  "steps": 86
}
```

## 2026-10-17T20:44:39+03:00 — small_epoch

Малый idgnn: эпоха 2/10, validation MAP=0.0760%

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.05502872788455597,
  "val_metrics": {
    "map": 0.000759548611111111
  },
  "train_seconds": 2.5743877759996394,
  "val_seconds": 0.0397834489995148,
  "steps": 86
}
```

## 2026-10-17T20:44:43+03:00 — small_epoch

Малый idgnn: эпоха 3/10, validation MAP=0.0760%

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.05061912833344798,
  "val_metrics": {
    "map": 0.000759548611111111
  },
  "train_seconds": 2.7154976130004798,
  "val_seconds": 0.0366887800009863,
  "steps": 86
}
```

## 2026-10-17T20:44:46+03:00 — small_epoch

Малый idgnn: эпоха 4/10, validation MAP=0.0760%

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.04963441821205061,
  "val_metrics": {
    "map": 0.000759548611111111
  },
  "train_seconds": 2.9595213520005927,
  "val_seconds": 0.02704861599886499,
  "steps": 86
}
```

## 2026-10-17T20:44:54+03:00 — small_epoch

Малый contextgnn: эпоха 1/10, validation MAP=0.0195%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 36.504595046819645,
  "val_metrics": {
    "map": 0.0001953125
  },
  "train_seconds": 6.623367558000609,
  "val_seconds": 0.19015237299936416,
  "steps": 86
}
```

## 2026-10-17T20:45:02+03:00 — small_epoch

Малый contextgnn: эпоха 2/10, validation MAP=0.0309%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 24.17852415040482,
  "val_metrics": {
    "map": 0.00030924479166666665
  },
  "train_seconds": 7.054201892999117,
  "val_seconds": 0.21287294500143616,
  "steps": 86
}
```

## 2026-10-17T20:45:08+03:00 — medium_cv_api_progress

Fold0 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T20:45:10+03:00 — small_epoch

Малый contextgnn: эпоха 3/10, validation MAP=0.1726%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 23.79494265622871,
  "val_metrics": {
    "map": 0.0017257771164021162
  },
  "train_seconds": 7.184341095000491,
  "val_seconds": 0.21720174999973096,
  "steps": 86
}
```

## 2026-10-17T20:45:18+03:00 — small_epoch

Малый contextgnn: эпоха 4/10, validation MAP=0.0093%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 25.956638269646223,
  "val_metrics": {
    "map": 9.300595238095238e-05
  },
  "train_seconds": 6.572204275000331,
  "val_seconds": 0.18949482700008957,
  "steps": 86
}
```

## 2026-10-17T20:45:25+03:00 — small_epoch

Малый contextgnn: эпоха 5/10, validation MAP=0.2958%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 23.436248003050338,
  "val_metrics": {
    "map": 0.0029578711219336216
  },
  "train_seconds": 6.1761105740006315,
  "val_seconds": 0.19726678600090963,
  "steps": 86
}
```

## 2026-10-17T20:45:32+03:00 — small_epoch

Малый contextgnn: эпоха 6/10, validation MAP=0.2803%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 22.92789417089418,
  "val_metrics": {
    "map": 0.002802861201298701
  },
  "train_seconds": 6.03576233000058,
  "val_seconds": 0.1833257500002219,
  "steps": 86
}
```

## 2026-10-17T20:45:39+03:00 — small_epoch

Малый contextgnn: эпоха 7/10, validation MAP=0.2580%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 22.743253109066984,
  "val_metrics": {
    "map": 0.0025796469155844153
  },
  "train_seconds": 6.178061848999278,
  "val_seconds": 0.1961526060003962,
  "steps": 86
}
```

## 2026-10-17T20:45:46+03:00 — small_epoch

Малый contextgnn: эпоха 8/10, validation MAP=0.2463%

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "training",
  "epoch": 8,
  "train_loss": 22.579382852066395,
  "val_metrics": {
    "map": 0.002463107638888889
  },
  "train_seconds": 6.384648379000282,
  "val_seconds": 0.19306771099945763,
  "steps": 86
}
```

## 2026-10-17T20:46:14+03:00 — medium_cv_api_progress

Fold0 h008: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T20:46:25+03:00 — medium_cv_initial_training

All3 fold validator suites passed47 checks each. Seeded past-only GNN schema passed fresh smoke and subsequent cached full fit; Recformer GPU smoke passed. Fold0 manual/raw15 and IDGNN/ContextGNN trained; fixed TDM started. H008 first2 API programs accepted, third preflight passed. These are search results only; outer targets not scored.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T20:46:25+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 1800,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "fixed",
    "run_id": "hm_medium_cv_v2_fold0_tdm_fixed",
    "subset_sha256": "79901c7e20e26891a7bbfe4ab1870414eb2959045746b06129ae6d20e8f70014",
    "data_hashes": {
      "article_id_map.csv": "1bd670ffb49641faf3381c3de3af962e652c167366dcab36b7271474c629d5a1",
      "customer_id_map.csv": "1d64bdeafa0c5ab8c0d6187943b5d1d5edbfb35d7bb3f87816f076811f24d1c9",
      "db/article.parquet": "d30e5b0075f792d6d3b52d315ae8c2f23fe787fc01d87aa5e533ca80e9e19cb5",
      "db/customer.parquet": "9e5b831bbd8e49e8ac910d0da6c5d14bd17bcf4674288b42a6234fadb9042489",
      "db/transactions.parquet": "6a88fb46636e38d4c76a26998b0038e92ddc7099f27fe9dffeaf9fd1bb9e716c",
      "manifest.yaml": "1ebe1d73bdc70e55fa156137a6cb45cb59b0bdbdd4adf543af45df876c7a902d",
      "selection.json": "19bd7c1e178c1214c69d0920d569954f7c7c29a398289f3354751f9018a0b053",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "5e569b098d3971a731646ea722ea5b8876ab9afb6000f511924cebbe04f5be2c",
      "tasks/user-item-purchase/test_full.parquet": "5e569b098d3971a731646ea722ea5b8876ab9afb6000f511924cebbe04f5be2c",
      "tasks/user-item-purchase/train.parquet": "fa42d70ae5e3bbea59f5fa3a91be16b1eb961602b2955a754035237d92c46a04",
      "tasks/user-item-purchase/val.parquet": "42377204d02afd9e0ce03d18b764d6f7b021d441e800f6bc20807c09234c7588",
      "tasks/user-item-purchase/val_full.parquet": "76dadcd9076d37f9546e7002ebf382ba600008fd44ce6670b6cbceb2b73a7880"
    },
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379",
    "prerequisite": {
      "tree": "fixed categories; no clustering"
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 833295
  }
}
```

## 2026-10-17T20:46:46+03:00 — medium_cv_api_progress

Fold0 h008: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T20:47:35+03:00 — medium_cv_api_progress

Fold0 h008: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T20:48:05+03:00 — medium_cv_gpu_recovery

Recovering GPU lane with required TDM CuBLAS deterministic setting; existing API lane kept running.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T20:48:19+03:00 — medium_cv_api_progress

Fold0 h008: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T20:48:34+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 1800,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "fixed",
    "run_id": "hm_medium_cv_v2_fold0_tdm_fixed",
    "subset_sha256": "79901c7e20e26891a7bbfe4ab1870414eb2959045746b06129ae6d20e8f70014",
    "data_hashes": {
      "article_id_map.csv": "1bd670ffb49641faf3381c3de3af962e652c167366dcab36b7271474c629d5a1",
      "customer_id_map.csv": "1d64bdeafa0c5ab8c0d6187943b5d1d5edbfb35d7bb3f87816f076811f24d1c9",
      "db/article.parquet": "d30e5b0075f792d6d3b52d315ae8c2f23fe787fc01d87aa5e533ca80e9e19cb5",
      "db/customer.parquet": "9e5b831bbd8e49e8ac910d0da6c5d14bd17bcf4674288b42a6234fadb9042489",
      "db/transactions.parquet": "6a88fb46636e38d4c76a26998b0038e92ddc7099f27fe9dffeaf9fd1bb9e716c",
      "manifest.yaml": "1ebe1d73bdc70e55fa156137a6cb45cb59b0bdbdd4adf543af45df876c7a902d",
      "selection.json": "19bd7c1e178c1214c69d0920d569954f7c7c29a398289f3354751f9018a0b053",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "5e569b098d3971a731646ea722ea5b8876ab9afb6000f511924cebbe04f5be2c",
      "tasks/user-item-purchase/test_full.parquet": "5e569b098d3971a731646ea722ea5b8876ab9afb6000f511924cebbe04f5be2c",
      "tasks/user-item-purchase/train.parquet": "fa42d70ae5e3bbea59f5fa3a91be16b1eb961602b2955a754035237d92c46a04",
      "tasks/user-item-purchase/val.parquet": "42377204d02afd9e0ce03d18b764d6f7b021d441e800f6bc20807c09234c7588",
      "tasks/user-item-purchase/val_full.parquet": "76dadcd9076d37f9546e7002ebf382ba600008fd44ce6670b6cbceb2b73a7880"
    },
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379",
    "prerequisite": {
      "tree": "fixed categories; no clustering"
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 833295
  }
}
```

## 2026-10-17T20:48:51+03:00 — medium_cv_api_progress

Fold0 h008: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T20:48:52+03:00 — medium_cv_tdm_environment_fix

TDM failed before its first successful forward/optimizer update because CUBLAS_WORKSPACE_CONFIG was absent under deterministic CUDA. Preserved failed config/tree in fixed_failed_before_first_forward_cublas. Set :4096:8 in TDM entry point before torch import; launched separate GPU recovery while original API lane continues without duplicate calls. Recovery waits for original controller and resumes completed stages.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T20:49:17+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 1,
  "val_metrics": {
    "map": 0.003175619798108637
  },
  "best_epoch": 1,
  "train_loss": 0.6644495908949556
}
```

## 2026-10-17T20:49:31+03:00 — medium_cv_api_progress

Fold0 h008: 8/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8
}
```

## 2026-10-17T20:49:58+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 2,
  "val_metrics": {
    "map": 0.003175619798108637
  },
  "best_epoch": 1,
  "train_loss": 0.6401328610537339
}
```

## 2026-10-17T20:50:01+03:00 — medium_cv_api_progress

Fold0 h008: 9/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9
}
```

## 2026-10-17T20:50:33+03:00 — medium_cv_api_progress

Fold0 h008: 10/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10
}
```

## 2026-10-17T20:50:38+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 3,
  "val_metrics": {
    "map": 0.003175619798108637
  },
  "best_epoch": 1,
  "train_loss": 0.5997709191936236
}
```

## 2026-10-17T20:51:15+03:00 — medium_cv_api_progress

Fold0 h008: 11/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 11
}
```

## 2026-10-17T20:51:20+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 4,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "best_epoch": 4,
  "train_loss": 0.5226433347913371
}
```

## 2026-10-17T20:51:44+03:00 — medium_cv_api_progress

Fold0 h008: 12/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 12
}
```

## 2026-10-17T20:52:00+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 5,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "best_epoch": 4,
  "train_loss": 0.45439365960894285
}
```

## 2026-10-17T20:52:19+03:00 — medium_cv_api_progress

Fold0 h008: 13/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 13
}
```

## 2026-10-17T20:52:40+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 6,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "best_epoch": 4,
  "train_loss": 0.40674531080816423
}
```

## 2026-10-17T20:53:08+03:00 — medium_cv_api_progress

Fold0 h008: 14/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 14
}
```

## 2026-10-17T20:53:20+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 7,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "best_epoch": 4,
  "train_loss": 0.37479444979322746
}
```

## 2026-10-17T20:53:47+03:00 — medium_cv_api_progress

Fold0 h008: 15/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 15
}
```

## 2026-10-17T20:53:59+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 8,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "best_epoch": 4,
  "train_loss": 0.34477731793948185
}
```

## 2026-10-17T20:53:59+03:00 — tdm_training_complete

TDM training complete; test not evaluated

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "trained_pending_test",
  "epoch": 8,
  "val_metrics": {
    "map": 0.006119791666666667
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/tdm/fixed",
  "summary": {
    "best_epoch": 4,
    "epochs": 8,
    "best_validation_map": 0.006119791666666667,
    "training_and_validation_seconds": 317.7619972930006,
    "peak_cuda_bytes": 108993536,
    "stop_reason": "patience4",
    "checkpoint_sha256": "5932d7ca6170c22ff2e7e6b47f20015417f3214938e98db6b5e6fccb04ba2f03",
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379"
  }
}
```

## 2026-10-17T20:54:24+03:00 — medium_cv_api_progress

Fold0 h008: 16/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 16
}
```

## 2026-10-17T20:55:04+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 1e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "low_lr_warmup",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 148110336,
      "frozen": 0
    },
    "freeze_policy": "none",
    "scheduler": "100 successful optimizer updates warmup, then linear decay over1204 updates",
    "warmup_updates": 100,
    "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog10000",
    "subset_sha256": "79901c7e20e26891a7bbfe4ab1870414eb2959045746b06129ae6d20e8f70014",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "c56a2ae95cecd0ce6ce5016c4629004ce3293158261cca41df94800b9dd14f57",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-17T20:55:36+03:00 — medium_cv_api_progress

Fold0 h008: 17/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 17
}
```

## 2026-10-17T20:56:03+03:00 — medium_cv_model_trained

Fold0 idgnn training complete; outer test not scored.

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "trained_pending_test",
  "config": {
    "best_epoch": 1,
    "epochs": 4,
    "seconds": 25.331882152999242
  }
}
```

## 2026-10-17T20:56:03+03:00 — medium_cv_model_trained

Fold0 contextgnn training complete; outer test not scored.

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "config": {
    "best_epoch": 5,
    "epochs": 8,
    "seconds": 58.78566937100004
  }
}
```

## 2026-10-17T20:56:03+03:00 — medium_cv_tdm_trained

Fold0 fixed TDM:8 epochs completed, checkpoint frozen; Recformer training started.

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "trained_pending_test",
  "summary": {
    "best_epoch": 4,
    "epochs": 8,
    "best_validation_map": 0.006119791666666667,
    "training_and_validation_seconds": 317.7619972930006,
    "peak_cuda_bytes": 108993536,
    "stop_reason": "patience4",
    "checkpoint_sha256": "5932d7ca6170c22ff2e7e6b47f20015417f3214938e98db6b5e6fccb04ba2f03",
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379"
  }
}
```

## 2026-10-17T20:56:16+03:00 — medium_cv_api_progress

Fold0 h008: 18/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 18
}
```

## 2026-10-17T20:56:53+03:00 — medium_cv_api_progress

Fold0 h008: 19/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 19
}
```

## 2026-10-17T20:57:30+03:00 — medium_cv_api_progress

Fold0 h008: 19/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 20
}
```

## 2026-10-17T20:58:44+03:00 — medium_cv_api_progress

Fold0 h008: 20/20 accepted, 21 responses.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 21
}
```

## 2026-10-17T21:03:52+03:00 — medium_cv_saved_schema_verified

H008 fold0 reached20 accepted programs in21 responses. Temporarily SIGSTOP API parent to check fresh LightGBM inference schema. Added engine.names=model.feature_name() at load boundary; fit/search implementation unchanged. Synthetic reversed-column test passed; both already-computed confirmation predictions/MAP repeated EXACTLY.47 regressions passed. Prior worker/config/manifests retained; API resumed without regeneration. GPU Recformer continued throughout.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T21:04:48+03:00 — medium_cv_api_selected

Fold0 h008:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:05:08+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 0.49598%

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 9.035711635211063,
    "val_metrics": {
      "map": 0.004959753787878787
    },
    "epoch_seconds": 527.6769564900005,
    "val_seconds": 4.353972221999356,
    "rows": 10923,
    "lr_first": 1.0000000000000001e-07,
    "lr_last": 7.796352583586628e-06,
    "optimizer_updates": 681,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:06:06+03:00 — medium_cv_api_progress

Fold0 h009: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T21:06:46+03:00 — medium_cv_api_progress

Fold0 h009: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T21:07:18+03:00 — medium_cv_fold0_h008_selected

H008 fold0 finished20 accepted programs in21 responses; confirmation selected8 (MAP0.007180277081592872), not search leader14. H009 fresh own-island-history stream started. Recformer fold0 completed first of4 epochs (10923 rows,527.7s); all outer-test metrics remain withheld. H008 elapsed includes explicit schema-validation maintenance pause; token/POST counts are the comparable API cost measures.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T21:07:31+03:00 — medium_cv_api_progress

Fold0 h009: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T21:08:25+03:00 — medium_cv_api_progress

Fold0 h009: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T21:09:03+03:00 — medium_cv_api_progress

Fold0 h009: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T21:09:47+03:00 — medium_cv_api_progress

Fold0 h009: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T21:10:48+03:00 — medium_cv_api_progress

Fold0 h009: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T21:11:32+03:00 — medium_cv_api_progress

Fold0 h009: 8/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8
}
```

## 2026-10-17T21:12:37+03:00 — medium_cv_api_progress

Fold0 h009: 9/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9
}
```

## 2026-10-17T21:13:36+03:00 — medium_cv_api_progress

Fold0 h009: 10/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10
}
```

## 2026-10-17T21:14:08+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 0.44703%

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.939029639476999,
    "val_metrics": {
      "map": 0.004470274733946609
    },
    "epoch_seconds": 521.6040198390001,
    "val_seconds": 4.123033959000168,
    "rows": 10923,
    "lr_first": 7.792553191489362e-06,
    "lr_last": 5.201367781155015e-06,
    "optimizer_updates": 1364,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:14:19+03:00 — medium_cv_api_progress

Fold0 h009: 11/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 11
}
```

## 2026-10-17T21:15:08+03:00 — medium_cv_api_progress

Fold0 h009: 12/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 12
}
```

## 2026-10-17T21:16:08+03:00 — medium_cv_api_progress

Fold0 h009: 13/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 13
}
```

## 2026-10-17T21:16:47+03:00 — medium_cv_api_progress

Fold0 h009: 14/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 14
}
```

## 2026-10-17T21:17:51+03:00 — medium_cv_api_progress

Fold0 h009: 15/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 15
}
```

## 2026-10-17T21:18:54+03:00 — medium_cv_api_progress

Fold0 h009: 16/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 16
}
```

## 2026-10-17T21:19:40+03:00 — medium_cv_api_progress

Fold0 h009: 17/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 17
}
```

## 2026-10-17T21:20:32+03:00 — medium_cv_api_progress

Fold0 h009: 18/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 18
}
```

## 2026-10-17T21:21:26+03:00 — medium_cv_api_progress

Fold0 h009: 19/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 19
}
```

## 2026-10-17T21:21:44+03:00 — medium_cv_live_audit

Existing CPU/API and GPU processes alive; all17 frozen source hashes match. Fold0 H00820 accepted, H00919 accepted and call20 in progress; Recformer stage2 epoch1. No outer-test scoring and no duplicate launches.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T21:22:09+03:00 — medium_cv_api_progress

Fold0 h009: 20/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 20
}
```

## 2026-10-17T21:23:20+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 0.42411%

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.918885554729561,
    "val_metrics": {
      "map": 0.004241071428571428
    },
    "epoch_seconds": 531.5393436739996,
    "val_seconds": 5.193239501999415,
    "rows": 10923,
    "lr_first": 5.197568389057751e-06,
    "lr_last": 2.6063829787234047e-06,
    "optimizer_updates": 2047,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:23:30+03:00 — medium_cv_protocol_explained

Documented exact training folds, shared tree pairs, neural-objective differences, original-target MAP denominators and user-cluster bootstrap in reports/medium_cv_v2/evaluation_explained_ru.md. H009fold0 reached20 accepted; confirmation pending; outer scores still unavailable. Frozen17 source hashes unchanged.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T21:24:02+03:00 — medium_cv_api_selected

Fold0 h009:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:24:19+03:00 — medium_cv_tree_trained

Fold1 manual: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold1_manual`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:24:32+03:00 — medium_cv_tree_trained

Fold1 raw15: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold1_raw15`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:25:41+03:00 — medium_cv_api_progress

Fold1 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T21:26:22+03:00 — medium_cv_api_progress

Fold1 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T21:27:06+03:00 — medium_cv_api_progress

Fold1 h008: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T21:27:50+03:00 — medium_cv_api_progress

Fold1 h008: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T21:28:31+03:00 — medium_cv_api_progress

Fold1 h008: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T21:29:18+03:00 — medium_cv_api_progress

Fold1 h008: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T21:29:55+03:00 — medium_cv_api_progress

Fold1 h008: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T21:30:14+03:00 — medium_cv_api_progress

Fold1 h008: 7/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 8
}
```

## 2026-10-17T21:31:03+03:00 — medium_cv_api_progress

Fold1 h008: 8/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 9
}
```

## 2026-10-17T21:31:42+03:00 — medium_cv_api_progress

Fold1 h008: 9/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 10
}
```

## 2026-10-17T21:32:17+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 0.54243%

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.871781921351799,
    "val_metrics": {
      "map": 0.005424303147136954
    },
    "epoch_seconds": 511.99816768100027,
    "val_seconds": 4.2450445530012075,
    "rows": 10923,
    "lr_first": 2.60258358662614e-06,
    "lr_last": 1.1398176291793313e-08,
    "optimizer_updates": 2730,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:32:17+03:00 — recformer_ablation_trained

Recformer low_lr_warmup:4epochs trained; test not evaluated yet

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 4,
  "training_seconds": 2161.4252003680012,
  "best_trained_val_map": 0.005424303147136954
}
```

## 2026-10-17T21:32:33+03:00 — medium_cv_api_progress

Fold1 h008: 10/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 11
}
```

## 2026-10-17T21:33:17+03:00 — medium_cv_api_progress

Fold1 h008: 11/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 12
}
```

## 2026-10-17T21:33:18+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold1_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T21:33:50+03:00 — medium_cv_api_progress

Fold1 h008: 12/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 13
}
```

## 2026-10-17T21:34:02+03:00 — small_epoch

Малый idgnn: эпоха 1/10, validation MAP=0.0667%

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.08287959893544515,
  "val_metrics": {
    "map": 0.0006665426587301587
  },
  "train_seconds": 13.046602373000496,
  "val_seconds": 0.03340489399852231,
  "steps": 75
}
```

## 2026-10-17T21:34:05+03:00 — small_epoch

Малый idgnn: эпоха 2/10, validation MAP=0.0667%

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.049520180051525434,
  "val_metrics": {
    "map": 0.0006665426587301587
  },
  "train_seconds": 2.2658956849991228,
  "val_seconds": 0.03497451100156468,
  "steps": 75
}
```

## 2026-10-17T21:34:08+03:00 — small_epoch

Малый idgnn: эпоха 3/10, validation MAP=0.0667%

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.04701697962979476,
  "val_metrics": {
    "map": 0.0006665426587301587
  },
  "train_seconds": 2.3132096819990693,
  "val_seconds": 0.029844459000742063,
  "steps": 75
}
```

## 2026-10-17T21:34:10+03:00 — small_epoch

Малый idgnn: эпоха 4/10, validation MAP=0.0667%

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.04472771018743515,
  "val_metrics": {
    "map": 0.0006665426587301587
  },
  "train_seconds": 2.4872355580009753,
  "val_seconds": 0.030030302999875857,
  "steps": 75
}
```

## 2026-10-17T21:34:18+03:00 — small_epoch

Малый contextgnn: эпоха 1/10, validation MAP=0.0000%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 34.65563601175944,
  "val_metrics": {
    "map": 0.0
  },
  "train_seconds": 6.113447592999364,
  "val_seconds": 0.237106374999712,
  "steps": 75
}
```

## 2026-10-17T21:34:25+03:00 — medium_cv_api_progress

Fold1 h008: 13/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 14
}
```

## 2026-10-17T21:34:25+03:00 — small_epoch

Малый contextgnn: эпоха 2/10, validation MAP=0.0043%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 22.434617156982423,
  "val_metrics": {
    "map": 4.340277777777777e-05
  },
  "train_seconds": 6.09272281199992,
  "val_seconds": 0.23417651300042053,
  "steps": 75
}
```

## 2026-10-17T21:34:33+03:00 — small_epoch

Малый contextgnn: эпоха 3/10, validation MAP=0.0049%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 22.11559361775716,
  "val_metrics": {
    "map": 4.8828125e-05
  },
  "train_seconds": 5.663129806000143,
  "val_seconds": 0.1917555390009511,
  "steps": 75
}
```

## 2026-10-17T21:34:39+03:00 — small_epoch

Малый contextgnn: эпоха 4/10, validation MAP=0.0112%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 22.542680689493814,
  "val_metrics": {
    "map": 0.00011160714285714287
  },
  "train_seconds": 5.486063193000518,
  "val_seconds": 0.20024721200024942,
  "steps": 75
}
```

## 2026-10-17T21:34:46+03:00 — small_epoch

Малый contextgnn: эпоха 5/10, validation MAP=0.0000%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 5,
  "train_loss": 21.63896464029948,
  "val_metrics": {
    "map": 0.0
  },
  "train_seconds": 5.60734124299961,
  "val_seconds": 0.2106500869995216,
  "steps": 75
}
```

## 2026-10-17T21:34:52+03:00 — small_epoch

Малый contextgnn: эпоха 6/10, validation MAP=0.0289%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 6,
  "train_loss": 21.31058926900228,
  "val_metrics": {
    "map": 0.00028935185185185184
  },
  "train_seconds": 5.464360260999456,
  "val_seconds": 0.20675685799869825,
  "steps": 75
}
```

## 2026-10-17T21:34:59+03:00 — small_epoch

Малый contextgnn: эпоха 7/10, validation MAP=0.0372%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 7,
  "train_loss": 21.050119959513346,
  "val_metrics": {
    "map": 0.0003720238095238095
  },
  "train_seconds": 5.730423629000143,
  "val_seconds": 0.20249182699990342,
  "steps": 75
}
```

## 2026-10-17T21:35:07+03:00 — small_epoch

Малый contextgnn: эпоха 8/10, validation MAP=0.1420%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 8,
  "train_loss": 20.910811665852865,
  "val_metrics": {
    "map": 0.0014204545454545453
  },
  "train_seconds": 6.11204190799981,
  "val_seconds": 0.22018225799911306,
  "steps": 75
}
```

## 2026-10-17T21:35:14+03:00 — small_epoch

Малый contextgnn: эпоха 9/10, validation MAP=0.0592%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 9,
  "train_loss": 21.438934224446616,
  "val_metrics": {
    "map": 0.0005918560606060605
  },
  "train_seconds": 6.013053691000096,
  "val_seconds": 0.21104274299977988,
  "steps": 75
}
```

## 2026-10-17T21:35:18+03:00 — medium_cv_api_progress

Fold1 h008: 14/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 15
}
```

## 2026-10-17T21:35:21+03:00 — small_epoch

Малый contextgnn: эпоха 10/10, validation MAP=0.1612%

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "training",
  "epoch": 10,
  "train_loss": 20.87695142110189,
  "val_metrics": {
    "map": 0.0016121031746031745
  },
  "train_seconds": 5.83315403099914,
  "val_seconds": 0.20101257900023484,
  "steps": 75
}
```

## 2026-10-17T21:35:52+03:00 — medium_cv_api_progress

Fold1 h008: 15/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 16
}
```

## 2026-10-17T21:35:56+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 1800,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "fixed",
    "run_id": "hm_medium_cv_v2_fold1_tdm_fixed",
    "subset_sha256": "7ae21022d095be49b701cb85748b4f475349ec8306b8ba55eb6fe2da58372f66",
    "data_hashes": {
      "article_id_map.csv": "1bd670ffb49641faf3381c3de3af962e652c167366dcab36b7271474c629d5a1",
      "customer_id_map.csv": "1d64bdeafa0c5ab8c0d6187943b5d1d5edbfb35d7bb3f87816f076811f24d1c9",
      "db/article.parquet": "d30e5b0075f792d6d3b52d315ae8c2f23fe787fc01d87aa5e533ca80e9e19cb5",
      "db/customer.parquet": "9e5b831bbd8e49e8ac910d0da6c5d14bd17bcf4674288b42a6234fadb9042489",
      "db/transactions.parquet": "6a88fb46636e38d4c76a26998b0038e92ddc7099f27fe9dffeaf9fd1bb9e716c",
      "manifest.yaml": "efbe22ac38f7d8d31503d82f4b26466024a94d72d9c097de857fb133f94e1520",
      "selection.json": "fbf9853f8ad633acb8d54c033bcf609d0b3846b6c260e3fd07f88192811b4ec6",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "fc9f3395c335ea1a194f1a58072d645b07cbc2b4995bd23094c7f648b516e124",
      "tasks/user-item-purchase/test_full.parquet": "fc9f3395c335ea1a194f1a58072d645b07cbc2b4995bd23094c7f648b516e124",
      "tasks/user-item-purchase/train.parquet": "ceaf7209c229a7924d23e76ff15d8f31d065f94b2622f01028bc7e8c508b9ae6",
      "tasks/user-item-purchase/val.parquet": "d900e245b24af97cfba768292ab0b1810625f80fa168fcc21d27812823f8c81a",
      "tasks/user-item-purchase/val_full.parquet": "5a18107f3e4d7bcbc4adb0fe63a1816be92ef16cbbf97dd6e6d631f4fabb24e1"
    },
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379",
    "prerequisite": {
      "tree": "fixed categories; no clustering"
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 833295
  }
}
```

## 2026-10-17T21:36:34+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 1,
  "val_metrics": {
    "map": 0.0026266431051587304
  },
  "best_epoch": 1,
  "train_loss": 0.6651236429719365
}
```

## 2026-10-17T21:36:38+03:00 — medium_cv_api_progress

Fold1 h008: 16/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 17
}
```

## 2026-10-17T21:37:10+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 2,
  "val_metrics": {
    "map": 0.0026266431051587304
  },
  "best_epoch": 1,
  "train_loss": 0.6395228087786322
}
```

## 2026-10-17T21:37:21+03:00 — medium_cv_api_progress

Fold1 h008: 17/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 18
}
```

## 2026-10-17T21:37:45+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 3,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "best_epoch": 3,
  "train_loss": 0.6029836512618755
}
```

## 2026-10-17T21:37:58+03:00 — medium_cv_api_progress

Fold1 h008: 18/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 19
}
```

## 2026-10-17T21:38:20+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 4,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "best_epoch": 3,
  "train_loss": 0.530102447127599
}
```

## 2026-10-17T21:38:37+03:00 — medium_cv_api_progress

Fold1 h008: 19/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 20
}
```

## 2026-10-17T21:38:55+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 5,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "best_epoch": 3,
  "train_loss": 0.45190964879962364
}
```

## 2026-10-17T21:39:21+03:00 — medium_cv_api_progress

Fold1 h008: 20/20 accepted, 21 responses.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 21
}
```

## 2026-10-17T21:39:33+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 6,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "best_epoch": 3,
  "train_loss": 0.3903739437352344
}
```

## 2026-10-17T21:40:12+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 7,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "best_epoch": 3,
  "train_loss": 0.34375564383419055
}
```

## 2026-10-17T21:40:12+03:00 — tdm_training_complete

TDM training complete; test not evaluated

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "trained_pending_test",
  "epoch": 7,
  "val_metrics": {
    "map": 0.0046178582702020195
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/tdm/fixed",
  "summary": {
    "best_epoch": 3,
    "epochs": 7,
    "best_validation_map": 0.0046178582702020195,
    "training_and_validation_seconds": 244.9855264939997,
    "peak_cuda_bytes": 108993536,
    "stop_reason": "patience4",
    "checkpoint_sha256": "6bee87ce61afac8b755b3d77c56f7af6aac81990637a60e4a643620dc9150bb9",
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379"
  }
}
```

## 2026-10-17T21:40:30+03:00 — medium_cv_api_selected

Fold1 h008:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:41:17+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 1e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "low_lr_warmup",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 148110336,
      "frozen": 0
    },
    "freeze_policy": "none",
    "scheduler": "100 successful optimizer updates warmup, then linear decay over1204 updates",
    "warmup_updates": 100,
    "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog10000",
    "subset_sha256": "7ae21022d095be49b701cb85748b4f475349ec8306b8ba55eb6fe2da58372f66",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "9ef731d89c6fbb594a667a538209d1e783a4c4c1dbc91bc20b04a5ee88cfbf5e",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-17T21:41:25+03:00 — medium_cv_api_progress

Fold1 h009: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T21:41:58+03:00 — medium_cv_api_progress

Fold1 h009: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T21:42:37+03:00 — medium_cv_api_progress

Fold1 h009: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T21:43:31+03:00 — medium_cv_api_progress

Fold1 h009: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T21:44:02+03:00 — medium_cv_checkpoint_status_verified

Fold0 idgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.000759548611111111
  }
}
```

## 2026-10-17T21:44:02+03:00 — medium_cv_checkpoint_status_verified

Fold0 contextgnn: training finished; selected epoch 5; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 8,
  "best_epoch": 5,
  "val_metrics": {
    "map": 0.0029578711219336216
  }
}
```

## 2026-10-17T21:44:03+03:00 — medium_cv_checkpoint_status_verified

Fold1 idgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.0006665426587301587
  }
}
```

## 2026-10-17T21:44:03+03:00 — medium_cv_checkpoint_status_verified

Fold1 contextgnn: training finished; selected epoch 10; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 10,
  "best_epoch": 10,
  "val_metrics": {
    "map": 0.0016121031746031745
  }
}
```

## 2026-10-17T21:44:03+03:00 — medium_cv_completed_selection_audit

Checked 3 completed API searches:20 distinct accepted programs each, exact message histories and selected hashes; no outer evaluation.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training",
  "artifacts": "reports/medium_cv_v2/completed_selection_audit.json"
}
```

## 2026-10-17T21:44:19+03:00 — medium_cv_api_progress

Fold1 h009: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T21:45:06+03:00 — medium_cv_api_progress

Fold1 h009: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T21:45:47+03:00 — medium_cv_api_progress

Fold1 h009: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T21:46:35+03:00 — medium_cv_api_progress

Fold1 h009: 8/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8
}
```

## 2026-10-17T21:47:23+03:00 — medium_cv_api_progress

Fold1 h009: 9/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9
}
```

## 2026-10-17T21:47:58+03:00 — medium_cv_api_progress

Fold1 h009: 10/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10
}
```

## 2026-10-17T21:48:34+03:00 — medium_cv_api_progress

Fold1 h009: 11/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 11
}
```

## 2026-10-17T21:49:23+03:00 — medium_cv_api_progress

Fold1 h009: 12/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 12
}
```

## 2026-10-17T21:50:14+03:00 — medium_cv_api_progress

Fold1 h009: 13/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 13
}
```

## 2026-10-17T21:50:37+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 0.05875%

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 9.050017480261138,
    "val_metrics": {
      "map": 0.0005874875992063493
    },
    "epoch_seconds": 479.40337134900074,
    "val_seconds": 3.9702435609997337,
    "rows": 9583,
    "lr_first": 1.0000000000000001e-07,
    "lr_last": 7.839721254355401e-06,
    "optimizer_updates": 597,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:50:52+03:00 — medium_cv_api_progress

Fold1 h009: 14/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 14
}
```

## 2026-10-17T21:51:42+03:00 — medium_cv_api_progress

Fold1 h009: 15/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 15
}
```

## 2026-10-17T21:52:21+03:00 — medium_cv_api_progress

Fold1 h009: 16/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 16
}
```

## 2026-10-17T21:52:58+03:00 — medium_cv_api_progress

Fold1 h009: 17/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 17
}
```

## 2026-10-17T21:53:48+03:00 — medium_cv_api_progress

Fold1 h009: 18/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 18
}
```

## 2026-10-17T21:54:27+03:00 — medium_cv_api_progress

Fold1 h009: 19/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 19
}
```

## 2026-10-17T21:55:09+03:00 — medium_cv_api_progress

Fold1 h009: 20/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 20
}
```

## 2026-10-17T21:56:35+03:00 — medium_cv_api_selected

Fold1 h009:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:56:52+03:00 — medium_cv_tree_trained

Fold2 manual: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold2_manual`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:57:02+03:00 — medium_cv_tree_trained

Fold2 raw15: trained on shared saved pairs.

Запуск: `hm_medium_cv_v2_fold2_raw15`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T21:58:54+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 0.17869%

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.971188939871494,
    "val_metrics": {
      "map": 0.0017868768601190476
    },
    "epoch_seconds": 467.1392990830009,
    "val_seconds": 4.009381514999404,
    "rows": 9583,
    "lr_first": 7.835365853658538e-06,
    "lr_last": 5.2308362369337985e-06,
    "optimizer_updates": 1196,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T21:59:25+03:00 — medium_cv_api_progress

Fold2 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T22:01:23+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T22:01:46+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 3
}
```

## 2026-10-17T22:02:49+03:00 — medium_cv_continuation_audit

Fold1 H008/H009 selections completed with20 accepted each. GPU Recformer fold1 stage2 epoch1 active; CPU H008fold2 call4 passed preflight after call3 actual generated-code error: window-filtered values paired with full-history MultiIndex; correct rejection before fitting. Existing controllers alive; no outer scores.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:02:51+03:00 — medium_cv_api_progress

Fold2 h008: 3/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 4
}
```

## 2026-10-17T22:03:18+03:00 — medium_cv_error

f0_tdm_train failed; inspect /mnt/c/Users/Мишаня/ml/projs/tbank/Features/reports/medium_cv_v2/stages/f0_tdm_train.log; f2_h008_search failed; inspect /mnt/c/Users/Мишаня/ml/projs/tbank/Features/reports/medium_cv_v2/stages/f2_h008_search.log

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "interrupted",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T22:06:28+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 0.07778%

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.89349664153161,
    "val_metrics": {
      "map": 0.0007777622767857142
    },
    "epoch_seconds": 434.8968037169998,
    "val_seconds": 3.737769561999812,
    "rows": 9583,
    "lr_first": 5.226480836236935e-06,
    "lr_last": 2.6219512195121956e-06,
    "optimizer_updates": 1795,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T22:10:05+03:00 — medium_cv_api_transport_resume

Resuming interrupted fold2 API lane after transport failure; saved responses reused, actual POST5 failure retained in300-attempt budget. Arm execution locks prevent overlap with GPU recovery controller.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:10:16+03:00 — medium_cv_api_progress

Fold2 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T22:10:16+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T22:10:17+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 3
}
```

## 2026-10-17T22:10:17+03:00 — medium_cv_api_progress

Fold2 h008: 3/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 4
}
```

## 2026-10-17T22:11:02+03:00 — medium_cv_api_progress

Fold2 h008: 4/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 5
}
```

## 2026-10-17T22:11:18+03:00 — medium_cv_api_restored

API recovery verified: fold2 H008 call5 received on actualPOST6, passed preflight and trained successfully (searchMAP .00520244212962963); four accepted now, prior selections preserved. FailedPOST5 remains recorded. Lock regression passed with zero new API or fits. GPU Recformer fold1 still training; outer tests not scored.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:11:39+03:00 — medium_cv_log_precision_correction

Correction to preceding restoration note: exact call5 search MAP from trial.json is0.0052024382590788835. Preceding message incorrectly expanded the rounded console score; trial.json and all experiment data were unchanged.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:12:37+03:00 — medium_cv_api_progress

Fold2 h008: 5/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 6
}
```

## 2026-10-17T22:13:26+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 7
}
```

## 2026-10-17T22:13:45+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 8
}
```

## 2026-10-17T22:14:01+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 0.08092%

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.850581478793952,
    "val_metrics": {
      "map": 0.0008091517857142857
    },
    "epoch_seconds": 441.1847353690009,
    "val_seconds": 4.118304243002058,
    "rows": 9583,
    "lr_first": 2.617595818815331e-06,
    "lr_last": 1.3066202090592337e-08,
    "optimizer_updates": 2394,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T22:14:01+03:00 — recformer_ablation_trained

Recformer low_lr_warmup:4epochs trained; test not evaluated yet

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 4,
  "training_seconds": 1888.1977026929999,
  "best_trained_val_map": 0.0017868768601190476
}
```

## 2026-10-17T22:14:45+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold2_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T22:14:58+03:00 — medium_cv_api_progress

Fold2 h008: 7/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 9
}
```

## 2026-10-17T22:15:27+03:00 — small_epoch

Малый idgnn: эпоха 1/10, validation MAP=0.0453%

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 0.12572358365156758,
  "val_metrics": {
    "map": 0.00045262896825396827
  },
  "train_seconds": 15.97686351700031,
  "val_seconds": 0.03142127200044342,
  "steps": 67
}
```

## 2026-10-17T22:15:30+03:00 — small_epoch

Малый idgnn: эпоха 2/10, validation MAP=0.0453%

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 0.04816415146994057,
  "val_metrics": {
    "map": 0.00045262896825396827
  },
  "train_seconds": 2.6387490809975134,
  "val_seconds": 0.036327709996839985,
  "steps": 67
}
```

## 2026-10-17T22:15:33+03:00 — small_epoch

Малый idgnn: эпоха 3/10, validation MAP=0.0453%

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 0.04450389328621217,
  "val_metrics": {
    "map": 0.00045262896825396827
  },
  "train_seconds": 2.9682545459982066,
  "val_seconds": 0.03212171500126715,
  "steps": 67
}
```

## 2026-10-17T22:15:37+03:00 — small_epoch

Малый idgnn: эпоха 4/10, validation MAP=0.0453%

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 0.04389295935519596,
  "val_metrics": {
    "map": 0.00045262896825396827
  },
  "train_seconds": 2.7333997120003914,
  "val_seconds": 0.03192098999716109,
  "steps": 67
}
```

## 2026-10-17T22:17:34+03:00 — medium_cv_wsl_restart

WSL uptime under1minute, no experiment processes alive, GPU idle. Recformer fold1 completed; fold2 IDGNN trained.json exists. H008fold2 has7 accepted/9 completed responses; call10 response and partial artifacts saved, no trial/result yet. Preserved partial candidate10 and stale process statuses in runtime/wsl_restart_2216. All17 source hashes match. Resume existing pipeline with no protocol changes; saved responses reused, incomplete call10 fitting may repeat after interruption.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "resuming"
}
```

## 2026-10-17T22:17:55+03:00 — medium_cv_resumed

Starting nine-method temporal CV; three reset folds; no Qwen/Llama. Outer scoring gated until all selections frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T22:17:55+03:00 — medium_cv_running

Validator and GPU smoke checks passed. CPU/API and GPU lanes begin; no outer-test scores available.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:18:04+03:00 — medium_cv_api_progress

Fold2 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T22:18:05+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T22:18:05+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 3
}
```

## 2026-10-17T22:18:05+03:00 — medium_cv_api_progress

Fold2 h008: 3/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 4
}
```

## 2026-10-17T22:18:05+03:00 — medium_cv_api_progress

Fold2 h008: 4/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 5
}
```

## 2026-10-17T22:18:06+03:00 — medium_cv_api_progress

Fold2 h008: 5/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 6
}
```

## 2026-10-17T22:18:06+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 7
}
```

## 2026-10-17T22:18:06+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 8
}
```

## 2026-10-17T22:18:07+03:00 — medium_cv_api_progress

Fold2 h008: 7/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 9
}
```

## 2026-10-17T22:18:27+03:00 — medium_cv_api_progress

Fold2 h008: 8/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 10
}
```

## 2026-10-17T22:18:31+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold2_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T22:19:01+03:00 — medium_cv_restart_verified

After WSL restart, new pipelinePID1342 and both child lanes confirmed alive. Saved call10 response reused and evaluation completed, H008fold2 now8 accepted; call11 in progress. Completed first two folds and IDGNNfold2 reused. Model source hashes unchanged; no outer-test evaluation yet.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:19:17+03:00 — medium_cv_api_progress

Fold2 h008: 9/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 11
}
```

## 2026-10-17T22:19:17+03:00 — small_epoch

Малый contextgnn: эпоха 1/10, validation MAP=0.0195%

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "training",
  "epoch": 1,
  "train_loss": 31.801424368103937,
  "val_metrics": {
    "map": 0.0001953125
  },
  "train_seconds": 21.017944204000003,
  "val_seconds": 0.20472748700001375,
  "steps": 67
}
```

## 2026-10-17T22:19:23+03:00 — small_epoch

Малый contextgnn: эпоха 2/10, validation MAP=0.0000%

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "training",
  "epoch": 2,
  "train_loss": 21.16683606959101,
  "val_metrics": {
    "map": 0.0
  },
  "train_seconds": 4.819035233999983,
  "val_seconds": 0.18659307799998714,
  "steps": 67
}
```

## 2026-10-17T22:19:29+03:00 — small_epoch

Малый contextgnn: эпоха 3/10, validation MAP=0.0000%

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "training",
  "epoch": 3,
  "train_loss": 21.985516904005365,
  "val_metrics": {
    "map": 0.0
  },
  "train_seconds": 4.904291075999993,
  "val_seconds": 0.18912270300000955,
  "steps": 67
}
```

## 2026-10-17T22:19:35+03:00 — small_epoch

Малый contextgnn: эпоха 4/10, validation MAP=0.0000%

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "training",
  "epoch": 4,
  "train_loss": 20.068540345377,
  "val_metrics": {
    "map": 0.0
  },
  "train_seconds": 5.021959753000004,
  "val_seconds": 0.198231241000002,
  "steps": 67
}
```

## 2026-10-17T22:19:35+03:00 — medium_cv_api_progress

Fold2 h008: 9/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 12
}
```

## 2026-10-17T22:20:09+03:00 — tdm_training_start

TDM small weekly training; fixed validation selection

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "embedding_dim": 24,
    "windows": [
      1,
      1,
      1,
      2,
      2,
      2,
      5,
      6,
      10,
      20
    ],
    "hidden": [
      128,
      64,
      24
    ],
    "attention_hidden": 36,
    "batch": 32,
    "pair_chunk": 512,
    "max_epochs": 20,
    "patience": 4,
    "minimum_epochs": 5,
    "max_training_seconds": 1800,
    "lr": 0.001,
    "negatives_per_level": 8,
    "beam": 64,
    "history_length": 50,
    "precision": "FP32",
    "objective": "equal-user equal-level balanced multi-positive BCE",
    "tree_selection": "best beam64 validation MAP; strict improvement",
    "upstream_reference": "TorchEasyRec 4458f1c66f6c32dc672b9c805855f3d2e6e6179e",
    "implementation": "local adaptation; no upstream framework installed",
    "variant": "fixed",
    "run_id": "hm_medium_cv_v2_fold2_tdm_fixed",
    "subset_sha256": "1f83dbb1e24d59b9737ece7746464478697969a5a24ff01a7e7d2926f39d5a87",
    "data_hashes": {
      "article_id_map.csv": "1bd670ffb49641faf3381c3de3af962e652c167366dcab36b7271474c629d5a1",
      "customer_id_map.csv": "1d64bdeafa0c5ab8c0d6187943b5d1d5edbfb35d7bb3f87816f076811f24d1c9",
      "db/article.parquet": "d30e5b0075f792d6d3b52d315ae8c2f23fe787fc01d87aa5e533ca80e9e19cb5",
      "db/customer.parquet": "9e5b831bbd8e49e8ac910d0da6c5d14bd17bcf4674288b42a6234fadb9042489",
      "db/transactions.parquet": "6a88fb46636e38d4c76a26998b0038e92ddc7099f27fe9dffeaf9fd1bb9e716c",
      "manifest.yaml": "8ebd3c2e78363f344c303f2cdc1324cf209bdddee0fc1add05df2e681258372a",
      "selection.json": "92ea83cede629a55606fc3dc7e9dbf612da8156261b4e7826dac4052406b5c2e",
      "tasks/user-item-purchase/manifest.yaml": "3b2acb699377f9074a11a9033507ec2ca32b7ce2e03c78a90b488ee2216e9281",
      "tasks/user-item-purchase/test.parquet": "974e443c2e0d889c9a17bd9c74ea531d57e83091e049f9ef16aa1e931ceb224c",
      "tasks/user-item-purchase/test_full.parquet": "974e443c2e0d889c9a17bd9c74ea531d57e83091e049f9ef16aa1e931ceb224c",
      "tasks/user-item-purchase/train.parquet": "7a5706c114da806df7ca6f8f43ecd17c527e6b7ba44a8fd8d08139fee5a2ed40",
      "tasks/user-item-purchase/val.parquet": "668cefba71c3fe9467cf2fbb647ef26c31611243d64035432c513dd852027a8a",
      "tasks/user-item-purchase/val_full.parquet": "5ba80ef398346aacc2ac4f32079efa336ab5bfcfda3f4f5881b95ca9d39924a1"
    },
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379",
    "prerequisite": {
      "tree": "fixed categories; no clustering"
    },
    "code_sha256": {
      "check_protocol.py": "b709798d6bbc705d6096fc6867f2df50a1c6c78987093466f8217075e4e3c4bb",
      "check_runtime.py": "502c0ad06477b626394357b1c1469dc77cb05778929012cea47b86ed66dd2c69",
      "common.py": "80c9013353db6142bf45cc1d27629cd3b4ac1a7d6f0a3307cea8989f9cd71f34",
      "report_small.py": "54ad0554c9ed7d88d9b27a8396da539929478e7f06885b6c1709188fdc76caa0",
      "run_small.py": "bbe968276d3a88ce0c7f42fabddf3d9a7b0f0c9ac8c10ccb303f93e2e340b278"
    },
    "torch_version": "2.2.2+cu118",
    "gpu": "NVIDIA GeForce RTX 3060 Laptop GPU",
    "trainable_parameters": 833295
  }
}
```

## 2026-10-17T22:20:45+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 1,
  "val_metrics": {
    "map": 0.002579365079365079
  },
  "best_epoch": 1,
  "train_loss": 0.6665506306222901
}
```

## 2026-10-17T22:21:07+03:00 — medium_cv_api_progress

Fold2 h008: 10/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 13
}
```

## 2026-10-17T22:21:17+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 2,
  "val_metrics": {
    "map": 0.0036982548701298703
  },
  "best_epoch": 2,
  "train_loss": 0.6394105540382796
}
```

## 2026-10-17T22:21:50+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 3,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "best_epoch": 3,
  "train_loss": 0.6178774681944874
}
```

## 2026-10-17T22:22:24+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 4,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "best_epoch": 3,
  "train_loss": 0.5527332957663387
}
```

## 2026-10-17T22:22:24+03:00 — medium_cv_api_progress

Fold2 h008: 11/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 14
}
```

## 2026-10-17T22:22:55+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 5,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "best_epoch": 3,
  "train_loss": 0.4527501026071771
}
```

## 2026-10-17T22:23:12+03:00 — medium_cv_api_progress

Fold2 h008: 12/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 15
}
```

## 2026-10-17T22:23:27+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 6,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "best_epoch": 3,
  "train_loss": 0.38660256596147896
}
```

## 2026-10-17T22:23:55+03:00 — tdm_epoch

TDM complete epoch and beam validation

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "training",
  "epoch": 7,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "best_epoch": 3,
  "train_loss": 0.33820404855000136
}
```

## 2026-10-17T22:23:55+03:00 — tdm_training_complete

TDM training complete; test not evaluated

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "trained_pending_test",
  "epoch": 7,
  "val_metrics": {
    "map": 0.006591162743506494
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/tdm/fixed",
  "summary": {
    "best_epoch": 3,
    "epochs": 7,
    "best_validation_map": 0.006591162743506494,
    "training_and_validation_seconds": 219.290067177,
    "peak_cuda_bytes": 108993536,
    "stop_reason": "patience4",
    "checkpoint_sha256": "693a1257ccdf11d225b233d989f1bcede1616a9d4c6cd540853e5324301cd046",
    "tree_sha256": "26bae1bd4f30d3890eeec4c60dc19d4e1ca4f66fd3a383599f089ae182378379"
  }
}
```

## 2026-10-17T22:24:49+03:00 — recformer_start

Recformer small: zero-shot plus two-stage fine-tuning, frozen small subset

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "training",
  "config": {
    "seed": 42,
    "max_tokens": 256,
    "max_items": 50,
    "attributes": 3,
    "max_attr_length": 32,
    "batch": 4,
    "gradient_accumulation": 4,
    "epochs_per_stage": 2,
    "stages": 2,
    "lr": 1e-05,
    "weight_decay": 0.0,
    "precision": "FP16 autocast; FP32 normalized cosine matmul",
    "variant": "low_lr_warmup",
    "parameter_counts": {
      "total": 148110336,
      "trainable": 148110336,
      "frozen": 0
    },
    "freeze_policy": "none",
    "scheduler": "100 successful optimizer updates warmup, then linear decay over1204 updates",
    "warmup_updates": 100,
    "comparison_policy": "same pretrained initialization, seed/order/2+2 epochs; lower LR+schedule bundled; freezing separately versus original constant5e-5",
    "objective": "mean per-user-time mean positive negative-log full softmax; catalog10000",
    "subset_sha256": "1f83dbb1e24d59b9737ece7746464478697969a5a24ff01a7e7d2926f39d5a87",
    "pretrained_sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022",
    "source_commit": "26b00a58e7affe0c54a89c143ea7bce37f2e8e08",
    "runner_sha256": "8d7e4d998da1c5e35544772225f94492aadfcc0e933b09ff5d12e6a8c0a15e61",
    "asset_manifest": {
      "checkpoint_source": "https://github.com/AaronHeee/RecFormer#pretrained-model",
      "checkpoint_file_id": "1BEboY3NxAUOBe6YwYZ_RsQ4BR6IIbl0-",
      "backbone_repo": "allenai/longformer-base-4096",
      "backbone_revision": "301e6a42cb0d9976a6d6a26a079fef81c18aa895",
      "files": {
        "config.json": {
          "bytes": 694,
          "sha256": "d0a64aa58d1b43c0d38000fa3083c142533c59fa151043e5c8113bcbee106d82"
        },
        "merges.txt": {
          "bytes": 456318,
          "sha256": "1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5"
        },
        "recformer_seqrec.bin": {
          "bytes": 749479199,
          "sha256": "6ca01ee6ce48756e49b381da1fa6eedb8873cdeb6f96b13274e89a6b5884d022"
        },
        "vocab.json": {
          "bytes": 898823,
          "sha256": "9e7f63c2d15d666b52e21d250d2e513b87c9b713cfa6987a82ed89e5e6e50655"
        }
      }
    },
    "runtime": {
      "torch": "2.2.2+cu118",
      "transformers": "4.46.3",
      "numpy": "1.26.4",
      "pandas": "2.2.3"
    },
    "budget_policy": "4 full epochs; no test before checkpoint selection; no continuation under same run after changes"
  }
}
```

## 2026-10-17T22:32:03+03:00 — recformer_epoch

Recformer stage 1 epoch 1: val MAP 0.70499%

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "training",
  "epoch": 1,
  "progress": {
    "stage": 1,
    "epoch": 1,
    "train_loss": 9.054527326002821,
    "val_metrics": {
      "map": 0.007049851190476191
    },
    "epoch_seconds": 367.04135890500004,
    "val_seconds": 3.511879444999977,
    "rows": 8548,
    "lr_first": 1.0000000000000001e-07,
    "lr_last": 7.882352941176471e-06,
    "optimizer_updates": 533,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T22:38:47+03:00 — recformer_epoch

Recformer stage 1 epoch 2: val MAP 0.53432%

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "training",
  "epoch": 2,
  "progress": {
    "stage": 1,
    "epoch": 2,
    "train_loss": 8.97293454573207,
    "val_metrics": {
      "map": 0.005343191964285714
    },
    "epoch_seconds": 389.03474968599994,
    "val_seconds": 4.124963090999927,
    "rows": 8548,
    "lr_first": 7.877450980392158e-06,
    "lr_last": 5.259803921568628e-06,
    "optimizer_updates": 1068,
    "amp_skipped_updates": 2
  }
}
```

## 2026-10-17T22:39:10+03:00 — medium_cv_api_transport_resume

Resuming fold2 API lane after transport timeout; saved responses reused and failed POSTs remain in300-attempt budget. At most3 consecutive stage runs on transport/transient HTTP errors,30s delay; arm locks retained.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:39:21+03:00 — medium_cv_api_progress

Fold2 h008: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T22:39:21+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T22:39:22+03:00 — medium_cv_api_progress

Fold2 h008: 2/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 3
}
```

## 2026-10-17T22:39:22+03:00 — medium_cv_api_progress

Fold2 h008: 3/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 4
}
```

## 2026-10-17T22:39:23+03:00 — medium_cv_api_progress

Fold2 h008: 4/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 5
}
```

## 2026-10-17T22:39:23+03:00 — medium_cv_api_progress

Fold2 h008: 5/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 6
}
```

## 2026-10-17T22:39:24+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 7
}
```

## 2026-10-17T22:39:24+03:00 — medium_cv_api_progress

Fold2 h008: 6/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 8
}
```

## 2026-10-17T22:39:24+03:00 — medium_cv_api_progress

Fold2 h008: 7/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 9
}
```

## 2026-10-17T22:39:25+03:00 — medium_cv_api_progress

Fold2 h008: 8/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 10
}
```

## 2026-10-17T22:39:25+03:00 — medium_cv_api_progress

Fold2 h008: 9/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 11
}
```

## 2026-10-17T22:39:25+03:00 — medium_cv_api_progress

Fold2 h008: 9/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 12
}
```

## 2026-10-17T22:39:26+03:00 — medium_cv_api_progress

Fold2 h008: 10/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 13
}
```

## 2026-10-17T22:39:26+03:00 — medium_cv_api_progress

Fold2 h008: 11/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 14
}
```

## 2026-10-17T22:39:27+03:00 — medium_cv_api_progress

Fold2 h008: 12/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 15
}
```

## 2026-10-17T22:40:23+03:00 — medium_cv_vpn_connectivity_restored

After user restarted VPN, actualPOST18 for fold2H008call16 returned a response; preflight passed and candidate training/evaluation resumed. Prior timeoutPOST17 retained. Recformer fold2 stage2epoch1 active. Temporal association observed; VPN causality not established.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:41:58+03:00 — medium_cv_api_progress

Fold2 h008: 13/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 16
}
```

## 2026-10-17T22:43:23+03:00 — medium_cv_api_progress

Fold2 h008: 14/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 17
}
```

## 2026-10-17T22:44:27+03:00 — medium_cv_api_progress

Fold2 h008: 15/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 18
}
```

## 2026-10-17T22:45:46+03:00 — recformer_epoch

Recformer stage 2 epoch 1: val MAP 0.56548%

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "training",
  "epoch": 3,
  "progress": {
    "stage": 2,
    "epoch": 1,
    "train_loss": 8.930145223730905,
    "val_metrics": {
      "map": 0.005654761904761905
    },
    "epoch_seconds": 395.70310183100014,
    "val_seconds": 4.074909557999945,
    "rows": 8548,
    "lr_first": 5.254901960784314e-06,
    "lr_last": 2.6421568627450983e-06,
    "optimizer_updates": 1602,
    "amp_skipped_updates": 3
  }
}
```

## 2026-10-17T22:47:22+03:00 — medium_cv_api_progress

Fold2 h008: 16/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 19
}
```

## 2026-10-17T22:48:56+03:00 — medium_cv_api_progress

Fold2 h008: 17/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 20
}
```

## 2026-10-17T22:49:55+03:00 — medium_cv_api_progress

Fold2 h008: 18/20 accepted, 21 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 21
}
```

## 2026-10-17T22:51:56+03:00 — medium_cv_api_progress

Fold2 h008: 19/20 accepted, 22 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 22
}
```

## 2026-10-17T22:52:44+03:00 — recformer_epoch

Recformer stage 2 epoch 2: val MAP 0.91541%

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "training",
  "epoch": 4,
  "progress": {
    "stage": 2,
    "epoch": 2,
    "train_loss": 8.881475609934213,
    "val_metrics": {
      "map": 0.009154110863095238
    },
    "epoch_seconds": 396.429374629,
    "val_seconds": 4.73114808299988,
    "rows": 8548,
    "lr_first": 2.6372549019607847e-06,
    "lr_last": 1.9607843137254902e-08,
    "optimizer_updates": 2137,
    "amp_skipped_updates": 3
  }
}
```

## 2026-10-17T22:52:44+03:00 — recformer_ablation_trained

Recformer low_lr_warmup:4epochs trained; test not evaluated yet

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "trained_pending_evaluation",
  "epoch": 4,
  "training_seconds": 1609.4941478459998,
  "best_trained_val_map": 0.009154110863095238
}
```

## 2026-10-17T22:52:54+03:00 — medium_cv_error

f2_h008_search failed; inspect /mnt/c/Users/Мишаня/ml/projs/tbank/Features/reports/medium_cv_v2/stages/f2_h008_search.log

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "interrupted",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T22:53:33+03:00 — medium_cv_api_progress

Fold2 h008: 20/20 accepted, 23 responses.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 23
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold0 idgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.000759548611111111
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold0 contextgnn: training finished; selected epoch 5; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 8,
  "best_epoch": 5,
  "val_metrics": {
    "map": 0.0029578711219336216
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold1 idgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.0006665426587301587
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold1 contextgnn: training finished; selected epoch 10; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 10,
  "best_epoch": 10,
  "val_metrics": {
    "map": 0.0016121031746031745
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold2 idgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.00045262896825396827
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_checkpoint_status_verified

Fold2 contextgnn: training finished; selected epoch 1; outer scoring pending.

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "trained_pending_test",
  "epoch": 4,
  "best_epoch": 1,
  "val_metrics": {
    "map": 0.0001953125
  }
}
```

## 2026-10-17T22:53:48+03:00 — medium_cv_completed_selection_audit

Checked 4 completed API searches:20 distinct accepted programs each, exact message histories and selected hashes; no outer evaluation.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training",
  "artifacts": "reports/medium_cv_v2/completed_selection_audit.json"
}
```

## 2026-10-17T22:54:10+03:00 — medium_cv_all_gpu_training_done

All3fold GPU training stages complete, including Recformer4epochs per fold. API helper1973 active; H008fold2 reached20 accepted/23 completed responses,25 actualPOST; confirmation pending. H009fold2 follows, then helper restarts full completed-stage-aware pipeline. Main1342 exited after GPU work with prior CPUfuture failure; no new failure since VPN restart. Outer scoring still gated.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T22:55:14+03:00 — medium_cv_api_selected

Fold2 h008:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T22:56:06+03:00 — medium_cv_api_progress

Fold2 h009: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T22:56:43+03:00 — medium_cv_api_progress

Fold2 h009: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T22:57:22+03:00 — medium_cv_api_progress

Fold2 h009: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T22:58:02+03:00 — medium_cv_api_progress

Fold2 h009: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T22:58:39+03:00 — medium_cv_api_progress

Fold2 h009: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T22:59:08+03:00 — medium_cv_api_progress

Fold2 h009: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T22:59:46+03:00 — medium_cv_api_progress

Fold2 h009: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T23:00:21+03:00 — medium_cv_api_progress

Fold2 h009: 8/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8
}
```

## 2026-10-17T23:01:03+03:00 — medium_cv_api_progress

Fold2 h009: 9/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9
}
```

## 2026-10-17T23:01:44+03:00 — medium_cv_api_progress

Fold2 h009: 10/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10
}
```

## 2026-10-17T23:02:33+03:00 — medium_cv_api_progress

Fold2 h009: 11/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 11
}
```

## 2026-10-17T23:03:06+03:00 — medium_cv_health_check

Health check: APIhelper1973 and H009fold2child2793 alive. H008fold2 selection complete(20 accepted,23 responses); H009fold2 has11 accepted/11 completed responses, call12 evaluating; no network failures in this arm. GPU idle as all training finished. Helper will relaunch pipeline after final selection; outer test not started.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T23:03:38+03:00 — medium_cv_api_progress

Fold2 h009: 12/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 12
}
```

## 2026-10-17T23:04:19+03:00 — medium_cv_api_progress

Fold2 h009: 13/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 13
}
```

## 2026-10-17T23:04:59+03:00 — medium_cv_api_progress

Fold2 h009: 14/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 14
}
```

## 2026-10-17T23:05:44+03:00 — medium_cv_api_progress

Fold2 h009: 15/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 15
}
```

## 2026-10-17T23:06:29+03:00 — medium_cv_api_progress

Fold2 h009: 16/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 16
}
```

## 2026-10-17T23:07:13+03:00 — medium_cv_api_progress

Fold2 h009: 17/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 17
}
```

## 2026-10-17T23:07:57+03:00 — medium_cv_api_progress

Fold2 h009: 18/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 18
}
```

## 2026-10-17T23:08:48+03:00 — medium_cv_api_progress

Fold2 h009: 19/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 19
}
```

## 2026-10-17T23:11:08+03:00 — medium_cv_api_transient_retry

Fold2 h009: transient provider error; resume in30s, stage retry1/2; actual POST budget unchanged.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T23:11:48+03:00 — medium_cv_api_progress

Fold2 h009: 1/20 accepted, 1 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 1,
  "responses": 1
}
```

## 2026-10-17T23:11:48+03:00 — medium_cv_api_progress

Fold2 h009: 2/20 accepted, 2 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 2,
  "responses": 2
}
```

## 2026-10-17T23:11:49+03:00 — medium_cv_api_progress

Fold2 h009: 3/20 accepted, 3 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 3,
  "responses": 3
}
```

## 2026-10-17T23:11:49+03:00 — medium_cv_api_progress

Fold2 h009: 4/20 accepted, 4 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 4,
  "responses": 4
}
```

## 2026-10-17T23:11:49+03:00 — medium_cv_api_progress

Fold2 h009: 5/20 accepted, 5 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 5,
  "responses": 5
}
```

## 2026-10-17T23:11:50+03:00 — medium_cv_api_progress

Fold2 h009: 6/20 accepted, 6 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 6,
  "responses": 6
}
```

## 2026-10-17T23:11:50+03:00 — medium_cv_api_progress

Fold2 h009: 7/20 accepted, 7 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 7,
  "responses": 7
}
```

## 2026-10-17T23:11:50+03:00 — medium_cv_api_progress

Fold2 h009: 8/20 accepted, 8 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 8,
  "responses": 8
}
```

## 2026-10-17T23:11:51+03:00 — medium_cv_api_progress

Fold2 h009: 9/20 accepted, 9 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 9,
  "responses": 9
}
```

## 2026-10-17T23:11:51+03:00 — medium_cv_api_progress

Fold2 h009: 10/20 accepted, 10 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 10,
  "responses": 10
}
```

## 2026-10-17T23:11:51+03:00 — medium_cv_api_progress

Fold2 h009: 11/20 accepted, 11 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 11,
  "responses": 11
}
```

## 2026-10-17T23:11:52+03:00 — medium_cv_api_progress

Fold2 h009: 12/20 accepted, 12 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 12,
  "responses": 12
}
```

## 2026-10-17T23:11:52+03:00 — medium_cv_api_progress

Fold2 h009: 13/20 accepted, 13 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 13,
  "responses": 13
}
```

## 2026-10-17T23:11:52+03:00 — medium_cv_api_progress

Fold2 h009: 14/20 accepted, 14 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 14,
  "responses": 14
}
```

## 2026-10-17T23:11:53+03:00 — medium_cv_api_progress

Fold2 h009: 15/20 accepted, 15 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 15,
  "responses": 15
}
```

## 2026-10-17T23:11:53+03:00 — medium_cv_api_progress

Fold2 h009: 16/20 accepted, 16 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 16,
  "responses": 16
}
```

## 2026-10-17T23:11:53+03:00 — medium_cv_api_progress

Fold2 h009: 17/20 accepted, 17 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 17,
  "responses": 17
}
```

## 2026-10-17T23:11:54+03:00 — medium_cv_api_progress

Fold2 h009: 18/20 accepted, 18 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 18,
  "responses": 18
}
```

## 2026-10-17T23:11:54+03:00 — medium_cv_api_progress

Fold2 h009: 19/20 accepted, 19 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 19,
  "responses": 19
}
```

## 2026-10-17T23:12:46+03:00 — medium_cv_api_progress

Fold2 h009: 20/20 accepted, 20 responses.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "searching",
  "measured": 20,
  "responses": 20
}
```

## 2026-10-17T23:12:52+03:00 — medium_cv_final_api_retry_received

Fold2H009call20: POST20 timed out at23:11, bounded resume replayed19 saved trials and sentPOST21. After user VPN restart, response saved at23:12:10; preflight passed, training/search active.19 accepted until evaluation completes. No earlier responses regenerated; failedPOST retained in300-budget.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T23:14:07+03:00 — medium_cv_api_selected

Fold2 h009:20 accepted, selection frozen before outer test.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "trained_pending_test"
}
```

## 2026-10-17T23:14:07+03:00 — medium_cv_api_resume_completed

Fold2 H008/H009 searches completed; waiting for existing controller before resuming full pipeline with completed-stage reuse.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T23:14:12+03:00 — medium_cv_resumed

Starting nine-method temporal CV; three reset folds; no Qwen/Llama. Outer scoring gated until all selections frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "verifying",
  "artifacts": "reports/medium_cv_v2"
}
```

## 2026-10-17T23:14:12+03:00 — medium_cv_running

Validator and GPU smoke checks passed. CPU/API and GPU lanes begin; no outer-test scores available.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "training"
}
```

## 2026-10-17T23:14:49+03:00 — medium_cv_pretest_barrier

All nine methods on all three folds selected; outer scoring now permitted.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-17T23:15:19+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T23:16:19+03:00 — small_context_start

Малый ContextGNN: независимый инференс

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T23:16:39+03:00 — small_model_verified

Независимая проверка idgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold0_idgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 6.132010645999799
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.39413183000033314
    },
    "checkpoint_sha256": "17f3d39bd3c0299bc450b73ce4c0ba121226b63e4f844fdd56cdb503bec4c350"
  }
}
```

## 2026-10-17T23:16:42+03:00 — small_model_verified

Независимая проверка contextgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold0_contextgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.450118927999938
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 1.2461239379999824
    },
    "checkpoint_sha256": "a251ed61b80f01f384ee6b04dfba454701f40f98c27516c6728e0bde6a761ccb"
  }
}
```

## 2026-10-17T23:20:26+03:00 — recformer_ablation_measured

Recformer low_lr_warmup zero_shot: measured; replay pending

Запуск: `hm_medium_cv_v2_fold0_recformer_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.008153909350198413
  },
  "test_metrics": {
    "map": 0.008612966847061464
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/recformer/zero_shot"
}
```

## 2026-10-17T23:21:01+03:00 — recformer_ablation_measured

Recformer low_lr_warmup finetuned: measured; replay pending

Запуск: `hm_medium_cv_v2_fold0_recformer_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.005424303147136954
  },
  "test_metrics": {
    "map": 0.004928330862942065
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/recformer/finetuned"
}
```

## 2026-10-17T23:23:06+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_medium_cv_v2_fold0_recformer_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.008153909350198413,
        "seconds": 9.697484712999994
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.008612966847061464,
        "seconds": 25.766506284000116
      },
      "checkpoint_sha256": "dc848016451b90999aa11ef3a8b957ad6b5e97e9ef402645785c2834ea287adf"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.005424303147136954,
        "seconds": 3.8384904560002724
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.004928330862942065,
        "seconds": 27.52184799400038
      },
      "checkpoint_sha256": "8ea881e128a19aac14cbdd5a359bfaa2c42423e4ccb21c4025dbf716ed58277e"
    }
  }
}
```

## 2026-10-17T23:29:32+03:00 — medium_cv_outer_evaluation_health

All6 API searches completed with20 accepted each(120 total); global selection_pretest barrier exists. New controller4552 active. Fold0 GNN/TDM/Recformer outer evaluation and full replays passed; manual evaluation complete, raw15 evaluation running. No fresh failures; old failure.json predates new controller. No model/prompt changes after outer scoring began.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-17T23:40:08+03:00 — medium_cv_scoring_health

Controller4552 and H009fold0 evaluation worker alive. Fold0 eight of nine methods evaluated and verified: GNN2, Recformer2, TDM, manual, raw15, H008. H009fold0 is in progress; then folds1/2 follow. No fresh failures; GPU idle during CPU scoring is expected. Prior failed-controller record remains historical.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-17T23:43:27+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold1_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T23:44:42+03:00 — small_context_start

Малый ContextGNN: независимый инференс

Запуск: `hm_medium_cv_v2_fold1_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-17T23:45:18+03:00 — small_model_verified

Независимая проверка idgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold1_idgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 10.913856116000716
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.4299358389998815
    },
    "checkpoint_sha256": "fd249fc6763c8f7cfb09814c2d14834a80db4acfd356671cc23c70e33b88b5be"
  }
}
```

## 2026-10-17T23:45:22+03:00 — small_model_verified

Независимая проверка contextgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold1_contextgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.37058369199985464
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 1.3793569079998633
    },
    "checkpoint_sha256": "22b7b11d1f41409652e08ed286c7c36681d3e8ce044a863d6cd9bf8053a94fb7"
  }
}
```

## 2026-10-17T23:48:55+03:00 — medium_cv_second_fold_scoring_health

Controller4552 alive. Fold0 all9 methods evaluated and verified. Fold1 GNN2 and TDM evaluated with successful replays; Recformer evaluation loading/running, then tree methods. No fresh failures; old failure.json remains from prior controller. All model choices stay frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-17T23:50:11+03:00 — recformer_ablation_measured

Recformer low_lr_warmup zero_shot: measured; replay pending

Запуск: `hm_medium_cv_v2_fold1_recformer_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.0021577380952380954
  },
  "test_metrics": {
    "map": 0.004664410247785625
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/recformer/zero_shot"
}
```

## 2026-10-17T23:50:48+03:00 — recformer_ablation_measured

Recformer low_lr_warmup finetuned: measured; replay pending

Запуск: `hm_medium_cv_v2_fold1_recformer_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.0017868768601190476
  },
  "test_metrics": {
    "map": 0.003784240038654771
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/recformer/finetuned"
}
```

## 2026-10-17T23:53:13+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_medium_cv_v2_fold1_recformer_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.0021577380952380954,
        "seconds": 13.099791110999831
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.004664410247785625,
        "seconds": 26.902163176999238
      },
      "checkpoint_sha256": "dc848016451b90999aa11ef3a8b957ad6b5e97e9ef402645785c2834ea287adf"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.0017868768601190476,
        "seconds": 3.5990127310005846
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.003784240038654771,
        "seconds": 26.909847835999244
      },
      "checkpoint_sha256": "a05ab632e5d7c6a14c609a2096819d8939bc40d29d2764441dda7320df3ae26c"
    }
  }
}
```

## 2026-10-18T00:02:25+03:00 — medium_cv_second_fold_trees_health

Health check00:02MSK: controller4552 active. Fold1 seven methods evaluated and verified including manual/raw15; H008fold1 scoring/replay active(child5775), H009 follows. Fold0 all9 passed; fold2 not yet evaluated. No fresh failures;25GiB free disk. Models and selection remain frozen.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-18T00:11:10+03:00 — small_context_start

Малый ContextGNN пилот: подготовка графа

Запуск: `hm_medium_cv_v2_fold2_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-18T00:12:22+03:00 — small_context_start

Малый ContextGNN: независимый инференс

Запуск: `hm_medium_cv_v2_fold2_gnn`.

```json
{
  "status": "preparing",
  "config": {
    "dataset": "rel-hm-small-v1",
    "seed": 42,
    "channels": 64,
    "encoder_channels": 64,
    "encoder_layers": 2,
    "layers": 2,
    "neighbors": [
      32,
      16
    ],
    "rhs_embedding_dim": 64,
    "rhs_mode": "FUSION",
    "batch_size": 128,
    "max_epochs": 10,
    "early_stopping_patience": 3,
    "lr": 0.001,
    "steps_per_epoch_cap": null,
    "temporal_strategy": "last",
    "evaluation": "all 10000 items; original full-target evaluation including unretrievable positives",
    "upstream_commit": "ca4a96985b7ef73c36a40da32e70710ad9b59a1e",
    "rhs_cache_policy": "clear before each evaluation and weight reload; avoid stale FUSION cache"
  }
}
```

## 2026-10-18T00:12:56+03:00 — small_model_verified

Независимая проверка idgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold2_idgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 11.159976279000148
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.35203016300056333
    },
    "checkpoint_sha256": "b76e3b1e3ffbdf0864de4adcd4da0848d39c0b32829bf251c6de591c92f8269f"
  }
}
```

## 2026-10-18T00:12:58+03:00 — small_model_verified

Независимая проверка contextgnn на малом наборе

Запуск: `hm_medium_cv_v2_fold2_contextgnn_inference`.

```json
{
  "status": "verified",
  "checks": {
    "val": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 0.4294001880007272
    },
    "test": {
      "passed": true,
      "predictions_identical": true,
      "scores_close": true,
      "ranked_scores_close": true,
      "map_difference": 0.0,
      "seconds": 1.2442135080000298
    },
    "checkpoint_sha256": "a8567bc18297cb7bccc3dbf985024a0ae7091284284559584ed5be46a966e4a4"
  }
}
```

## 2026-10-18T00:17:16+03:00 — recformer_ablation_measured

Recformer low_lr_warmup zero_shot: measured; replay pending

Запуск: `hm_medium_cv_v2_fold2_recformer_zero_shot`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.004503038194444444
  },
  "test_metrics": {
    "map": 0.005659976815380231
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/recformer/zero_shot"
}
```

## 2026-10-18T00:17:50+03:00 — recformer_ablation_measured

Recformer low_lr_warmup finetuned: measured; replay pending

Запуск: `hm_medium_cv_v2_fold2_recformer_finetuned`.

```json
{
  "status": "measured_pending_verification",
  "val_metrics": {
    "map": 0.009154110863095238
  },
  "test_metrics": {
    "map": 0.004952917464590862
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/recformer/finetuned"
}
```

## 2026-10-18T00:20:14+03:00 — medium_cv_third_fold_scoring_health

Health check00:20MSK: controller4552 active. Folds0/1 all9 methods evaluated and verified. Fold2 GNN2 and TDM passed evaluation/replay; Recformer predictions measured and full replay currently running onGPU(child6263). Four tree methods follow, then report. No fresh failures;25GiB disk free.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-18T00:20:36+03:00 — recformer_verified

Recformer small: independent full val/test checkpoint and item-cache replay passed

Запуск: `hm_medium_cv_v2_fold2_recformer_inference`.

```json
{
  "status": "verified",
  "checks": {
    "zero_shot": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.004503038194444444,
        "seconds": 14.536022279999997
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.005659976815380231,
        "seconds": 24.55203222199998
      },
      "checkpoint_sha256": "dc848016451b90999aa11ef3a8b957ad6b5e97e9ef402645785c2834ea287adf"
    },
    "finetuned": {
      "val": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.009154110863095238,
        "seconds": 4.769786582999586
      },
      "test": {
        "passed": true,
        "predictions_identical": true,
        "scores_close": true,
        "max_score_difference": 0.0,
        "map": 0.004952917464590862,
        "seconds": 29.741962598999635
      },
      "checkpoint_sha256": "b197ddea9f5c86734e7d5046b225a63bf9cbde3729cd00e51b162be6961c0579"
    }
  }
}
```

## 2026-10-18T00:28:09+03:00 — medium_cv_last_two_evaluations

Health check00:28MSK: controller4552 alive,25 of27 method-fold evaluations verified. Fold2 Recformer/manual/raw15 replays/checks passed; H008fold2 active(child6463), H009 last. No fresh failures. Final report and graphical QA still pending; frozen model choices unchanged.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-18T00:37:32+03:00 — medium_cv_final_evaluation_health

Health check00:37MSK:26 of27 method-fold evaluations verified. H008fold2 passed full replay; H009fold2 last evaluation active(parent6671,worker6723), CPU used. Controller4552 alive; no fresh failures. After last replay automatic report includes all6 numeric-diversity/message audits and uncertainty plots; visual QA pending.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "evaluating"
}
```

## 2026-10-18T00:41:27+03:00 — medium_cv_all_evaluations_verified

All27 method-fold evaluations/replays completed successfully; report process6874 active, numeric-diversity audit child6884 active. Numeric audit may identify value-identical sets among20 structurally distinct accepted programs; diagnostic only, no new API, fits or selection changes. Final comparison/plots and visual QA pending.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "reporting"
}
```

## 2026-10-18T00:45:56+03:00 — medium_cv_complete

Temporal CV comparison and frozen replays completed. See report for per-fold results, uncertainty and limits.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "complete",
  "artifacts": "reports/medium_cv_v2/report.md"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 LightGBM manual: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_manual`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0025059816890336604,
    "recall12": 0.011005825070475045,
    "hit12": 0.037520391517128875,
    "users": 1839,
    "conditional_catalog_map": 0.004738431957279919,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/lightgbm_manual",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 LightGBM raw15: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_raw15`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.001972438724749763,
    "recall12": 0.004203889277298738,
    "hit12": 0.015769439912996192,
    "users": 1839,
    "conditional_catalog_map": 0.0055601945149358935,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/lightgbm_raw15",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 ID-GNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_idgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0,
    "recall12": 0.0,
    "hit12": 0.0,
    "users": 1839,
    "conditional_catalog_map": 0.0,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/gnn/idgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 ContextGNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_contextgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.00030906536820076786,
    "recall12": 0.0008378893778567515,
    "hit12": 0.004893964110929853,
    "users": 1839,
    "conditional_catalog_map": 0.0005319901602229188,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/gnn/contextgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 Recformer zero-shot: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_recformer_zero_shot`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.008612966847061464,
    "recall12": 0.015006903404130157,
    "hit12": 0.03588907014681892,
    "users": 1839,
    "conditional_catalog_map": 0.017767266258645567,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/recformer/zero_shot",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 Recformer LR/warmup: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_recformer_finetuned`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004928330862942065,
    "recall12": 0.015232004265446351,
    "hit12": 0.03643284393692224,
    "users": 1839,
    "conditional_catalog_map": 0.009898372156405072,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/recformer/finetuned",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 TDM fixed beam64: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_tdm_fixed`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0019525557695079176,
    "recall12": 0.006501284498837517,
    "hit12": 0.022294725394236,
    "users": 1839,
    "conditional_catalog_map": 0.00406271675178415,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/tdm/fixed/beam",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 API GPT H008 best-only: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_h008`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.005226402635029218,
    "recall12": 0.012804079794291864,
    "hit12": 0.03806416530723219,
    "users": 1839,
    "conditional_catalog_map": 0.009940724512628901,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/h008",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold0 API GPT H009 full history: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold0_h009`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004640644383711269,
    "recall12": 0.01506438610027517,
    "hit12": 0.043501903208265365,
    "users": 1839,
    "conditional_catalog_map": 0.008864673945003098,
    "conditional_users": 1276,
    "zero_retrievable_users": 563
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/h009",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_family_final_verified

Fold0 gnn: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold0_gnn`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/gnn"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_family_final_verified

Fold0 recformer: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold0_recformer`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_0/recformer"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 LightGBM manual: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_manual`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004127791919344464,
    "recall12": 0.013877969640123139,
    "hit12": 0.044399596367305755,
    "users": 1982,
    "conditional_catalog_map": 0.0140265979938524,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/lightgbm_manual",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 LightGBM raw15: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_raw15`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0012659325342221407,
    "recall12": 0.002684759401791639,
    "hit12": 0.00958627648839556,
    "users": 1982,
    "conditional_catalog_map": 0.003913972296633925,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/lightgbm_raw15",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 ID-GNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_idgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.00047792900656170077,
    "recall12": 0.0018429756699181522,
    "hit12": 0.006559031281533804,
    "users": 1982,
    "conditional_catalog_map": 0.001407047565737742,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/gnn/idgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 ContextGNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_contextgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0004727249429570318,
    "recall12": 0.0024133871510258996,
    "hit12": 0.006054490413723511,
    "users": 1982,
    "conditional_catalog_map": 0.0012045306125910659,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/gnn/contextgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 Recformer zero-shot: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_recformer_zero_shot`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004664410247785625,
    "recall12": 0.010110689229335997,
    "hit12": 0.026236125126135216,
    "users": 1982,
    "conditional_catalog_map": 0.012723416848101986,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/recformer/zero_shot",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 Recformer LR/warmup: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_recformer_finetuned`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.003784240038654771,
    "recall12": 0.009945872545851301,
    "hit12": 0.024217961654894045,
    "users": 1982,
    "conditional_catalog_map": 0.00933415054951579,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/recformer/finetuned",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 TDM fixed beam64: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_tdm_fixed`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0015955464864395234,
    "recall12": 0.006959766464055061,
    "hit12": 0.020181634712411706,
    "users": 1982,
    "conditional_catalog_map": 0.004813215518505191,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/tdm/fixed/beam",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 API GPT H008 best-only: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_h008`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004438860883109117,
    "recall12": 0.014126355097541425,
    "hit12": 0.044399596367305755,
    "users": 1982,
    "conditional_catalog_map": 0.013030244217796694,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/h008",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold1 API GPT H009 full history: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold1_h009`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.003866700796550504,
    "recall12": 0.014749322462490978,
    "hit12": 0.04490413723511604,
    "users": 1982,
    "conditional_catalog_map": 0.011599044760853565,
    "conditional_users": 1191,
    "zero_retrievable_users": 791
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/h009",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_family_final_verified

Fold1 gnn: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold1_gnn`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/gnn"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_family_final_verified

Fold1 recformer: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold1_recformer`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_1/recformer"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold2 LightGBM manual: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_manual`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0037554084226640175,
    "recall12": 0.01340750179060905,
    "hit12": 0.043580683156654886,
    "users": 1698,
    "conditional_catalog_map": 0.013533951306001707,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/lightgbm_manual",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold2 LightGBM raw15: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_raw15`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0009851763753412754,
    "recall12": 0.005005676825464812,
    "hit12": 0.015901060070671377,
    "users": 1698,
    "conditional_catalog_map": 0.004225228337484924,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/lightgbm_raw15",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold2 ID-GNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_idgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.0002372071718361471,
    "recall12": 0.000785237534354142,
    "hit12": 0.0017667844522968198,
    "users": 1698,
    "conditional_catalog_map": 0.0007636502481863306,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/gnn/idgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:31+03:00 — medium_cv_method_final_verified

Fold2 ContextGNN: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_contextgnn`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 4.9077345897133886e-06,
    "recall12": 4.907734589713388e-05,
    "hit12": 0.0005889281507656066,
    "users": 1698,
    "conditional_catalog_map": 5.72737686139748e-05,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/gnn/contextgnn",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_method_final_verified

Fold2 Recformer zero-shot: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_recformer_zero_shot`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.005659976815380231,
    "recall12": 0.0117937961135841,
    "hit12": 0.023557126030624265,
    "users": 1698,
    "conditional_catalog_map": 0.0165278624900618,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/recformer/zero_shot",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_method_final_verified

Fold2 Recformer LR/warmup: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_recformer_finetuned`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004952917464590862,
    "recall12": 0.011813816009929081,
    "hit12": 0.023557126030624265,
    "users": 1698,
    "conditional_catalog_map": 0.014009527445953563,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/recformer/finetuned",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_method_final_verified

Fold2 TDM fixed beam64: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_tdm_fixed`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.002962433357260605,
    "recall12": 0.009445986742806532,
    "hit12": 0.02591283863368669,
    "users": 1698,
    "conditional_catalog_map": 0.010603590077080505,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/tdm/fixed/beam",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_method_final_verified

Fold2 API GPT H008 best-only: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_h008`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.004197712632145298,
    "recall12": 0.01148110396343612,
    "hit12": 0.038869257950530034,
    "users": 1698,
    "conditional_catalog_map": 0.014686258758423706,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/h008",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_method_final_verified

Fold2 API GPT H009 full history: final original-target test metrics; saved-model replay and independent metric check passed.

Запуск: `hm_medium_cv_v2_fold2_h009`.

```json
{
  "status": "complete",
  "test_metrics": {
    "map": 0.005133956131698573,
    "recall12": 0.013804434179875875,
    "hit12": 0.04299175500588928,
    "users": 1698,
    "conditional_catalog_map": 0.018233866648815104,
    "conditional_users": 873,
    "zero_retrievable_users": 825
  },
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/h009",
  "evaluation_scope": "Original weekly targets including outside-catalog purchases; fixed10000-item catalog"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_family_final_verified

Fold2 gnn: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold2_gnn`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/gnn"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_family_final_verified

Fold2 recformer: all reported variants verified.

Запуск: `hm_medium_cv_v2_fold2_recformer`.

```json
{
  "status": "complete",
  "artifacts": "CVBenchmark/results/medium_v2/fold_2/recformer"
}
```

## 2026-10-18T00:52:32+03:00 — medium_cv_final_review_complete

All27 method-fold results verified;3fold paired report, numeric/API audits and4 figures visually reviewed. Comparison is internal and conditional on3 weeks/1 seed; no universal good/bad claim.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "complete",
  "artifacts": "reports/medium_cv_v2/report.md",
  "comparison_summary": [
    {
      "method": "manual",
      "label": "LightGBM manual",
      "pooled_map": 0.0034728152585535663,
      "ci95_low": 0.002689589697128854,
      "ci95_high": 0.00437121626461813,
      "equal_fold_map": 0.0034630606770140473,
      "fold_maps": [
        0.0025059816890336604,
        0.004127791919344464,
        0.0037554084226640175
      ],
      "conditional_catalog_map": 0.010349418227037985
    },
    {
      "method": "raw15",
      "label": "LightGBM raw15",
      "pooled_map": 0.0014149705712941806,
      "ci95_low": 0.0009301776364485842,
      "ci95_high": 0.002011699641134648,
      "equal_fold_map": 0.0014078492114377266,
      "fold_maps": [
        0.001972438724749763,
        0.0012659325342221407,
        0.0009851763753412754
      ],
      "conditional_catalog_map": 0.004624243576339384
    },
    {
      "method": "idgnn",
      "label": "ID-GNN",
      "pooled_map": 0.00024461552251912823,
      "ci95_low": 0.00010682479816394456,
      "ci95_high": 0.0004075103533474099,
      "equal_fold_map": 0.00023837872613261595,
      "fold_maps": [
        0.0,
        0.00047792900656170077,
        0.0002372071718361471
      ],
      "conditional_catalog_map": 0.0007013354243893166
    },
    {
      "method": "contextgnn",
      "label": "ContextGNN",
      "pooled_map": 0.0002742608049275923,
      "ci95_low": 0.00011152444900486036,
      "ci95_high": 0.0004860268873130335,
      "equal_fold_map": 0.0002622326819158377,
      "fold_maps": [
        0.00030906536820076786,
        0.0004727249429570318,
        4.9077345897133886e-06
      ],
      "conditional_catalog_map": 0.0006477291628863484
    },
    {
      "method": "recformer_zero",
      "label": "Recformer zero-shot",
      "pooled_map": 0.006286419238154154,
      "ci95_low": 0.0048685735793580695,
      "ci95_high": 0.007855303136564623,
      "equal_fold_map": 0.006312451303409107,
      "fold_maps": [
        0.008612966847061464,
        0.004664410247785625,
        0.005659976815380231
      ],
      "conditional_catalog_map": 0.015644744061660228
    },
    {
      "method": "recformer_lr",
      "label": "Recformer LR/warmup",
      "pooled_map": 0.004525025922891737,
      "ci95_low": 0.003438627424487717,
      "ci95_high": 0.005732225124866504,
      "equal_fold_map": 0.004555162788729233,
      "fold_maps": [
        0.004928330862942065,
        0.003784240038654771,
        0.004952917464590862
      ],
      "conditional_catalog_map": 0.010771740609689712
    },
    {
      "method": "tdm",
      "label": "TDM fixed beam64",
      "pooled_map": 0.002135048928587915,
      "ci95_low": 0.0015730103477115513,
      "ci95_high": 0.0027807945105828807,
      "equal_fold_map": 0.0021701785377360155,
      "fold_maps": [
        0.0019525557695079176,
        0.0015955464864395234,
        0.002962433357260605
      ],
      "conditional_catalog_map": 0.006039970178175909
    },
    {
      "method": "h008",
      "label": "API GPT H008 best-only",
      "pooled_map": 0.004627086929792302,
      "ci95_low": 0.003594993036765165,
      "ci95_high": 0.0058141459891102145,
      "equal_fold_map": 0.004620992050094544,
      "fold_maps": [
        0.005226402635029218,
        0.004438860883109117,
        0.004197712632145298
      ],
      "conditional_catalog_map": 0.012282781208866536
    },
    {
      "method": "h009",
      "label": "API GPT H009 full history",
      "pooled_map": 0.004514477896726273,
      "ci95_low": 0.003533006715982536,
      "ci95_high": 0.005613539043720563,
      "equal_fold_map": 0.004547100437320116,
      "fold_maps": [
        0.004640644383711269,
        0.003866700796550504,
        0.005133956131698573
      ],
      "conditional_catalog_map": 0.012288608337849142
    }
  ]
}
```

## 2026-10-18T00:53:05+03:00 — medium_cv_hypotheses_conclusions

Added dated H008/H009 temporal-CV evidence to HYPOTHESES.md without replacing earlier experiments. Russian summary/report links saved. H009 advantage overH008 not established; H008 vsmanual promising but paired95%CI includes0. All computations and visual/checkpoint review complete.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "complete"
}
```

## 2026-10-18T00:56:17+03:00 — medium_cv_bootstrap_documented

Added detailed paired customer-cluster percentile-bootstrap method to summary_ru.md and report.md:4548 customers/5519 outer-test rows, sampling with replacement and retaining weeks jointly,5000 replicates/seed42,variable observation denominator,paired differences and2.5/97.5 percentiles. H008-minus-manual example checked against savedCSV with sign reversal. Documentation only; no metric,model,source-code or plot changes.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "complete"
}
```

## 2026-10-18T01:04:55+03:00 — contextgnn_regression_diagnosed

Read-only comparison: old ContextGNN248 distinct top12 lists/250users/1574recommended items; medium folds11/8/11lists across1839/1982/1698users, only24/26/26items. Ranking personalization collapsed. Root cause unresolved; larger catalog/full-target denominator alone insufficient(conditionalMAP also very low). Saved audit and notes, no new fitting/inference or model changes; do not infer architectural failure.

Запуск: `hm_medium_temporal_cv_v2`.

```json
{
  "status": "complete"
}
```
