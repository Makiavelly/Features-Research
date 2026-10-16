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
