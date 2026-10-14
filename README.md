# Features: эксперименты H&M / RelBench

Код, метрики и отчёты доступны в Git. Данные, GloVe, обученные ID-GNN и
DecisionTree, предсказания, кэши и окружения исключены через `.gitignore`.
Клонирование репозитория само по себе не восстанавливает эти файлы.

## Что скачать после клонирования

Команды ниже выполняются из корня проекта в Ubuntu / WSL; Python >= 3.11.

| Артефакт | Источник / версия | Куда сохранить |
|---|---|---|
| H&M: 18 файлов, включая db и train/val/test | `stanford-star/relbench-v1`, ревизия `7abf5d46a48534d918704ca2af278861b932f4dc` | `data/rel-hm/` |
| GloVe 6B 300d для текстовых признаков | `sentence-transformers/average_word_embeddings_glove.6B.300d`, ревизия `e5e8fec6971be8960cfaa853a77a6ddc62a265d7` | `data/models/glove/` |
| RelBench | [исходники](https://github.com/stanford-star/relbench), commit `919fb8a61a4b4cb787283860597f45701895578d` | `RelBenchGNN/upstream/` |
| Экспертные SQL | [RelBench User Study](https://github.com/snap-stanford/relbench-user-study), commit `445bb7a3b1230f49f8e5890ae81754d3e365680f` | `baseline/expert_upstream/` |

```bash
python3 RelBenchGNN/restore_downloads.py all
```

Скрипт использует зафиксированные ревизии и проверяет размер и SHA256 каждого
файла по `data/download_manifest.json` и `data/glove_download_manifest.json`.
Правильные локальные файлы пропускаются. Проверка без скачивания:

```bash
python3 RelBenchGNN/restore_downloads.py all --verify-only
```

Старые `download_data.py` и `download_glove.py` обращаются к текущей версии
источника; для восстановления именно этого эксперимента используйте
`restore_downloads.py`.

Если каталоги исходников отсутствуют, восстановите их:

```bash
git clone https://github.com/stanford-star/relbench.git RelBenchGNN/upstream
git -C RelBenchGNN/upstream checkout 919fb8a61a4b4cb787283860597f45701895578d
git clone https://github.com/snap-stanford/relbench-user-study.git baseline/expert_upstream
git -C baseline/expert_upstream checkout 445bb7a3b1230f49f8e5890ae81754d3e365680f
```

## Обученные веса: отдельные локальные артефакты

Публичная ссылка на скачивание наших обученных весов пока не опубликована.
GloVe — входной текстовый кодировщик; скачивание GloVe не восстанавливает ID-GNN.
Для точного повторения инференса запросите у владельца проекта:

- `RelBenchGNN/results/seed_42/best.pt` — ID-GNN seed 42, лучшая эпоха 19;
  SHA256: `f5439416aeeb6f0f2dedab20aabb14ea541b4bd98b70f21334986dc03a05abc4`.
- `RelBenchGNN/results/seed_42/last.pt` — дополнительно для продолжения обучения.
- `RelBenchGNN/results/seed_42/val_predictions.npy` и `test_predictions.npy` —
  эталонные предсказания для скрипта независимой проверки инференса.
- `baseline/results/manual_v1/decision_tree/seed_42/model.joblib` —
  DecisionTree вместе с кодировщиком и списками признаков.

Сохраните файлы по этим же относительным путям. Конфигурации и JSON метрик
должны соответствовать переданным весам. Текстовые модели LightGBM
`baseline/results/manual_v1/lightgbm/seed_42/model.txt` и
`baseline/results/gnn_embeddings_v1/model.txt` не исключены из Git.

Без передачи локальных весов требуется повторное обучение. Его результат
не гарантирует побитовое совпадение или прежние метрики. Сохранённые JSON
результатов не являются признаком наличия весов на новом компьютере:
`run_experiment.sh full` пропускает каталог с `metrics.json`. Не используйте
эту команду для восстановления отсутствующих весов в клоне с прежними
результатами; создайте новый каталог и уникальный `run_id` согласно
[протоколу](RelBenchGNN/README.md). Старые результаты сохраняйте.

Кэши `RelBenchGNN/cache/` и `baseline/cache/` строятся кодом экспериментов;
скачивать их отдельно не требуется. Окружение и инструкции запуска описаны
в [RelBenchGNN/README.md](RelBenchGNN/README.md). `setup_wsl.sh` требует локальный
`RelBenchGNN/tools/uv.tar.gz`: этот инструмент также исключён из Git;
перед запуском setup восстановите его из дистрибутива uv для Linux x86_64
или настройте окружение по `RelBenchGNN/requirements.lock.txt`.

Итоги: [EXPERIMENTS.md](EXPERIMENTS.md), отчёты в `reports/`.
